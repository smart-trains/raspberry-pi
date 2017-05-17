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

_max_count = 1000
_count = 0
_connected = False
_end_trying = False

while not _end_trying:
	conn = http.HTTPConnection("www.google.com", timeout=2)
	try:
		conn.request("HEAD", "/")
		_connected = True
		_end_trying = True
	except:
		pass
	finally:
		conn.close()

	_count += 1
	if _count >= _max_count:
		_end_trying = True
	if _connected:
		print("attempt {0}: successful".format(_count))
	else:
		print("attempt {0}: failed".format(_count))
	if not _end_trying:
		sleep(1)

if (_connected):
	_sent = False
	conn = http.HTTPConnection("52.65.244.105")
	headers = {'Content-type': 'application/json'}

	while not _sent:
		try:
			conn.request("POST", "/api/rpi_ip", json.dumps({'ssid': getssid(), 'ip': getip()}), headers)
			_sent = True
		except:
			pass
		finally:
			conn.close()
