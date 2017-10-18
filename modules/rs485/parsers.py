import struct


def parse_temperature_matrix(bytearray):
    message = {}

    for i, datum in enumerate(bytearray):
        if i == 0:
            message['thermistor__c'] = datum * 0.0625
        else:
            message['cell{index}__c'.format(index=(i - 1))] = datum * 0.25

    return message


def parse_temperature(bytearray):
    return {'temperature__c': struct.unpack('f', bytearray)}


def parse_humidity():
    return {'humidity__c': struct.unpack('f', bytearray)}


def parse_vibration():
    keys = [
        'acceleration_x__c',
        'acceleration_y__c',
        'acceleration_z__c',
        'gyro_x__c',
        'gyro_y__c',
        'gyro_z__c',
    ]
    message = {}

    bytes = ''
    for i, datum in enumerate(bytearray):
        if i % 2 == 0:
            bytes += datum
        else:
            bytes += datum
            message[keys[(i - 1) / 2]] = int.from_bytes(bytes, byteorder='big')

    return message
