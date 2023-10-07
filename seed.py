import lib.prng as prng
import json
import sys
import os
import base64
from base64 import b64encode
from base64 import b64decode

if len(sys.argv) == 2:

    is_pipeline = ( sys.stdin.readable() and (not sys.stdin.isatty()) )
    is_file = ( sys.stdout.writable() and (not sys.stdout.isatty()) )

    if is_pipeline:
        seed = sys.stdin.read()
    else:
        if is_file:
            sys.stdout.close()
            quit(1)

        print ("Enter seed:")
        seed = sys.stdin.readline()

    generator = prng.UhePrng()
    generator.init_state()
    generator.hash_string(seed)
    string = generator.string(int(sys.argv[1]))

    print (string)
else:
    print ('seed.py <random data length in bytes (as more as better)>')
    print ('Take seed from pipeline and save random generated data to file:')
    print ('echo "quick brown fox jump over the lazy dog" | python seed.py 1024 > my.key')
    print ('Another variant:')
    print ('cat seed.txt | python seed.py 1024 > my.key')