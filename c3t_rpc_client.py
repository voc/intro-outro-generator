#!/usr/bin/python3
#    Copyright (C) 2014  derpeter
#    derpeter@berlin.ccc.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xmlrpc.client
import hashlib
import hmac
import socket
import urllib
import xml
import sys


## client constructor #####
# group: worker group
# secret: client secret
# host: client hostname (will be taken from local host if set to None)
# url: tracker url (without the rpc)
# method: method to access
############################
def C3TClient(url, method, group, host, secret, args):
    if 'rpc' != url[-3:]:
        url = url + "rpc"
    
#     if host == None:
#         host = socket.getfqdn()
        
    #####################
    # generate signature
    #####################
    # assemble static part of signature arguments
    # 1. URL  2. method name  3. worker group token  4. hostname
    sig_args = urllib.parse.quote(url  + "&" + method + "&" + group + "&" + host + "&", '')
    
    #### add method args
    if len(args) > 0:
        i = 0
        while i < len(args):
            arg = args[i]
            if isinstance(arg, dict):
                for k in arg:
                    sig_args = str(sig_args) + urllib.parse.quote("[" + str(k) + "]", '') + "=" + urllib.parse.quote(str(arg[k]), '')
            else:
                sig_args = str(sig_args) + urllib.parse.quote(str(arg), '')
            
            if i < (len(args) -1):
                sig_args = sig_args + urllib.parse.quote("&", '')
            i = i + 1
    
        
    #### generate the hmac hash with key
    hash =  hmac.new(bytes(secret, 'utf-8'), bytes(sig_args, 'utf-8'), hashlib.sha256)
    
    #### add signature as last parameter to the arg list
    args.append(hash.hexdigest())
    
    #### create xmlrpc client
    print('creating XML RPC proxy: ' + url + "?group=" + group + "&hostname=" + host)
    try:
        proxy = xmlrpc.client.ServerProxy(url + "?group=" + group + "&hostname=" + host);
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
        sys.exit()
    except xmlrpc.client.ProtocolError as err:
        print("A protocol error occurred")
        print("URL: %s" % err.url)
        print("HTTP/HTTPS headers: %s" % err.headers)
        print("Error code: %d" % err.errcode)
        print("Error message: %s" % err.errmsg)
        sys.exit()
    except socket.gaierror as err:
        print("A socket error occurred")
        print(err)
        sys.exit()
    except xmlrpc.client.ProtocolError as err:
        print("A Protocol occurred")
        print(err)
        sys.exit()
    
    #### call the given method with args
    try:
        print(method + str(args))
        result = getattr(proxy,method)(*args)
    except xml.parsers.expat.ExpatError as err:
        print("A expat err occured")
        print(err)
        sys.exit()
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
        sys.exit()
    except xmlrpc.client.ProtocolError as err:
        print("A protocol error occurred")
        print("URL: %s" % err.url)
        print("HTTP/HTTPS headers: %s" % err.headers)
        print("Error code: %d" % err.errcode)
        print("Error message: %s" % err.errmsg)
        sys.exit()
    #### return the result
    return result

def open_rpc(method, args, url, group, host, secret):
    result = C3TClient(url, method, group, host, secret, args)
    return result

### get Tracker Version
def getVersion():
    tmp_args = ["1"];
    return str(open_rpc("C3TT.getVersion",tmp_args))

### check for new ticket on tracker an get assignement 
def assignNextUnassignedForState(from_state, to_state, url, group, host, secret, filter = {}):
    tmp_args = [from_state, to_state, filter]
    xml = open_rpc("C3TT.assignNextUnassignedForState",tmp_args,url, group, host, secret)
    # if get no xml there seems to be no ticket for this job
    if xml == False:
        return False
    else:
        print(xml)
        return xml['id']

### get ticket properties 
def getTicketProperties(id ,url, group, host, secret):
    tmp_args = [id]
    xml = open_rpc("C3TT.getTicketProperties",tmp_args, url, group, host, secret)
    if xml == False:
        print("no xml in answer")
        return None
    else:
        print(xml)
        return xml

### set Ticket status on done
def setTicketDone(id, url, group, host, secret):
    tmp_args = [id]
    xml = open_rpc("C3TT.setTicketDone", tmp_args , url, group, host, secret)
    print(xml)
    
### set ticket status on failed an supply a error text
def setTicketFailed(id,error , url, group, host, secret):
    tmp_args = [id, error]
    xml = open_rpc("C3TT.setTicketFailed", tmp_args , url, group, host, secret)
