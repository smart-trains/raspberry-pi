import serial as s


def poll(addr, bytes_to_read):
	word = get_word('poll', addr)
	serial.write(bytearray([word]))
	data = serial.read(bytes_to_read)
	return validate_data(data)

def poll_and_next(bytes_to_read):
	poll(addr, bytes_to_read)
	inc_addr()

def validate_data(data):
	if not data:
		raise ValueError('NO DATA')
	elif data[0] != get_word('resp', addr):
		raise ValueError('INVALID RESPONSE')
	
	return data

def inc_addr():
	addr = addr + 1
	if addr == init_addr + num_dct:
		addr = 0b0001

def get_word(command, addr):
	return (ctrls[command] << 4) + addr

def serial_close():
	serial.close()


num_dct = 6
init_addr = 0b0001
period = 0.1/num_dct
brate = 51500 # Maximum rate due to slow n-MOSFET

ctrls = {
	'poll': 0b0101,
	'resp': 0b0100
}
addr = init_addr

serial = s.Serial(port='/dev/ttyAMA0', baudrate=51500, timeout=2*period)