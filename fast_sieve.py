import heapq, math, profile, sqlite3, timeit

MAX_NUMBERS = 50


def old_sieve(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 2.0003080300002694
    # max_numbers = 5000; 1000 times; 29.907139191999704
    results = []
    lastResult = None
    sieve = []
    
    for i in range(2, max_numbers):
        sieve.append(i)

    for prime in results:
        newSieve = []
        for i in sieve:
            if i % prime != 0:
                newSieve.append(i)
            sieve = newSieve

    while len(sieve) >= 1:
        lastResult = sieve[0]
        newSieve = []
        for i in sieve:
            if i % lastResult != 0:
                newSieve.append(i)
            results.append(lastResult)
        sieve = newSieve

    return results


def range_generator(max_number):
    i = 0
    while i < max_number:
        yield i
        i += 1


def positional_sieve(max_numbers, max_check):
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


def better_positional_sieve(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.21832396400077414
    # max_numbers = 5000; 1000 times; 1.189540945000772
    numbers = [1 for i in range(max_numbers)]
    results = []
    for i, v in enumerate(numbers, 2):
        if v:
            results.append(i)
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = 0
                next_i += i
    return results


def positional_bool_sieve(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.25520653300009144
    # max_numbers = 5000; 1000 times; 2.664866823999546
    numbers = [True for i in range(max_numbers)]
    results = []
    for i in range(max_numbers):
        if i > 1 and numbers[i]:
            results.append(i)
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = False
                next_i += i

    return results


def positional_bool_sieve1_1(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.25520653300009144
    # max_numbers = 5000; 1000 times; 2.664866823999546
    numbers = [True for i in range(max_numbers)]
    results = [0,1]
    for i in range(2,max_numbers):
        if numbers[i]:
            results.append(i)
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = False
                next_i += i

    return results


def positional_bool_sieve2(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.3128934599999411
    # max_numbers = 5000; 1000 times; 3.275825315000475
    numbers = [True for i in range(max_numbers)]
    for i in range(len(numbers)):
        if i > 1 and numbers[i]:
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = False
                next_i += i

    return [i for i in range(len(numbers)) if i > 1 and numbers[i]]


def db_sieve(file_name, max_numbers, start_number=2):
    # Results:
    # :memory: max_numbers = 1000; 1000 times; 16.557492848000038
    # file max_numbers = 1000; 1000 times; 63.57015368400016
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS primes")
    cur.execute("CREATE TABLE primes (n number, is_prime boolean)")
    data = [(i, True) for i in range(2, max_numbers)]
    cur.executemany("INSERT INTO primes (n, is_prime) VALUES (?, ?)", data)
    i = start_number
    previous = -1
    while i <= max_numbers:
        previous = i
        cur.execute("UPDATE primes SET is_prime = ? WHERE is_prime = TRUE and n > ? and MOD(n, ?) = 0", (False, i, i))
        r = cur.execute("SELECT MIN(n) FROM primes WHERE is_prime = TRUE and n > ?", (i,)).fetchone()
        if r == None or r[0] == None:
            break
        else:
            i = r[0]
            if i <= previous:
                break
    results = [i[0] for i in cur.execute("SELECT n FROM primes WHERE is_prime = TRUE").fetchall()]
    cur.close()
    conn.close()
    return results


def db_sieve_wrapper(max_numbers, max_check):
    db_sieve("cheese.db", max_numbers)


def naive_primes(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.6541405450007005
    # max_numbers = 5000; 1000 times; 9.670261576000485
    primes = []
    for i in range(2, max_numbers):
        prime = True
        for p in primes:
            if i%p == 0:
                prime = False
                break
        if prime:
            primes.append(i)
    return primes


def better_naive_primes(max_numbers, max_check):
    # Results:
    # max_numbers = 1000; 1000 times; 0.6541405450007005
    # max_numbers = 5000; 1000 times; 9.670261576000485
    primes = []
    for i in range(2, max_numbers):
        prime = True
        for p in primes[:max_check]:
            if i%p == 0:
                prime = False
                break
        if prime:
            primes.append(i)
    return primes


def dijkstra_primes(max_numbers, max_check):
    pool = [[2,4]]
    primes = [2]
    sorted_pool = sorted(pool, key=lambda s: s[1])
    for i in range(3, max_numbers):
        if i < sorted_pool[0][1]:
            primes.append(i)
            pool.append([i, i*i])
        else:
            for s in sorted_pool:
                if i == s[1]:
                    s[1] += s[0]
                else:
                    break
            sorted_pool = sorted(pool, key=lambda s: s[1])
    return primes


def better_disjkstra(max_numbers, max_check):
    primes_pool = [(4, 2)]
    heapq.heapify(primes_pool)
    primes = [2]
    for i in range(3, max_numbers):
        while primes_pool[0][0] < i:
            multiple, prime = heapq.heappop(primes_pool)
            heapq.heappush(primes_pool, (multiple + prime, prime))
        if primes_pool[0][0] == i:
            multiple, prime = heapq.heappop(primes_pool)
            heapq.heappush(primes_pool, (multiple + prime, prime))
        else:
            primes.append(i)
            heapq.heappush(primes_pool, (i*i, i))
    return primes


def amazing_disjkstra(max_numbers, max_check):
    primes_pool = [2]
    multiple_pool = [4]
    primes = []
    min_multiple = 4
    for i in range(3, max_numbers):
        if min_multiple == i:
            for j in range(len(multiple_pool)):
                if multiple_pool[j] == min_multiple:
                    multiple_pool[j] += primes_pool[j]
            min_multiple = sorted(multiple_pool)[0]
        else:
            primes.append(i)
            primes_pool.append(i)
            multiple_pool.append(i*i)
    return primes


if __name__ == '__main__':
    #print(timeit.timeit(f"old_sieve({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import old_sieve", number=1000))
    #print(timeit.timeit(f"positional_sieve({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import positional_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import positional_bool_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve2({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import positional_bool_sieve2", number=1000))
    #print(timeit.timeit(f"db_sieve_wrapper({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import db_sieve_wrapper", number=1000))
    #print(timeit.timeit(f"naive_primes({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup="from __main__ import naive_primes", number=1000))

    functions = [
        #old_sieve,
        positional_sieve,
        better_positional_sieve,
        #dijkstra_primes,
        #better_disjkstra,
        #amazing_disjkstra,
        #positional_bool_sieve,
        #positional_bool_sieve2,
        #naive_primes,
        #positional_bool_sieve1_1,
        #better_naive_primes,
    ]

    function_times = []

    for f in functions:
        function_times.append((f.__name__, timeit.timeit(f"{f.__name__}({MAX_NUMBERS}, {int(math.sqrt(MAX_NUMBERS))})", setup=f"from __main__ import {f.__name__}", number=1000)))
    
    for i in sorted(function_times, key=lambda f: f[1]):
        print(f"{i[0]} - {i[1]}")

    print("results check")
    for f in functions:
        print(f"{f.__name__} = {len(f(MAX_NUMBERS, int(math.sqrt(MAX_NUMBERS))))}")
