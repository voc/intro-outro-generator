#!/usr/bin/python3
import xmlrpc.client
import socket
import time
import sys
import os
import c3t_rpc_client as rpc

print("C3TT preroll generator")

if os.environ.get('CRS_TOKEN') is None or os.environ.get('CRS_SECRET') is None:
	print('CRS_TOKEN or CRS_SECRET is empty. did you source the tracker-scripts-profile?')
	sys.exit(1)

ticket_type = 'recording'
ticket_state = 'generating'

host = socket.getfqdn()
url = os.environ['CRS_TRACKER']
token = os.environ['CRS_TOKEN']
secret = os.environ['CRS_SECRET']

filter = {}
if not os.environ.get('CRS_ROOM') is None:
	filter['Fahrplan.Room'] = os.environ['CRS_ROOM']

def generatePreroll(ticket):
	print('generating preroll for', ticket)

while True:
	print('Asking RPC for {0}-tickets which are ready for state {1}'.format(ticket_type, ticket_state))

	ticket_id = rpc.assignNextUnassignedForState(ticket_type, ticket_state, url, token, host, secret, filter)
	if ticket_id != False:
		ticket = rpc.getTicketProperties(str(ticket_id), url, token, host, secret)
		generatePreroll(ticket)
	
	else:
		print('No ticket found')
	
	print('Sleeping for 30 seconds')
	time.sleep(30);

