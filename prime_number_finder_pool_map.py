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


def check_prime(x):
    """
    Helper function for pool.map that returns the number if it is prime,
    or None if it is not. This avoids sending booleans back.
    """
    return x if is_prime(x) else None


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
    # We use chunksize to improve IPC performance.
    with Pool(processes=proc) as pool:
        # range(5, var, 2) covers all potential primes > 3
        # chunksize=1000 reduces IPC overhead significantly
        result = pool.map(check_prime, range(5, var, 2), chunksize=1000)

    # Filter out None values
    cleaned.extend(filter(None, result))
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
