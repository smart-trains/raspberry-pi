from digitemp.master import UART_Adapter
from digitemp.device import DS18B20

bus = UART_Adapter('/dev/serial0')  # DS9097 connected to COM1

# only one 1-wire device on the bus:
sensor = DS18B20(bus)

sensor.info()

# get temperature
print(sensor.get_temperature())