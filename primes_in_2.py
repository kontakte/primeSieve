def positional_sieve(max_numbers):
    # Results:
    # max_numbers = 1000; 1000 times; 0.21832396400077414
    # max_numbers = 5000; 1000 times; 1.189540945000772
    numbers = [i for i in range(max_numbers)]
    results = []
    for i in numbers:
        if i > 1:
            results.append(i)
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = 0
                next_i += i

    return results

counts = {}
total = 0

previous = 1
for p in positional_sieve(1000000000):
    d = p - previous
    counts[d] = counts.get(d,0) + 1
    previous = p
    total += 1

for k in sorted(counts.keys()):
    print(f"{k}: {counts[k]}")

print(total)
