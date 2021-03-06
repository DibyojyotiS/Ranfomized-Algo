import math
from queue import Queue
import random
import multiprocessing as mp
from csv import writer
from union_find_ADT import UnionFind
import matplotlib.pyplot as plt


def worker_naive(n,p,queue):
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i+1,n):
            if random.random()<p:
                uf.union(i,j)
    # find Snp and tally of sizes
    max_size = 1; sizes={}
    for size in uf.itter_sizes():
        if size not in sizes: sizes[size]=0
        sizes[size]+=1
        max_size = max(max_size, size)
    # return [p, max_size, uf.num_sets, sizes]
    queue.put([p, max_size, uf.num_sets, sizes])


def worker(n, p, queue):
    # ref: Batagelj V, Brandes U. Efficient generation of large random 
    # networks. Physical Review E. 2005 Mar 11;71(3):036113.
    # union-find to compute connected components 
    # while making the graph.
    uf = UnionFind(n)
    w = -1; v = 1
    lp = math.log(1.0 - p)
    while v < n:
        lr = math.log(1.0 - random.random())
        w = w + 1 + int(lr / lp)
        while w >= v and v < n:
            w = w - v
            v = v + 1
        if v < n:
            uf.union(v,w)
    
    # find Snp and tally of sizes
    max_size = 1; sizes={}
    for size in uf.itter_sizes():
        if size not in sizes: sizes[size]=0
        sizes[size]+=1
        max_size = max(max_size, size)
    # return [p, max_size, uf.num_sets, sizes]
    queue.put([p, max_size, uf.num_sets, sizes])
    

def watcher(queue:Queue, fname:str):
    with open(fname, 'w') as f:
        print('saving in', fname)
        csv_writer = writer(f)
        csv_writer.writerow(['p', 'max_size', 'num_components', 'sizes'])

        num_finished = 0
        while 1:
            m = queue.get()
            if m == 'kill':
                print('\nall done', flush=True)
                break
            csv_writer.writerow(m)
            f.flush()

            plt.scatter(m[0],m[1])
            plt.title('$S_{n,p}$ v/s $p$')
            plt.xlabel('$p$')
            plt.ylabel('$S_{n,p}$')
            plt.draw()
            plt.pause(0.00001)

            num_finished += 1
            print(f'\r {num_finished}', end = '', flush=True)
        plt.show()


if __name__ == '__main__':

    mp_manager = mp.Manager()
    queue = mp_manager.Queue()

    n = 1E7
    num_points = 40
    num_repeats = 20
    num_parallel = 20

    # vary p from (0, 2/n]
    fname = 'outputs.csv'
    probs = [2*(i+1)/(n*num_points) for i in range(num_points)]

    # vary p in 0.9/n to 1.1/n
    # fname = 'outputs-mid.csv'
    # probs = [0.9/n + 0.2*x/(n*(num_points-1)) for x in range(num_points)]

    num_parallel = min(num_parallel, num_repeats)
    pool =  mp.Pool(num_parallel)
    listener = pool.apply_async(watcher, (queue,fname))

    queue.put([0.0, 1, n, {1:n}]) # for p=0
    for p in probs:
        for r in range(0,num_repeats,num_parallel):

            jobs = []
            for i in range(num_parallel):
                job = pool.apply_async(worker, (int(n),p,queue))
                jobs.append(job)
            for job in jobs: 
                job.get()

    queue.put('kill')
    pool.close()
    pool.join()