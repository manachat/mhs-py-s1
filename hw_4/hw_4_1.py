import time
import threading as th
import multiprocessing as mp

import re

fib_count = 30


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def start_thread():
    t = th.Thread(target=fib, args=(fib_count, ))
    t.start()
    return t

def start_process():
    p = mp.Process(target=fib, args=(fib_count, ))
    p.start()
    return p

def main():
    
    parallelism = 10
    print('Start sync')
    sync_start = time.time()
    [fib(30) for _ in range(10)]
    sync_res = time.time() - sync_start
    
    print('Start threads')
    threads_start = time.time()
    threads = [start_thread() for _ in range(parallelism)]
    [t.join() for t in threads]
    threads_res = time.time() - threads_start

    print('Start procs')
    multi_start = time.time()
    procs = [start_process() for _ in range(parallelism)]
    [p.join() for p in procs]
    multi_res = time.time() - multi_start
    
    with open('artifacts/4_1.txt', 'w') as f:
        f.write(f'Sync execution: \t{sync_res:.4}s\n')
        f.write(f'Thread execution: \t{threads_res:.4}s\n')
        f.write(f'Proc execution: \t{multi_res:.4}s\n')


if __name__ == '__main__':
    main()
