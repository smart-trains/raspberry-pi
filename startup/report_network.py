from subprocess import check_output
from time import sleep
from datetime import datetime
import http.client as http
import json

from ..constants import train__c, server


_api = '/methods/lcu_status_insert'
_max_count = 500


def getssid():
    try:
        ssid = check_output(['iwgetid'])\
            .decode('utf-8')\
            .split('ESSID:')[1]\
            .translate(
            {ord(c): '' for c in '\n"'}
        )
        return ssid
    except:
        return None
    

def getip():
    try:
        ip = check_output(['hostname', '-I'])\
            .decode('utf-8')\
            .translate(
            {ord(c): '' for c in '\n '}
        )
        return ip
    except:
        return None


def test_internet():
    conn = http.HTTPConnection('www.google.com', timeout=2)
    result = False
    try:
        conn.request('HEAD', '/')
        result = True
    except:
        pass
    finally:
        conn.close()
    return result


def report_network(server, api):
    conn = http.HTTPConnection(server)
    headers = {'Content-type': 'application/json'}
    result = False
    try:
        data = {'ssid__c': getssid(),
                'ip__c': getip(),
                'recorded_at__c': datetime.now().isoformat(' '),
                'train__c': train__c
                }
        conn.request('POST', api, json.dumps(data), headers)
        result = True
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return result


if __name__ == '__main__':
    def try_until(func, max_trials, succ_cb, fail_cb, *args):
        _success = False
        _end_trying = False
        _count = 0

        while not _end_trying:
            if func(*args):
                succ_cb(_count)
                _end_trying = True
                _success = True
            else:
                fail_cb(_count)
                if _count >= max_trials:
                    _end_trying = True
                else:
                    sleep(1)
                    _count += 1

        return _success

    _connected = try_until(
        test_internet,
        _max_count,
        lambda c: print('attempt internet connection successful, attempt {0}'.format(c)),
        lambda c: print('attempt internet connection failed, attempt {0}'.format(c))
    )

    if (_connected):
        try_until(
            report_network,
            _max_count,
            lambda c: print('report to {0} successful, attempt {1}'.format(server, c)),
            lambda c: print('report to {0} failed, attempt {1}'.format(server, c)),
            server, _api
        )
