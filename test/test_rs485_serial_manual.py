import serial
import RPi.GPIO as gpio
from time import sleep, time
from datetime import datetime as dt

RE = 13 # Read enable, active LOW
#DE = 15 # Drive enable, active HIGH

s = serial.Serial(port="/dev/ttyAMA0", baudrate=115200, timeout=0)
gpio.setmode(gpio.BOARD)
gpio.setup(RE, gpio.OUT)
#gpio.setup(DE, gpio.OUT)
gpio.output(RE, gpio.LOW)
#gpio.output(DE, gpio.LOW)

# Program
try:
	while True:
		gpio.output(RE, gpio.HIGH)
#		gpio.output(DE, gpio.HIGH)
		s.write(bytearray([0x51]))
		gpio.output(RE, gpio.LOW)
#		gpio.output(DE, gpio.LOW)
		start_t = time()
		while(not s.in_waiting):
			if(time() - start_t > 0.1):
				break
		print(s.read(9))
		sleep(0.001)

except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
gpio.cleanup()
s.close()
