#AUTHOR : GAUTHAM V KIDIYOOR
'''

Emulate a common dictionary among n peer to peer process, which are in a circular topology.

Create n independent process ( Eg : python node.py <portNo> <nextPortNo> )

PROBLEM STATEMENT : 

There are N identical processes in a peer-to-peer system, which are arranged 

in a circular topology. The system supports a set of operations which are 

defined by a language, like

a. GET key

b. POST key value

c. PUT key value

d. DELETE key

It is possible to operate these instructions from any process. For example we 

can do this,

Process 1:  ADD key1 value1

Process 2:  GET key1 

Process 3:  DELETE key1

Process 1:  Get key1

Process 2:  Get key1

The system should behave in a consistent way; meaning answer to any such 

command should give same result across all processes.

Implement the above system, assuming the processes are perfect and do not 

fail.


'''


import sys
from flask import Flask, request
import urllib
import urllib2
import httplib2


app = Flask(__name__)


# Acts as unique process id
port = "port, to be assigned"
#singly linked circular topology
nextport = "next port, to be assigned"

d = {}

change = 0
trip = 0

@app.route('/display')
def display():
	s = str(d)
	return s

@app.route('/GET')
def get():
	key = request.args.get('key')
	if key in d.keys():
		out = "value of key : <b>"+ key + "</b> is : <b>" + d[key] + "</b>"
	else:
		out = "Key not found"
	return out

@app.route('/POST')
def post():
	key = request.args.get('key')
	value = request.args.get('value')
	
	action = "POST"
	url = "http://127.0.0.1:"+str(nextport)+"/status?id=" +str(port) + "&action="+action+"&key="+key+ "&value="+value
	httplib2.Http().request(url)

	if key in d.keys():
		out = "Key already present"
	else:
		d[key] = value
		out = "Key inserted"
	return out

@app.route('/PUT')
def put():
	key = request.args.get('key')
	value = request.args.get('value')
	
	action = "PUT"
	url = "http://127.0.0.1:"+str(nextport)+"/status?id=" +str(port) + "&action="+action+"&key="+key+ "&value="+value
	httplib2.Http().request(url)

	if key in d.keys():
		d[key] = value
		out = "Key : <b>"+ key + "</b> updated with value : <b>"+ value + "</b>"
		change = 1
	else:
		out = "Key not present"
	return out

@app.route('/DELETE')
def delete():
	key = request.args.get('key')
	
	action = "DEL"
	url = "http://127.0.0.1:"+str(nextport)+"/status?id=" +str(port) + "&action="+action+"&key="+key
	httplib2.Http().request(url)
	
	if key in d.keys():
		d.pop(key)
		out = "Key : <b>"+ key + "</b> deleted"
	else:
		out = "Key not present"
	return out

@app.route('/status',methods=['GET', 'POST'])
def status():
	id1 = request.args.get('id')
	action = request.args.get('action')
	if action == 'POST':
		key = request.args.get('key')
		value = request.args.get('value')
		d[key] = value
	elif action == 'DEL':
		key = request.args.get('key')
		value = "somevalue" # refer the http call made
		d.pop(key)
	elif action == 'PUT':
		key = request.args.get('key')
		value= request.args.get('value')
		d[key] = value


	if id1 ==str(nextport):
		return "success"
	if id1 != str(port) :
			url = "http://127.0.0.1:"+str(nextport)+"/status?id="+str(id1)+"&action="+action+"&key="+key+ "&value="+value
			#url = "http://127.0.0.1:4000/status?id=4000&action=POST&key=key1&value=value1"
			#req = urllib2.Request(url)
			#res = urllib2.urlopen(req).read()
			httplib2.Http().request(url)
	return "success"

def callurl(url1):
    return urllib2.urlopen(url1)

if __name__ == '__main__':
	port = int(sys.argv[1])
	print(sys.argv[2])
	nextport = int(sys.argv[2])
	app.debug = True
	app.run(port = port)