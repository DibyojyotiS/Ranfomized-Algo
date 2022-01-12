# Deterministic 

# deterministic quick-sort
def QuickSort(arr:list):

    num_comparisons = 0

    def partition(arr, low, high):
        nonlocal num_comparisons
        curr = low - 1
        pivot = arr[high]
        for i in range(low, high):
            if arr[i] <= pivot:
                num_comparisons+=1
                curr += 1
                arr[i], arr[curr] = arr[curr], arr[i]
        arr[curr+1], arr[high] = arr[high], arr[curr+1]
        return curr + 1

    def quicksort(arr, low, high):
        nonlocal num_comparisons
        if low < high:
            num_comparisons += 1
            curr = partition(arr, low, high)
            quicksort(arr, low, curr-1)
            quicksort(arr, curr+1, high)

    def non_recursive_quicksort(arr, low, high):
        nonlocal num_comparisons
        call_stack = []
        call_stack.append((low, high))
        while call_stack:
            low, high = call_stack.pop()
            if low < high:
                num_comparisons += 1
                curr = partition(arr, low, high)
                call_stack.append((low, curr-1))
                call_stack.append((curr+1, high))


    if len(arr) <= 1: return arr
    # quicksort(arr, 0, len(arr)-1)
    non_recursive_quicksort(arr, 0, len(arr)-1)
    return arr, num_comparisons


# deterministic mergesort
def MergeSort(arr:list):

    num_comparisons = 0

    def merge(arr, a,b):
        nonlocal num_comparisons
        i=j=k=0
        while i<len(a) and j<len(b):
            num_comparisons += 2
            if a[i] < b[j]:
                num_comparisons += 1
                arr[k] = a[i]
                i+=1
            else:
                arr[k] = b[j]
                j+=1
            k+=1
        
        while i < len(a):
            num_comparisons += 1
            arr[k] = a[i]
            i+=1
            k+=1
        
        while j < len(b):
            num_comparisons += 1
            arr[k] = b[j]
            j+=1
            k+=1
        return

    def mergesort(arr):
        nonlocal num_comparisons
        if len(arr) == 1: 
            num_comparisons += 1
            return
        mid = len(arr)//2
        a, b = arr[:mid], arr[mid:]
        mergesort(a)
        mergesort(b)
        merge(arr, a,b)

    mergesort(arr)
    return arr, num_comparisons


if __name__ == "__main__":
    from random import uniform
    import numpy as np
    from time import perf_counter
    n = int(10E6)
    rand_list = np.random.uniform(0,1,n).tolist()
    print('made rand list')

    t1 = perf_counter()
    QuickSort([*rand_list])
    t2 = perf_counter()
    print('quick-sort',  t2-t1,'s\n')

    t1 = perf_counter()
    MergeSort([*rand_list])
    t2 = perf_counter()
    print('merge-sort',  t2-t1,'s\n')


