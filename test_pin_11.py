import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.IN)

try:
	while True:
		print(gpio.input(11))
		sleep(1)
except KeyboardInterrupt:
	pass

print("Gracefully exiting")
gpio.cleanup()