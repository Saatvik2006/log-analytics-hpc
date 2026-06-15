from multiprocessing import Pool
import os
import time

def square(x):
    pid = os.getpid()

    print(f"Process {pid} started {x}")

    time.sleep(2)

    print(f"Process {pid} finished {x}")

    return x*x

if __name__ == "__main__":

    numbers = [1,2,3,4]

    with Pool(4) as pool:
        results = pool.map(square, numbers)

    print(results)