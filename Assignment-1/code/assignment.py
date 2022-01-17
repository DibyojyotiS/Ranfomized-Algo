from deterministic_algos import QuickSort, MergeSort
from randomied_algos import RandomizedQuickSort
from helper_funcs import *

RUN_SORTS = False # set to True to run the sorts

# run merge-sort, quick-sort and randomized-quick-sort
# and save the data
def assignment():

    # run experiemtns and results
    list_n = [10**x for x in range(2,7)]

    data_RandomizedQuickSort = runExperiemnt(RandomizedQuickSort, list_n, K=500, 
                                        filename='exp_data/randomized_quickSort_data.json')
    print('rand-quick-sort:\n', data_RandomizedQuickSort['avg-comparisons'],
                                data_RandomizedQuickSort['avg-single-sort-time-ns'],
                                data_RandomizedQuickSort['avg-double-sort-time-ns'])


    data_MergeSort = runExperiemnt(MergeSort, list_n, K=500, 
                                        filename='exp_data/mergeSort_data.json')
    print('merge-sort:\n', data_MergeSort['avg-comparisons'],
                            data_MergeSort['avg-single-sort-time-ns'],
                            data_MergeSort['avg-double-sort-time-ns'])


    # extrapolate double-sort time for 10E5 and 10E6
    data_QuickSort = runExperiemnt(QuickSort, list_n, K=500, 
                                        extrapolate_n=[10**5, 10**6],
                                        filename='exp_data/quickSort_data.json')

    print('quick-sort:\n', data_QuickSort['avg-comparisons'],
                            data_QuickSort['avg-single-sort-time-ns'],
                            data_QuickSort['avg-double-sort-time-ns'])
    
    data_set = [data_RandomizedQuickSort, data_MergeSort, data_QuickSort]
    return data_set


if __name__ == "__main__":
    if RUN_SORTS: data_set = assignment() # run the experiments and get all the data
    else: data_set = load_dataset()
    for data in data_set: print_formated(data)

    # number of times merge-sort outperformed quick-sort
    print_num_times_outperformed(data_set[1], data_set[2])

    # deviations
    print_deviation_stats(data_set[0])

    # plots
    make_plots(data_set)