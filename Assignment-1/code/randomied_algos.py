# randomized algo 

# randomized quick-sort
def RandomizedQuickSort(arr:list):
    from random import randint

    num_comparisons = 0

    def rando_partition(arr, low, high):
        nonlocal num_comparisons
        curr = low - 1

        rando = randint(low+1, high)
        arr[high], arr[rando] = arr[rando], arr[high]

        pivot = arr[high]
        for i in range(low, high):
            if arr[i] <= pivot:
                num_comparisons +=1
                curr += 1
                arr[i], arr[curr] = arr[curr], arr[i]
        arr[curr+1], arr[high] = arr[high], arr[curr+1]
        return curr + 1

    def quicksort(arr, low, high):
        nonlocal num_comparisons
        if low < high:
            num_comparisons += 1
            curr = rando_partition(arr, low, high)
            quicksort(arr, low, curr-1)
            quicksort(arr, curr+1, high)

    if len(arr) <= 1: return arr
    quicksort(arr, 0, len(arr)-1)
    return arr, num_comparisons



if __name__ == "__main__":
    from random import uniform
    import numpy as np
    from time import perf_counter
    n = int(10E6)
    rand_list = np.random.uniform(0,1,n).tolist()
    print('made rand list is size', n)

    t1 = perf_counter()
    RandomizedQuickSort([*rand_list])
    t2 = perf_counter()
    print('randomized-quick-sort',  t2-t1,'s\n')

