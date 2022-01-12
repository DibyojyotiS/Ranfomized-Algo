import sys
import json
from numpy.random import uniform # rnd generator
from time import perf_counter_ns as timer # timer for benchmarking

# sets a larger recursion limit
# however this may be rarely required
sys.setrecursionlimit(10**7) 

# generate list random numbers in [0,1] of size n
def generate_randomlist(n=10E6):
    n = int(n)
    # rand_list = [uniform(0,1) for x in range(n)]
    rand_list = uniform(0,1,n).tolist()
    return rand_list

# measure time for single sort
def time_single_sort(sortingAlgo, arr):
    t1 = timer()
    _, numcomparisons = sortingAlgo(arr)
    t2 = timer()
    return numcomparisons, t2-t1 # in nano-seconds

# measure time for double sort
def time_double_sort(sortingAlgo, arr):
    t1 = timer()
    sortingAlgo(arr)
    sortingAlgo(arr)
    t2 = timer()
    return t2-t1 # in nano-seconds    

# add data to elements of the list counter
def incrementCounter(counter:list, data):
    for i,d in enumerate(data):
        counter[i] += d
    return

# save json-serialized data
def save_json(filname, data):
    with open(filname, 'w') as f:
        json.dump(data, f)

# linear-extrapolation of double-sort times
def extrapolate(data, n):
    n1,n2 = data['array-size'][-2:] 
    t1,t2 = data['avg-double-sort-time-ns'][-2:]
    t = t1 + (n - n1)/(n2-n1) * (t2 - t1)
    return t

def runExperiemnt(sortingAlgo, list_n, K, filename=None, extrapolate_n = []):
    # will run experiments for the following list of n
    # each experiemnt will be repeated K times

    print('running for', sortingAlgo.__name__)
    
    data = {
        'algo-name': sortingAlgo.__name__, # str
        'array-size': [], # list of floats/ints
        'avg-comparisons': [], # list of floats
        'avg-single-sort-time-ns': [], # list of floats
        'avg-double-sort-time-ns': [], # list of floats
        'raw-samples':[] # list of dicts
    }

    # get sorting times
    for n in list_n:
        arr = generate_randomlist(n) 
        print(f'{n} : 0%', end='')

        # accumulators - stores the average
        counters = [0,0,0] #conparisons, single_t, double_t
        samples = {'comparisons':[], 
                    'single-sort-time-ns':[], 
                    'double-sort-time-ns':[]}

        # if n is in extrapolate_n list then extrapolate 
        # double sort time and dont run time_double_sort
        run_doublesort = n not in extrapolate_n
        if not run_doublesort: 
            double_sort_t = extrapolate(data, n)

        # run for K times 
        for k in range(K):
            # for deterministc-quicksort
            numcomparisons, single_sort_t = time_single_sort(sortingAlgo, arr)
            if run_doublesort:
                double_sort_t = time_double_sort(sortingAlgo, arr)
            samples['comparisons'].append(numcomparisons)
            samples['single-sort-time-ns'].append(single_sort_t)
            samples['double-sort-time-ns'].append(double_sort_t)
            sample = (numcomparisons, single_sort_t, double_sort_t)
            incrementCounter(counters, [x/K for x in sample])
            print(f'\r{n} : {100*(k+1)/K:.2f}%', end='')
        data['array-size'].append(n)
        data['raw-samples'].append(samples)
        data['avg-comparisons'].append(counters[0])
        data['avg-single-sort-time-ns'].append(counters[1])
        data['avg-double-sort-time-ns'].append(counters[2])
        print()

    if filename:
        save_json(filename, data)
    return data


# loads the json serealized data
def load_dataset(file_names = [ 'randomized_quickSort_data.json',
                                'mergeSort_data.json',
                                'quickSort_data.json' ]):
    data_set = []
    for filename in file_names:
        with open(filename, 'r') as f:
            data = json.load(f)
            data_set.append(data)
    return data_set