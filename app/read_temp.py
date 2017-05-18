from digitemp.master import UART_Adapter
from digitemp.device import DS18B20

server = "52.65.244.105"
api = "/api/temperature"

bus = UART_Adapter('/dev/serial0')  # DS9097 connected to COM1

# only one 1-wire device on the bus:
sensor = DS18B20(bus)

sensor.info()

temp = sensor.get_temperature()

# get temperature
print(temp)

conn = http.HTTPConnection(server)
	headers = {'Content-type': 'application/json'}
try:
	conn.request("POST", api, json.dumps({'temperature': temp}), headers)
	print("report to {0} successful".format(server))
except:
	print("report to {0} failed".format(server))
finally:
	conn.close()