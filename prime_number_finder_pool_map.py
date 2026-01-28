import math
import time
from multiprocessing import Pool

# The algorithm used here is actually Trial Division.
def is_prime(x):
    """
    Checks if a number is prime.
    Kept for reference and testing, though inlined in worker for performance.
    """
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


def find_primes_in_range(start, end):
    """
    Finds prime numbers in the range [start, end).
    Optimized to only check odd numbers and inline the primality check
    to avoid function call overhead.
    """
    primes = []
    # Ensure we start at an odd number
    if start % 2 == 0:
        start += 1

    for x in range(start, end, 2):
        # Inline optimization of is_prime logic
        # We know x >= 5 and x is odd.

        if x % 3 == 0:
            continue

        limit = int(math.sqrt(x)) + 1
        is_p = True
        for i in range(5, limit, 6):
            if x % i == 0 or x % (i + 2) == 0:
                is_p = False
                break

        if is_p:
            primes.append(x)
    return primes


def find_primes(var, proc):
    """
    Finds prime numbers up to 'var' using 'proc' parallel processes.
    Optimized to process ranges in workers and use inlined checks.
    """
    cleaned = []
    if var > 2:
        cleaned.append(2)
    if var > 3:
        cleaned.append(3)

    if var <= 5:
        return cleaned

    # Create ranges to be processed by workers.
    # Chunk size of 10,000 provides a good balance:
    # - Large enough to reduce IPC overhead (passing ranges vs individual numbers).
    # - Small enough to ensure good load balancing across workers (since larger numbers take longer to check).
    chunk_size = 10000
    ranges = []
    for i in range(5, var, chunk_size):
        ranges.append((i, min(i + chunk_size, var)))

    with Pool(processes=proc) as pool:
        results = pool.starmap(find_primes_in_range, ranges)

    for result in results:
        cleaned.extend(result)

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
