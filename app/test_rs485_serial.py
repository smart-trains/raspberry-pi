import serial
import RPi.GPIO as gpio
from time import sleep, time
from datetime import datetime as dt

num_dct = 6
init_addr = 0b0001
period = 0.1/num_dct

s = serial.Serial(port="/dev/ttyAMA0", baudrate=38400, timeout=period/2)

ctrl = 0b0101
resp = 0b0100
addr = init_addr

try:
    while True:
        start_t = time()

        word = (ctrl << 4) + addr
        s.write(bytearray([word]))

        start_wait_t = time()
        while s.in_waiting < 66:
            if time() - start_wait_t > period:
                break

        data = s.read(66)
        print('time: {0}'.format(str(dt.now())))
        print('word: {0}'.format(bin(word)))

        if not data:
            print('NO DATA')
        elif data[0] != (resp << 4) + addr:
            print('INVALID RESPONSE')
        else:
            for i, datum in enumerate(data):
                if i == 0:
                    print('resp word: {0}'.format(bin(datum)))
                elif i == 1:
                    print('env temp: {0}'.format(str(datum * 0.0625)))
                else:
                    if (i-1) % 8 == 0:
                        ending = None
                    else:
                        ending = ''
                    print('sensor {0}: {1} '.format(str(i - 2), str(datum * 0.25)), end=ending)
        print('')

        addr = addr + 1
        if addr == init_addr + num_dct:
            addr = 0b0001
        time_left = period - (time() - start_t)

        if time_left > 0:
            sleep(time_left)

except ValueError:
    pass


print("\n")
print("Gracefully exiting")
#gpio.cleanup()
s.close()
