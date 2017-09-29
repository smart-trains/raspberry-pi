from time import sleep, time
from datetime import datetime as dt
from modules import rs485, server

running = True

try:
    while running:
        try:
            start_t = time()

            print('time: {0}'.format(str(dt.now())))
            print('word: {0}'.format(bin(rs485.get_word('poll', rs485.addr))))

            data = rs485.poll_and_next(66)
        
            server.report_temp(_server, _api, server.get_message(rs485.addr ,data))
        
            time_left = period - (time() - start_t)

            if time_left > 0:
                sleep(time_left)

        except ValueError as e:
            print(e)
            continue

        else:
            raise

except KeyboardInterrupt:
    pass

print("\n")
print("Gracefully exiting")
rs485.serial_close()
