import serial
import RPi.GPIO as gpio
from time import sleep, time
from datetime import datetime as dt

period = 0.1/6

s = serial.Serial(port="/dev/ttyAMA0", baudrate=38400, timeout=period/2)

ctrl = 0b01010001

try:
	while True:
		start_t = time()
		s.write(bytearray([ctrl]))
		start_wait_t = time()
		while(not s.in_waiting):
			if(time() - start_wait_t > period):
				break
		data = s.read(66)
		print('time: {0}'.format(str(dt.now())))

		if not data:
			print('ctrl: {0}'.format(bin(ctrl)))
			print('NO DATA')
		else:		
			for i, datum in enumerate(data):
				if i == 0:
					print('resp ctrl: {0}'.format(bin(datum)))
				elif i == 1:
					print('env temp: {0}'.format(str(datum * 0.0625)))
				else:
					if (i-1) % 8 == 0:
						end = None
					else:
						end = ''
					print('sensor {0}: {1} '.format(str(i-2), str(datum * 0.25)), end=end)
		print('')
		ctrl = ctrl + 1
		if ctrl > 0b01010110:
			ctrl = 0b01010001
		time_left = period - (time() - start_t)
		
		if time_left > 0:
			sleep(time_left)

except KeyboardInterrupt:
	pass

print("\n")
print("Gracefully exiting")
#gpio.cleanup()
s.close()
