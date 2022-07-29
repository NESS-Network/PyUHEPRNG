import lib.prng as prng
import json
import sys
from base64 import b64encode
from base64 import b64decode
import uuid

if len(sys.argv) == 3:
    arg = sys.argv[1]
    cnt = int(sys.argv[2])

    generator = prng.UhePrng()

    for i in range (0, 9):
        rand = ''
        with open('/dev/random', 'rb') as file:
            rand = b64encode(file.read(1024)).decode('utf-8')
            file.close()

        generator.add_entropy(rand, str(uuid.getnode()))

    if arg == '-s' or arg == '-seed':
        if cnt < 256:
            cnt = 256
        print(generator.string(cnt))

        quit()
    elif arg == '-n' or arg == '-numbers':
        cnt += 1
        if cnt < 1:
            cnt = 1
        seed = generator.string(1024)
        numbers = generator.generate(0, cnt)
        numbers = json.dumps(numbers)
        print(numbers)

        quit()
elif len(sys.argv) == 2:
    arg = sys.argv[1]

    generator = prng.UhePrng()

    for i in range (0, 99):
        rand = ''
        with open('/dev/random', 'rb') as file:
            rand = b64encode(file.read(1024)).decode('utf-8')
            file.close()

        generator.add_entropy(rand, str(uuid.getnode()))

    if arg == '-h256' or arg == '-i256':
        seed = generator.string(1024)
        numbers = generator.generate(0, 17)

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

        quit()

print('Usage')
print('prng.py -s <length> or prng.py --seed  <length> display the random generated seed')
print('Usage prng.py -n <count> or prng.py --numbers <count> display the random generated numbers')
print('Usage prng.py -i256 or prng.py -h256 show random generated 256 bit integer which can be used in Ethereum')
