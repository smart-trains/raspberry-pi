import RPi.GPIO as gpio
from time import sleep
from datetime import datetime as dt

# helper type
class Const(object):
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

c = Const()

# Borad setup
gpio.setmode(gpio.BOARD)
gpio.setup(c.PIN_RO, gpio.IN, gpio.PUD_UP)
gpio.setup(c.PIN_RE, gpio.OUT);
gpio.setup(c.PIN_DE, gpio.OUT);
gpio.setup(c.PIN_DI, gpio.OUT);

gpio.output(c.PIN_RE, 1) # disable
gpio.output(c.PIN_DE, 1) # enable

# Program
try:
	while True:
		gpio.output(c.PIN_DI, dt.datetime.now().second % 2)
		sleep(1)
except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
gpio.cleanup()
