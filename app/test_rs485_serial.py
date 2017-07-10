import serial
from time import sleep
from datetime import datetime as dt

s = serial.Serial(port="/dev/ttyAMA0")

# Program
try:
	while True:
		s.write("caosi pangpang")
		sleep(1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
serial.close()
