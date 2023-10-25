import profile, sqlite3, timeit

MAX_NUMBERS = 5000

def old_sieve(max_numbers):
    # Results:
    # max_numbers = 1000; 1000 times; 2.0003080300002694
    # max_numbers = 5000; 1000 times; 29.907139191999704
    results = []
    lastResult = None
    sieve = []
    
    for i in range(2,max_numbers):
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


def positional_bool_sieve(max_numbers):
    # Results:
    # max_numbers = 1000; 1000 times; 0.25520653300009144
    # max_numbers = 5000; 1000 times; 2.664866823999546
    numbers = [True for i in range(max_numbers)]
    results = []
    for i in range(len(numbers)):
        if i > 1 and numbers[i]:
            results.append(i)
            next_i = i + i
            while next_i < max_numbers:
                numbers[next_i] = False
                next_i += i

    return results


def positional_bool_sieve2(max_numbers):
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


def db_sieve_wrapper(max_numbers):
    db_sieve("cheese.db", max_numbers)


def naive_primes(max_numbers):
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


if __name__ == '__main__':
    #print(timeit.timeit(f"old_sieve({MAX_NUMBERS})", setup="from __main__ import old_sieve", number=1000))
    #print(timeit.timeit(f"positional_sieve({MAX_NUMBERS})", setup="from __main__ import positional_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve({MAX_NUMBERS})", setup="from __main__ import positional_bool_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve2({MAX_NUMBERS})", setup="from __main__ import positional_bool_sieve2", number=1000))
    #print(timeit.timeit(f"db_sieve_wrapper({MAX_NUMBERS})", setup="from __main__ import db_sieve_wrapper", number=1000))
    print(timeit.timeit(f"naive_primes({MAX_NUMBERS})", setup="from __main__ import naive_primes", number=1000))

    #profile.run('positional_sieve(10000)')
    #profile.run('positional_bool_sieve(10000)')
    #profile.run('positional_bool_sieve2(10000)')

    
