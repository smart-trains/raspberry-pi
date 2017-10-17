from time import sleep, time
from datetime import datetime as dt
from raspberrypi.modules import rs485, server


def clean_up():
    rs485.serial_close()


running = True

try:
    while running:
        try:
            start_t = time()

            print('time: {0}'.format(str(dt.now())))
            print('word: {0}'.format(bin(rs485.get_word('poll', rs485.addr))))

            dct_data = rs485.poll_and_next()
            server.report(dct_data)
        
            time_left = rs485.period - (time() - start_t)

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
clean_up()
