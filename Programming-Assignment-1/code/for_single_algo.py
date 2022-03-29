from helper_funcs import draw_hist, print_deviation_stats, runExperiemnt
from randomied_algos import RandomizedQuickSort


if __name__ == "__main__":
    list_n = [10**x for x in range(2,7)]

    data_RandomizedQuickSort = runExperiemnt(RandomizedQuickSort, list_n, K=500, fix_arr=True,
                                        filename='exp_data/randomized_quickSort_data.json')
    print('rand-quick-sort:\n', data_RandomizedQuickSort['avg-comparisons'],
                                data_RandomizedQuickSort['avg-single-sort-time-ns'],
                                data_RandomizedQuickSort['avg-double-sort-time-ns'])

    print_deviation_stats(data_RandomizedQuickSort)

    draw_hist(data_RandomizedQuickSort)