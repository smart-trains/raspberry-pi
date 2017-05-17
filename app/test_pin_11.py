import RPi.GPIO as gpio
from time import sleep
from datetime import datetime as dt

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.IN)

try:
	while True:
		print("[{0}] {1}".format(dt.now(), gpio.input(11)))
		sleep(0.5)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
gpio.cleanup()
