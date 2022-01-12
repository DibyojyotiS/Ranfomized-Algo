# timer for benchmarking
import sys
import json
from numpy.random import uniform # rnd generator
from time import perf_counter_ns as timer

from deterministic_algos import QuickSort, MergeSort
from randomied_algos import RandomizedQuickSort

# question-1
# Randomized Quick-Sort v/s Quick-Sort
def Qusetion1():

    sys.setrecursionlimit(10**7)

    def generate_randomlist(n=10E6):
        n = int(n)
        # rand_list = [uniform(0,1) for x in range(n)]
        rand_list = uniform(0,1,n).tolist()
        return rand_list

    def time_single_sort(sortingAlgo, arr):
        t1 = timer()
        _, numcomparisons = sortingAlgo(arr)
        t2 = timer()
        return numcomparisons, t2-t1 # in nano-seconds

    def time_double_sort(sortingAlgo, arr):
        t1 = timer()
        sortingAlgo(arr)
        sortingAlgo(arr)
        t2 = timer()
        return t2-t1 # in nano-seconds    

    def incrementCounter(counter, data):
        for i,d in enumerate(data):
            counter[i] += d
        return  

    def runExperiemnt(sortingAlgo, list_n, K):
        # will run experiments for the following list of n
        # each experiemnt will be repeated about K times

        print('running for', sortingAlgo.__name__)
        
        avgtimes = []
        # get sorting times
        for n in list_n:
            arr = generate_randomlist(n) 
            print(n)
            # accumulators
            counters = [0,0,0] #conparisons, single_t, double_t
            # run K times 
            for k in range(K):
                # for deterministc-quicksort
                numcomparisons, single_sort_t = time_single_sort(sortingAlgo, arr)
                double_sort_t = time_double_sort(sortingAlgo, arr)
                incrementCounter(counters, 
                                (numcomparisons/K, single_sort_t/K, double_sort_t/K))

            avgtimes.append(counters)
        return avgtimes

    # print results
    list_n = [10**x for x in range(2,5)]
    avgtimes_QuickSort = runExperiemnt(QuickSort, list_n, K=500)
    print(avgtimes_QuickSort)

    list_n = [10**x for x in range(2,7)]
    avgtimes_RandomizedQuickSort = runExperiemnt(RandomizedQuickSort, list_n, K=500)
    print(avgtimes_RandomizedQuickSort)

    # save stuffs
    data = {'avgtimes_QuickSort': avgtimes_QuickSort,
            'avgtimes_RandomizedQuickSort': avgtimes_RandomizedQuickSort}
    with open('save.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    Qusetion1()