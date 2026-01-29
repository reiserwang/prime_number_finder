import math
import time
from multiprocessing import Pool

# The algorithm used here is called the "Sieve of Eratosthenes," which iteratively identifies prime numbers by eliminating multiples of known primes.
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


def check_prime(x):
    """
    Helper function for pool.map that returns the number if it is prime,
    or None if it is not. This avoids sending booleans back.
    """
    return x if is_prime(x) else None


def check_prime_range(range_tuple):
    """
    Worker function that finds primes in a given range.
    Optimizes performance by:
    1. Reducing function call overhead (called once per chunk, not per number).
    2. Reducing IPC overhead (returns list of primes, not individual results).
    """
    start, end = range_tuple
    primes = []
    # Ensure we start on an odd number if start is even
    if start % 2 == 0:
        start += 1

    for x in range(start, end, 2):
        if is_prime(x):
            primes.append(x)
    return primes


def find_primes(var, proc):
    """
    Finds prime numbers up to 'var' using 'proc' parallel processes.
    """
    cleaned = []
    if var > 2:
        cleaned.append(2)
    if var > 3:
        cleaned.append(3)

    # We use a chunk size of 10,000 for range-based processing.
    # Benchmarks showed this to be the optimal size:
    # - Too small (e.g. 1000) -> Overhead dominates
    # - Too large (e.g. 100000) -> Load balancing issues (uneven work)
    chunk_size = 10000
    ranges = []
    for i in range(5, var, chunk_size):
        end = min(i + chunk_size, var)
        ranges.append((i, end))

    with Pool(processes=proc) as pool:
        # Instead of mapping over individual numbers, we map over ranges.
        result = pool.map(check_prime_range, ranges)

    # Flatten the list of lists
    for sublist in result:
        cleaned.extend(sublist)

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
