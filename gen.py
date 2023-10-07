import signal

halt = False


def exit_fn (*args):
    global halt
    halt = True


signal.signal(signal.SIGINT, exit_fn)
signal.signal(signal.SIGTERM, exit_fn)

import lib.prng as prng
import json
import sys
import os
import base64
from base64 import b64encode
from base64 import b64decode
import uuid

is_pipeline = ( sys.stdin.readable() and (not sys.stdin.isatty()) )

if is_pipeline:
    randomdata = b64encode(bytes(sys.stdin.read(), 'utf-8')).decode('utf-8')
else:
    with open('/dev/random', 'rb') as file:
        rand = file.read(1024)
        randomdata = b64encode(rand).decode('utf-8')
        file.close()

if len(sys.argv) == 3:
    arg = sys.argv[1]
    cnt = int(sys.argv[2])

    generator = prng.UhePrng()

    generator.add_entropy(randomdata, uuid.getnode())

    if arg == '-s' or arg == '-string':
        if cnt < 256:
            cnt = 256
        print(generator.string(cnt))

        if halt:
            quit(1)
            
        else:
            quit()
    elif arg == '-n' or arg == '-numbers':
        cnt += 1
        if cnt < 1:
            cnt = 1
        seed = generator.string(1024)
        numbers = generator.generate(0, cnt)
        numbers = json.dumps(numbers)
        print(numbers)

        if halt:
            quit(1)
        else:
            quit()
elif len(sys.argv) == 2:
    arg = sys.argv[1]

    generator = prng.UhePrng()

    generator.add_entropy(randomdata, uuid.getnode())

    if arg == '-h256' or arg == '-i256':
        seed = generator.string(1024)
        numbers = generator.generate(0, 8)

        module = 1 << 32
        i256 = 0

        for i in range (0, 7):
            num = int(numbers[i] * 10e16)
            num = num << (32 * i)
            i256 += num

        if arg == '-i256':
            print(i256)
        if arg == '-h256':
            print(hex(i256))

        if halt:
            quit(1)
        else:
            quit()



print('Usage')
print('prng.py -s <length> or prng.py --string  <length> display the random generated string')
print('Usage prng.py -n <count> or prng.py --numbers <count> display the random generated numbers')
print('Usage prng.py -i256 or prng.py -h256 show random generated 256 bit integer which can be used in Ethereum')
