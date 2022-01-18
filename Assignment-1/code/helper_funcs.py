import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
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
def time_single_sort(sortingAlgo, arr:list):
    temp_arr = arr.copy() # copies the array
    t1 = timer()
    _, numcomparisons = sortingAlgo(temp_arr)
    t2 = timer()
    return numcomparisons, t2-t1 # in nano-seconds

# measure time for double sort
def time_double_sort(sortingAlgo, arr:list):
    temp_arr =  arr.copy() # copies the array
    t1 = timer()
    sortingAlgo(temp_arr)
    sortingAlgo(temp_arr) # run again on the sorted temp_arr
    t2 = timer()
    return t2-t1 # in nano-seconds    

# add data to elements of the list counter
def incrementCounter(counter:list, data):
    for i,d in enumerate(data):
        counter[i] += d
    return

# save json-serialized data
def save_json(filename, data):
    head, tail = os.path.split(filename)
    if head and not os.path.exists(head): os.makedirs(head)
    with open(filename, 'w') as f:
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
def load_dataset(file_names = [ 'exp_data/randomized_quickSort_data.json',
                                'exp_data/mergeSort_data.json',
                                'exp_data/quickSort_data.json' ]):
    data_set = []
    for filename in file_names:
        with open(filename, 'r') as f:
            data = json.load(f)
            data_set.append(data)
    return data_set


# prints and returns the number of times the  
# sorting fn from data1 outperformed that of data2
def print_num_times_outperformed(data1, data2):
    arraysize1 = data1['array-size']
    arraysize2 = data2['array-size']
    
    sizearray = arraysize1
    if len(arraysize1) > len(arraysize2):
        sizearray = arraysize2

    num_outperformes = []
    for i,n in enumerate(sizearray):
        raw_samples_1 = data1['raw-samples'][i]['single-sort-time-ns']
        raw_samples_2 = data2['raw-samples'][i]['single-sort-time-ns']

        # outperformes if runtime is lesser
        n_outperform = sum(np.array(raw_samples_1) < np.array(raw_samples_2))
        num_outperformes.append(n_outperform)

    
    data =  {
        'array-size': sizearray,
        'num-outperforms': num_outperformes
    }

    print('\n>>> number of times', data1['algo-name'],
                    'outperfromed', data2['algo-name'])
    print(tabulate(data, headers=['n', 'num-outperfroms']))

    return data


# print the data formated as n, single-t, double-sort-t, comparisons
def print_formated(data):
    print('\n>>>', data['algo-name'])
    header = ['n', 'single-t', 'double-sort-t', 'comparisons']
    pretty_list = [*zip(
        data['array-size'],
        data['avg-single-sort-time-ns'],
        data['avg-double-sort-time-ns'],
        data['avg-comparisons']
    )]
    print(tabulate(pretty_list, headers=header, floatfmt=".3f"))


# print and return stats on deviation for the mean for the given data
def print_deviation_stats(data):
    array_sizes = data['array-size']
    avg_runtimes = data['avg-single-sort-time-ns']
    stumps = [5, 10, 20, 30, 50, 100] # ratios in percentage
    return_dict = {'array-size':array_sizes}
    for k in stumps: return_dict[f'ex_{k}%']=[]
    for i,n in enumerate(array_sizes):
        runtimes = data['raw-samples'][i]['single-sort-time-ns']
        runtimes = np.array(runtimes)
        ratios = runtimes/avg_runtimes[i] - 1
        for k in stumps:
            return_dict[f'ex_{k}%'].append(sum(ratios > k/100))

    print(f'\n>>> {data["algo-name"]}: count of times it exceeds mean by k%')
    print(tabulate(return_dict, headers=return_dict.keys()))
    return return_dict


# draw histogram given experiemnt data
from matplotlib.axes import Axes
def draw_hist(data, ax:Axes=None):
    algo_name = data['algo-name']
    tmp = []
    for i,n in enumerate(data['array-size']):
        samples = data['raw-samples'][i]['single-sort-time-ns']
        samples = np.array(samples)/(2*n*np.log(n))
        tmp.extend(samples)
    if ax is None:
        plt.hist(tmp, 50)
        plt.title(algo_name)
        plt.xlabel('T(n)/2nlogn')
        plt.ylabel('frequency')
        plt.show()

    else:
        ax.hist(tmp, 50)
        ax.set_xlabel('T(n)/2nlogn')
        ax.set_ylabel('frequency')
        ax.set_title(algo_name)


def make_plots(data_set:list, max_row_size=3):
    n = len(data_set)
    assert n > 0
    c = min(max_row_size, n)
    r = (n+c-1)//c
    fig, axs = plt.subplots(r, c, figsize=(3*c,3*r))
    if r > 1 and c > 1: axs = [ax for l in axs for ax in l]
    for data, ax in zip(data_set, axs):
        draw_hist(data, ax)
    plt.tight_layout()
    plt.show()