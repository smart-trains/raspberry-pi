import serial
from time import sleep
from datetime import datetime as dt

s = serial.Serial(
		port="/dev/ttyAMA0",
		bytesize=serial.EIGHTBITS
	)

# Program
try:
	while True:
		s.write(b"caosi pangpang")
		sleep(1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
serial.Serial.close()
