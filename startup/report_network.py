from subprocess import check_output
from time import sleep
import http.client as http
import json

def getssid():
	try:
		ssid = check_output(["iwgetid"])\
		.decode('utf-8')\
		.split("ESSID:")[1]\
		.translate(
			{ord(c): '' for c in '\n"'}
		)
		return ssid
	except:
		return None

def getip():
	try:
		ip = check_output(["hostname", "-I"])\
		.decode('utf-8')\
		.translate(
			{ord(c): '' for c in '\n '}
		)
		return ip
	except:
		return None

def test_internet():
	conn = http.HTTPConnection("www.google.com", timeout=2)
	result = False
	try:
		conn.request("HEAD", "/")
		result = True
	except:
		pass
	finally:
		conn.close()
	return result

def report_network():
	conn = http.HTTPConnection(_server)
	headers = {'Content-type': 'application/json'}
	result = False
	try:
		conn.request("POST", _api, json.dumps({'ssid': getssid(), 'ip': getip()}), headers)
		result = True
	except:
		pass
	finally:
		conn.close()
	return result

_connected = False

_max_count = 1000
_count = 0
_end_trying = False

_server = "52.65.244.105"
_api = "/api/rpi_ip"

while not _end_trying:
	if test_internet():
		print("attempt {0}: successful".format(_count))
		_end_trying = True
		_connected = True
	else:
		print("attempt {0}: failed".format(_count))
		if _count >= _max_count:
			_end_trying = True
		else:
			sleep(1)
	_count += 1

if (_connected):
	_count = 0
	_end_trying = False
	while not _end_trying:
		if report_network():
			print('attempt to connect {0} successful'.format(_server))
			_end_trying = True
		else:
			print('attempt to connect {0} failed'.format(_server))
			if _count >= _max_count:
				_end_trying = True
			else:
				sleep(1)
		
	


