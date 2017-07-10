import RPi.GPIO as gpio
from time import sleep
from datetime import datetime as dt

# helper type
class Const(object):
 	"""docstring for Const"""
 	def __init__(self, arg):
 		raise TypeError("The Const type is not allowed to be instantiated.")

 	_RO = 31
 	_RE = 33
 	_DE = 35
 	_DI = 37

 	@property # Receiver Output
 	def PIN_RO(self):
 		return type(self)._RO
 	@property # Receiver output Enable, active LOW
 	def PIN_RE(self):
 		return type(self)._RE
 	@property # Driver output Enable, active HIGH
 	def PIN_DE(self):
 		return type(self)._DE
 	@property # Driver Input
 	def PIN_DI(self):
 		return type(self)._DI

# Borad setup
gpio.setmode(gpio.BOARD)
gpio.setup(Const.PIN_RO, gpio.IN, gpio.PUD_UP)
gpio.setup(Const.PIN_RE, gpio.OUT, gpio.PUD_UP);
gpio.setup(Const.PIN_DE, gpio.OUT, gpio.PUD_DOWN);
gpio.setup(Const.PIN_DI, gpio.OUT, gpio.PUD_UP);

gpio.output(Const.PIN_DE, 1)

# Program
try:
	while True:
		gpio.output(Const.PIN_DI, dt.datetime.now().second % 2)
		sleep(1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
gpio.cleanup()
