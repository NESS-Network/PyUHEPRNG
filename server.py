import lib.prng as prng
import json
import sys
import os
import signal
import time
from base64 import b64encode
from base64 import b64decode
import uuid

halt = False


def exit_fn (*args):
    global halt
    halt = True


signal.signal(signal.SIGINT, exit_fn)
signal.signal(signal.SIGTERM, exit_fn)

generator = prng.UhePrng()



directory = ''

if len(sys.argv) >= 2:
    directory = sys.argv[1]

if directory != '':
    if not os.path.exists(directory):
        print('Directory ' + directory + ' does not exist')
        exit(1)
    else:
        directory += os.path.sep
else:
    directory = os.path.sep + 'tmp' + os.path.sep

while True:
    # print('.')

    rand = ''
    with open('/dev/random', 'rb') as file:
        rand = b64encode(file.read(1024)).decode('utf-8')
        file.close()

    generator.add_entropy(rand, str(uuid.getnode()))
    seed = generator.string(256)

    with open(directory + 'seed.txt', 'w+') as file:
        file.seek(0)
        file.write(seed)
        file.truncate()
        file.close()

    numbers = generator.generate(0, 100)
    numbers = json.dumps(numbers)
    # print(numbers)

    with open(directory + 'numbers.json', 'w+') as file:
        file.seek(0)
        file.write(numbers)
        file.truncate()
        file.close()

    rand = ''
    with open('/dev/random', 'rb') as file:
        rand = b64encode(file.read(1024)).decode('utf-8')
        file.close()

    generator.add_entropy(rand, str(uuid.getnode()))
    seed = generator.string(1024)
    # print(seed)

    with open(directory + 'seed-big.txt', 'w+') as file:
        file.seek(0)
        file.write(seed)
        file.truncate()
        file.close()
        file.close()

    numbers = generator.generate(0, 1024)
    numbers = json.dumps(numbers)


    with open(directory + 'numbers-big.json', 'w+') as file:
        file.seek(0)
        file.write(numbers)
        file.truncate()
        file.close()


    seed = generator.string(1024)
    numbers = generator.generate(0, 8*16)
    numbersi256 = []
    numbersh256 = []

    module = 1 << 32

    for x in range (0, 15):
        i256 = 0

        for i in range (0, 7):
            num = int(numbers[x*8 + i] * 10e16)
            num = num << (32 * i)
            i256 += num

        numbersi256.append(i256)
        numbersh256.append(hex(i256))

    numbersi256 = json.dumps(numbersi256)
    numbersh256 = json.dumps(numbersh256)

    with open(directory + 'i256.json', 'w+') as file:
        file.seek(0)
        file.write(numbersi256)
        file.truncate()
        file.close()

    with open(directory + 'h256.json', 'w+') as file:
        file.seek(0)
        file.write(numbersh256)
        file.truncate()
        file.close()

    # print('.')

    if halt:
        print()
        print('Process stopped by signal')
        break

    time.sleep(1)
