import serial
import RPi.GPIO as gpio
from time import sleep, time
from datetime import datetime as dt
import http.client as http
import json


def report_temp(server, api, data):
    conn = http.HTTPConnection(server)
    headers = {'Content-type': 'application/json'}
    result = False
    try:
        conn.request("POST", api, json.dumps(data), headers)
        result = True
    except:
        pass
    finally:
        conn.close()
    return result

_server = "52.65.244.105"
_api = "/DctIr"

num_dct = 6
init_addr = 0b0001
period = 0.1/num_dct

s = serial.Serial(port="/dev/ttyAMA0", baudrate=51500, timeout=2*period)

ctrl = 0b0101
resp = 0b0100
addr = init_addr

try:
    while True:
        start_t = time()

        word = (ctrl << 4) + addr
        s.write(bytearray([word]))

        data = s.read(66)
        print('time: {0}'.format(str(dt.now())))
        print('word: {0}'.format(bin(word)))

        if not data:
            print('NO DATA')
        elif data[0] != (resp << 4) + addr:
            print('INVALID RESPONSE')
        else:
            json = {
                "address": addr,
                "datetime": time() * 1000
            }

            for i, datum in enumerate(data):
                if i == 0:
                    print('resp word: {0}'.format(bin(datum)))
                elif i == 1:
                    print('env temp: {0}'.format(str(datum * 0.0625)))
                    json["temp"] = datum * 0.0625
                else:
                    if (i-1) % 8 == 0:
                        ending = None
                    else:
                        ending = ''
                    print('sensor {0}: {1} '.format(str(i - 2), str(datum * 0.25)), end=ending)
                    json["cell" + str(i - 2)] = datum * 0.25
        print('')
        report_temp(_server, _api, json)

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
