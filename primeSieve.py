import sys

STEP = 1000

results = []
lastResult = None

max = int(sys.argv[1])
sieve = []

lastMax = 2
currentMax = max if max < STEP else STEP

while currentMax <= max:
  print("Working on %d - %d" % (lastMax, currentMax))
  
  for i in range(lastMax,currentMax):
    sieve.append(i)

  print("Removing multiples of known primes")
  for prime in results:
    #print("Removing multiples of %d from sieve" % prime)
    newSieve = []
    for i in sieve:
      if i % prime != 0:
        newSieve.append(i)
    sieve = newSieve

  print("Sieving")
  while len(sieve) >= 1:
    lastResult = sieve[0]
    newSieve = []
    for i in sieve:
      if i % lastResult != 0:
        newSieve.append(i)
    results.append(lastResult)
    sieve = newSieve

  if currentMax == max:
    break
  
  lastMax = currentMax
  currentMax += STEP
  if currentMax > max:
    currentMax = max

#for i in results:
#  print i
