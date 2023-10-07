from base64 import b64encode
import sys

if len(sys.argv) == 2:
    rand = ''
    with open('/dev/random', 'rb') as file:
        rand = file.read(int(sys.argv[1]))
        file.close()

    print (b64encode(rand).decode('utf-8'))
else:
    print ('python r.py <bytes to read from /dev/random>')
