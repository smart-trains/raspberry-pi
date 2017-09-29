from time import time
import http.client as http
import json


def get_message(addr, data):
    msg = {
        "address": addr,
        "datetime": time() * 1000
    }

    for i, datum in enumerate(data):
        if i == 0:
            print('resp word: {0}'.format(bin(datum)))
        elif i == 1:
            print('env temp: {0}'.format(str(datum * 0.0625)))
            msg["temp"] = datum * 0.0625
        else:
            if (i-1) % 8 == 0:
                ending = None
            else:
                ending = ''
        
        print('sensor {0}: {1} '.format(str(i - 2), str(datum * 0.25)), end=ending)
        print('')
        msg["cell" + str(i - 2)] = datum * 0.25

def report_temp(server = _server, api = _api, data):
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


_server = "smart-trains.herokuapp.com"
_api = "/DctIr"