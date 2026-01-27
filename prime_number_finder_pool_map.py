import math
import time
from multiprocessing import Pool

# The algorithm used here is trial division, optimized to skip multiples of 2 and 3.
def is_prime(x):
    if x < 2:
        return False
    elif x == 2 or x == 3:
        return True
    elif x % 2 == 0 or x % 3 == 0:
        return False
    else:
        for i in range(5, int(math.sqrt(x)) + 1, 6):
            if x % i == 0 or x % (i + 2) == 0:
                return False
        return True


def get_primes_in_range(r):
    """
    Worker function that checks a range of numbers and returns a list of primes.
    This runs in the worker process and filters locally to minimize IPC.
    """
    return [x for x in r if is_prime(x)]


def find_primes(var, proc):
    """
    Finds prime numbers up to 'var' using 'proc' parallel processes.
    """
    cleaned = []
    if var > 2:
        cleaned.append(2)
    if var > 3:
        cleaned.append(3)

    # We check odd numbers starting from 5.
    full_range = range(5, var, 2)

    # Process in chunks to reduce IPC overhead.
    # Instead of sending every number as a separate task item or returning None for non-primes,
    # we send a range object (lightweight) and return a list of valid primes (efficient).
    chunk_len = 10000
    chunks = [full_range[i:i + chunk_len] for i in range(0, len(full_range), chunk_len)]

    with Pool(processes=proc) as pool:
        result_lists = pool.map(get_primes_in_range, chunks)

    for res in result_lists:
        cleaned.extend(res)

    return cleaned


if __name__ == "__main__":
    var = int(input("Find prime numbers up to: "))
    proc = int(input("# of parallel worker processes: "))
    
    start = time.perf_counter()

    primes = find_primes(var, proc)

    elapsed = time.perf_counter() - start
    print(primes)
    print("total prime numbers:", len(primes))
    print("run time:", elapsed)
