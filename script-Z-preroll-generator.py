#!/usr/bin/python3
import xmlrpc.client
import traceback
import socket
import time
import sys
import os

import renderlib
import c3t_rpc_client as rpc

print("C3TT preroll generator")
renderlib.debug = True

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

projects = {}
def generatePreroll(ticket):
	print(ticket)
	projectname = ticket.get('Processing.Prerolls.Slug', ticket['Meta.Acronym'])
	if not projectname in projects:
		projects[projectname] = renderlib.loadProject(projectname)

	project = projects[projectname]
	task = project.ticket(ticket)
	task.outfile = os.path.join(ticket['Processing.Path.Intros'], ticket['Fahrplan.ID'] + '.dv')
	task.workdir = os.path.join(os.getcwd(), projectname, 'artwork')

	print("rendering")
	renderlib.rendertask(task)

	if hasattr(project, 'deploy'):
		print("deploying")
		project.deploy(ticket, task)


while True:
	print('Asking RPC for {0}-tickets which are ready for state {1}'.format(ticket_type, ticket_state))

	ticket_id = rpc.assignNextUnassignedForState(ticket_type, ticket_state, url, token, host, secret, filter)
	if ticket_id != False:
		ticket = rpc.getTicketProperties(str(ticket_id), url, token, host, secret)
		try:
			generatePreroll(ticket)
			rpc.setTicketDone(str(ticket_id), url, token, host, secret)
		except:
			error = str(traceback.format_exc())
			print(error)
			rpc.setTicketFailed(str(ticket_id), error, url, token, host, secret)
	
	else:
		print('No ticket found')
	
	print('Sleeping for 30 seconds')
	time.sleep(30);

