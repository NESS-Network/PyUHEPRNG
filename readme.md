# Py UHEPRNG
## UHEPRNG - Ultra High Entropy Pseudo-Random Number Generator

This is Steve Gibson's [UHEPRNG](https://www.grc.com/otg/uheprng.htm) adaptation to python 

### Running server
```
python server.py [directory]
```
Where *[directory]* is dir, where you want to store your files with random-generated data.
*[directory]* is optional, if no params, then current directory is used.
*Tmpfs* or other memory storage is recommended.

#### Four files will be generated:
1. seed.txt - seed of 256 random characters
2. seed-big.txt - seed of 1024 random characters
3. numbers.json - array of 100 random floating-point numbers
4. numbers-big.json - array of 1000 random floating-point numbers

Every second the seed and the numbers are regenerated.

### Running server with named pipe output
```
python pserver.py [pipeline file (default /tmp/random.pipeline)]
```
#### Redirecting output to /dev/random
```
python pserver.py /tmp/random.pipeline
rngd -r /tmp/random.pipeline -i
```
Need *rng-tools* package
### Random generator utility
```
python gen.py -s 555
```
Output random string 555 characters length

```
python gen.py -n 5
```
Output 5 random floating point numbers in JSON format

```
python gen.py -i256
```
Output random generated 256 bit integer which can be used in Ethereum
```
echo "w7ehfiulhf 4rh39fhuqh qfh9q4hfiuqfh fh9qfhiufhuiwrfhwfh" | python gen.py -s 555
```
Use pipeline to use custom initialisation data
### Seed generation utility
Seed utility generates same data from same seed.
Seed is accepted as pipeline input.

Usage:
```
seed.py <random data length in bytes (as more as better)>
```

Output to screen:
```
echo "quick brown fox jump over the lazy dog" | python seed.py 1024
```
Output to file:
```
echo "quick brown fox jump over the lazy dog" | python seed.py 1024 > my.key
```
### Pseudonames
```
./gen = python gen.py
./server = python server.py
./pserver = python pserver.py
./seed = python seed.py
```
### WEB interface
In `public` directory:

* print out seed.txt - index.php?s
* print out seed-big.txt - index.php?sb
* print out numbers.json - index.php?n
* print out numbers-big.json - index.php?nb
