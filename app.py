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

            dct_data = rs485.poll_and_next()

            print('time: {0}'.format(str(dt.now())))
            print('carriage: {0}'.format(dct_data.carriage__c))
            print('matrix: {data}'.format(data=dct_data.temperature_matrix))
            print('temp: {data}'.format(data=dct_data.temperature))
            print('humidity: {data}'.format(data=dct_data.humidity))
            print('vibration: {data}'.format(data=dct_data.temperature_matrix))

            server.report(dct_data)
        
            time_left = rs485.period - (time() - start_t)

            if time_left > 0:
                sleep(time_left)

        except ValueError as e:
            print(e)
            continue
        except IndexError as e:
            print(e)
            continue

        else:
            raise

except KeyboardInterrupt:
    pass

print("\n")
print("Gracefully exiting")
clean_up()
