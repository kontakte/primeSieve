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


def setup_tables(file_name, max_numbers):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute("CREATE TABLE primes (n number, is_prime boolean)")
    data = [(i, True) for i in range(2, max_numbers)]
    cur.executemany("INSERT INTO primes (n, is_prime) VALUES (?, ?)", data)
    conn.commit()
    cur.close()
    conn.close()


def db_sieve(file_name, max_numbers, start_number=2):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    i = start_number
    while i <= max_numbers:
        cur.execute("UPDATE primes SET is_prime = ? WHERE is_prime = TRUE and n > ? and MOD(n, ?) = 0", (False, i, i))
        r = cur.execute("SELECT MIN(n) FROM primes WHERE is_prime = TRUE and n > ?", (i,)).fetchone()
        if r == None or r[0] == None:
            break
        else:
            i = r[0]
    results = [i[0] for i in cur.execute("SELECT n FROM primes WHERE is_prime = TRUE").fetchall()]
    cur.close()
    conn.commit()
    conn.close()
    return results


if __name__ == '__main__':
    #print(timeit.timeit(f"old_sieve({MAX_NUMBERS})", setup="from __main__ import old_sieve", number=1000))
    #print(timeit.timeit(f"positional_sieve({MAX_NUMBERS})", setup="from __main__ import positional_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve({MAX_NUMBERS})", setup="from __main__ import positional_bool_sieve", number=1000))
    #print(timeit.timeit(f"positional_bool_sieve2({MAX_NUMBERS})", setup="from __main__ import positional_bool_sieve2", number=1000))
    
    #profile.run('positional_sieve(10000)')
    #profile.run('positional_bool_sieve(10000)')
    #profile.run('positional_bool_sieve2(10000)')

    setup_tables("blah.db", 1000000)
    print(db_sieve("blah.db", 1000000))
