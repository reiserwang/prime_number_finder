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


def check_prime_chunk(chunk_range):
    """
    Checks a range of numbers for primality.
    Returns a list of primes found in the range.
    """
    start, end = chunk_range
    primes = []

    # Ensure start is odd
    if start % 2 == 0:
        start += 1

    for x in range(start, end, 2):
        # Optimization: skip multiples of 3 to avoid function call overhead
        if x % 3 == 0:
            continue
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

    # Divide the range (5, var) into chunks
    # Dynamic chunk size ensures utilization of all processes
    # while keeping chunks large enough to reduce IPC overhead.
    # We aim for at least 4 chunks per process if possible.
    total_items = var - 5
    if total_items < 0: total_items = 0

    # Minimum chunk size to justify overhead
    min_chunk = 10000

    # Calculate optimal chunk size
    # usage: total / (proc * 4) -> 4 batches per worker
    calculated_chunk = total_items // (proc * 4)
    chunk_size = max(min_chunk, calculated_chunk)

    chunks = []
    for i in range(5, var, chunk_size):
        chunks.append((i, min(i + chunk_size, var)))

    with Pool(processes=proc) as pool:
        # Map chunks to worker processes
        result_chunks = pool.map(check_prime_chunk, chunks)

    # Flatten the results
    for chunk in result_chunks:
        cleaned.extend(chunk)

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
