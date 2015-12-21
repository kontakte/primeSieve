import sys

results = []
lastResult = None

max = int(sys.argv[1])
sieve = []
for i in range(2,max):
  sieve.append(i)

while len(sieve) >= 1:
  lastResult = sieve[0]
  newSieve = []
  print("Sieving %d" % lastResult)
  for i in sieve:
    if i % lastResult != 0:
      newSieve.append(i)
  results.append(lastResult)
  sieve = newSieve

for i in results:
  print i
