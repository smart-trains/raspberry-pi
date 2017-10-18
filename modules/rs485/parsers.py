import struct


def parse_temperature_matrix(data):
    message = {}

    for i, datum in enumerate(data):
        if i == 0:
            message['thermistor__c'] = datum * 0.0625
        else:
            message['cell{index}__c'.format(index=(i - 1))] = datum * 0.25

    return message


def parse_temperature(data):
    return {'temperature__c': struct.unpack('f', data)}


def parse_humidity(data):
    return {'humidity__c': struct.unpack('f', data)}


def parse_vibration(data):
    keys = [
        'acceleration_x__c',
        'acceleration_y__c',
        'acceleration_z__c',
        'gyro_x__c',
        'gyro_y__c',
        'gyro_z__c',
    ]
    message = {}

    byte_sequence = ''
    for i, datum in enumerate(data):
        if i % 2 == 0:
            byte_sequence += datum
        else:
            byte_sequence += datum
            message[keys[(i - 1) / 2]] = int.from_bytes(byte_sequence, byteorder='big')

    return message
