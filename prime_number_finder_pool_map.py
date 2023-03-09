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


if __name__ == "__main__":
    cleaned = [2,3]
    var = int(input("Find prime numbers up to: "))
    proc = int(input("# of parallel worker processes: "))
    
    start = time.perf_counter()
    #we use a with statement to create the Pool object, which ensures that the pool is cleaned up properly after use.
    with Pool(processes=proc) as pool:
        result = pool.map(is_prime, range(5, var,6))

    for x in result:
        if x:
            cleaned.append(x)

    elapsed = time.perf_counter() - start
    print(cleaned)
    print("total prime numbers:", len(cleaned))
    print("run time:", elapsed)
