from time import sleep, time
from raspberrypi.modules import rs485, server


def clean_up():
    rs485.serial_close()


running = True

try:
    while running:
        try:
            start_t = time()

            dct_data = rs485.poll_and_next()

            print(dct_data)

            server.report(dct_data)
        
            time_left = rs485.period - (time() - start_t)

            if time_left > 0:
                sleep(time_left)

        except IOError as e:
            print(e)
            continue

        except KeyError as e:
            continue

        except:
            raise

except KeyboardInterrupt:
    pass

print("\n")
print("Gracefully exiting")
clean_up()
