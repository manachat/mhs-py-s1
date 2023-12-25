from multiprocessing.connection import Connection
import time
import multiprocessing as mp
import codecs
import sys
import datetime


def proc_a(a_dst, a_b_queue):
    while True:
        msg = a_dst.recv()
        a_b_queue.put(msg.lower())
        time.sleep(5)

def proc_b(a_b_queue, b_src):
    while True:
        msg = a_b_queue.get()
        b_src.send(codecs.encode(msg, 'rot_13'))


def main_process():

    a_dst, main_src = mp.Pipe(duplex=False)
    a_b_queue = mp.Queue()
    main_dst, b_src = mp.Pipe(duplex=False)
    child_a = mp.Process(target=proc_a, args=(a_dst, a_b_queue), daemon=True)
    child_b = mp.Process(target=proc_b, args=(a_b_queue, b_src), daemon=True)
    child_a.start()
    child_b.start()

    with open('artifacts/hw_4_3.txt', 'w') as log:
        start_time = time.time()
        for i, line in enumerate(sys.stdin):
            user_msg = line.strip()
            print(f'Sending msg {i}: {user_msg}')
            log.write(f'Elapsed {time.time() - start_time:.2f}s\tUser sent {i}:\t{user_msg}\n')
            main_src.send(user_msg)
            msg = main_dst.recv()
            print(f'Received msg {i}: {user_msg}')
            log.write(f'Elapsed {time.time() - start_time:.2f}s\tUser received {i}:\t{msg}\n')

        log.write(f'Elapsed {time.time() - start_time:.2f}s\tEnd of input')



def main():
    main_process()

if __name__ == '__main__':
    main()



