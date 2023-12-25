import math
import concurrent.futures as cf
import multiprocessing
import functools
import time


def integrate_part(f, a, iter_start, iter_end, step):
    acc = 0
    for i in range(iter_start, iter_end):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000000, exec_type='thread'):
    acc = 0
    measure = 0
    step = (b - a) / n_iter
    if n_jobs > 1:
        iter_num = n_iter // n_jobs 
        
        parts = [(x*iter_num, min((x+1)*iter_num, n_iter)) for x in range(n_jobs)]
        if exec_type == 'thread':
            print(f'Start thread executor {n_jobs} jobs')
            with cf.ThreadPoolExecutor(max_workers=n_jobs) as executor:
                t_start = time.time()
                futures = [executor.submit(integrate_part, f, a, i1, i2, step) for i1, i2 in parts]
                acc = functools.reduce(lambda x, y: x + y, [f.result() for f in cf.as_completed(futures)])
                measure = time.time() - t_start 
        elif exec_type == 'process':
            print('Start process executor')
            with cf.ProcessPoolExecutor(max_workers=n_jobs) as executor:
                p_start = time.time()
                futures = [executor.submit(integrate_part, f, a, i1, i2, step) for i1, i2 in parts]
                acc = functools.reduce(lambda x, y: x + y, [f.result() for f in cf.as_completed(futures)])
                measure = time.time() - p_start # without pool setup overhead
        else:
            raise RuntimeError('Unknown processor ' + exec_type)
    else:
        s_start = time.time()
        acc = integrate_part(f, a, 0, n_iter, step)
        measure = time.time() - s_start
    
    return (acc, measure)



def main():
    cpu_num = multiprocessing.cpu_count()
    max_jobs = cpu_num * 2
    with open('artifacts/hw_4_2.txt', 'w') as f:
        for jobs in range(1, max_jobs + 1):
            f.write(f'{jobs} jobs\t')
            t_start = time.time()
            result, t_inn_res = integrate(math.cos, 0, math.pi / 2, n_jobs=jobs, exec_type='thread')
            t_res = time.time() - t_start
            f.write(f'Thread\t{t_res:.5}s\tInner\t{t_inn_res:.5}s\t{result:.7}\n')

            f.write('    \t')
            p_start = time.time()
            result, p_inn_res = integrate(math.cos, 0, math.pi / 2, n_jobs=jobs, exec_type='process')
            p_res = time.time() - p_start
            f.write(f'Process\t{p_res:.5}s\tInner\t{p_inn_res:.5}s\t{result:.7}\n')


if __name__ == '__main__':
    main()



