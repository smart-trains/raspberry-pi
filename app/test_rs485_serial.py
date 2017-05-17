import serial
from time import sleep
from datetime import datetime as dt

s = serial.Serial(port="/dev/ttyAMA0")

# Program
try:
	while True:
		s.write(b"caosi pangpang")
		sleep(0.1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
s.close()
