# timer for benchmarking
from random import uniform # rnd generator
from time import perf_counter_ns as timer

from deterministic_algos import QuickSort, MergeSort
from randomied_algos import RandomizedQuickSort

# question-1
# Randomized Quick-Sort v/s Quick-Sort
def Qusetion1():

    def generate_randomlist(n=10E6):
        n = int(n)
        rand_list = [uniform(0,1) for x in range(n)]
        return rand_list

    def time_single_sort(sortingAlgo, arr):
        t1 = timer()
        sortingAlgo(arr)
        t2 = timer()
        return t1-t2 # in nano-seconds

    def time_double_sort(sortingAlgo, arr):
        t1 = timer()
        sortingAlgo(arr)
        sortingAlgo(arr)
        t2 = timer()
        return t1-t2 # in nano-seconds        

    # will run experiments for the following list of n
    # each experiemnt will be repeated about K=1000 times
    list_n = [int(10**x) for x in range(2,7)]
    K = 1000
    
    times_QuickSort = []
    times_RandomizedQuickSort = []
    # get sorting times
    for n in list_n:
        arr = generate_randomlist(n)    
        # run K times 
        for k in range(K):
            # for deterministc-quicksort
            single_sort_t = time_single_sort(QuickSort, arr)
            double_sort_t = time_double_sort(QuickSort, arr)
            times_QuickSort.append((single_sort_t, double_sort_t))
            # for randomized-quicksort
            single_sort_t = time_single_sort(QuickSort, arr)
            double_sort_t = time_double_sort(QuickSort, arr)            
            times_RandomizedQuickSort.append((single_sort_t, double_sort_t))
