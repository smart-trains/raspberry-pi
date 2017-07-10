import RPi.GPIO as gpio
from time import sleep
from datetime import datetime as dt

# helper type
class Const(object):
 	_RO = 10
 	_DI = 8

 	@property # Receiver Output (=Pi input)
 	def PIN_RO(self):
 		return type(self)._RO
 	@property # Driver Input (=Pi output)
 	def PIN_DI(self):
 		return type(self)._DI

c = Const()

# Borad setup
gpio.setmode(gpio.BOARD)
gpio.setup(c.PIN_RO, gpio.IN, gpio.PUD_UP)
gpio.setup(c.PIN_DI, gpio.OUT);

gpio.output(c.PIN_DI, 0) # disable

# Program
try:
	while True:
		gpio.output(c.PIN_DI, dt.now().second % 2)
		sleep(1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
gpio.cleanup()
