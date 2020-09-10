import math,time
from multiprocessing import Pool

def isPrime(x):
    if x <2:
        return 0
    if x==2:
        return x
    else:
        for div in range(2,int(math.sqrt(x) +1)):
        if ((x % div) ==0):
            return 0
    return x


if __name__ == '__main__':
    cleaned=[]
    var = input("Find prime numbers up to: ")
    proc=input("# of parallel worker processes:")
    start = time.clock()
    pool= Pool(processes=proc)
    result =  pool.map(isPrime, range(2,int(var)))
    for x in result:
        if x<>0:
        cleaned.append(x)

    elapsed = (time.clock()-start)
    print cleaned
    print ('total prime numbers:',len(cleaned)) 
    print ('run time:',elapsed)