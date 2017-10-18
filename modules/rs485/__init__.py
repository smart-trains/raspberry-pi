import serial as s
from datetime import datetime as dt
from raspberrypi.constants import carriage__c
from .parsers import (
    parse_temperature_matrix,
    parse_temperature,
    parse_humidity,
    parse_vibration,
)


num_dct = 6
# By using Arduino as fallback, we have 2 terminals representing one DCT
num_terminals = 12
init_address = 0b0001
period = 0.2 / num_terminals
brate = 50000  # Maximum rate: 51500 due to slow n-MOSFET

address = init_address

controls = {
    'poll': 0b0101,
    'resp': 0b0100,
    'end': 0xFF
}

sensors = {
    0x01: {
        'name': 'temperature_matrix',
        'bytes': 65,
        'parser': parse_temperature_matrix
    },
    0x02: {
        'name': 'temperature',
        'bytes': 4,
        'parser': parse_temperature
    },
    0x03: {
        'name': 'humidity',
        'bytes': 4,
        'parser': parse_humidity
    },
    0x04: {
        'name': 'vibration',
        'bytes': 12,
        'parser': parse_vibration
    },
}

# Mapping between internal address and carriage id
sub_dct_carriage_mapping = {
    0b0001: 0x00,
    0b0010: 0x00,
    0b0011: 0x01,
    0b0110: 0x01,
}

serial = s.Serial(port='/dev/ttyAMA0', baudrate=brate, timeout=3*period)


def poll(internal_address, parsed=True):
    print('address: {a}'.format(a=bin(internal_address)))
    word = get_word('poll', internal_address)
    serial.write(bytearray([word]))

    if internal_address == 0b0001:
        print(serial.read(68))
        raise IOError("SB dabanzi")

    head = serial.read()
    validate_head(head)

    result = {
        'address': internal_address
    }
    not_finished = True

    while not_finished:
        try:
            sensor_id = serial.read()[0]
        except IndexError:
            print('Last byte not detected')
            not_finished = False
            break

        if sensor_id == controls['end']:
            not_finished = False
        else:
            sensor = sensors[int(sensor_id)]
            data = serial.read(sensor['bytes'])
            result[sensor['name']] = data

    if parsed:
        return parse(result)

    return result


def poll_and_next(parsed=True):
    try:
        data = poll(address, parsed=parsed)
    except:
        raise
    finally:
        inc_address()

    return data


def validate_head(head):
    if not head:
        raise IOError('NO DATA')
    elif head[0] != get_word('resp', address):
        #  Clear other junk bytes
        serial.read(serial.in_waiting)
        raise IOError('INVALID RESPONSE HEAD: {head}'.format(head=bin(head[0])))

    return head


def inc_address():
    global address
    address = address + 1

    if address == init_address + num_terminals:
        address = 0b0001


def get_word(command, internal_address):
    return (controls[command] << 4) + internal_address


def parse(dct_data):
    internal_address = dct_data['address']

    message = {
        "carriage__c": carriage__c[sub_dct_carriage_mapping[internal_address]],
        "recorded_at__c": dt.now().isoformat(' '),
    }

    for _, sensor in sensors.items():
        try:
            name = sensor['name']
            message[name] = sensor['parser'](dct_data[name])
        except KeyError:
            pass

    return message


def serial_close():
    serial.close()
