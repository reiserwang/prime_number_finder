import math
import time
from multiprocessing import Pool

#The algorithm used here is called the "Sieve of Eratosthenes," which iteratively identifies prime numbers by eliminating multiples of known primes. 
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


def check_prime_range(range_tuple):
    """
    Helper function for pool.map that checks a range of numbers.
    Returns a list of primes found in the range.
    This reduces IPC overhead by returning batches of results.
    """
    start, end = range_tuple
    primes = []
    # Ensure we only check odd numbers
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

    # We check odd numbers starting from 5.
    # We use a larger chunk size (range) to process in each worker.
    # 10,000 is chosen as an optimal balance for IPC overhead vs load balancing.
    chunk_size = 10000
    ranges = []
    for i in range(5, var, chunk_size):
        end = min(i + chunk_size, var)
        ranges.append((i, end))

    with Pool(processes=proc) as pool:
        # Map the ranges to the workers
        results = pool.map(check_prime_range, ranges)

    # Flatten the results
    for batch in results:
        cleaned.extend(batch)

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
