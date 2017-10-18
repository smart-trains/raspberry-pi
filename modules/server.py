import http.client as http
import json

from raspberrypi.constants import server as _server


_api = '/methods/data_insert'


def report(data):
    conn = http.HTTPConnection(_server)
    headers = {'Content-type': 'application/json'}
    result = False
    try:
        conn.request("POST", _api, json.dumps(data), headers)
        result = True
    except:
        pass
    finally:
        conn.close()
    return result


