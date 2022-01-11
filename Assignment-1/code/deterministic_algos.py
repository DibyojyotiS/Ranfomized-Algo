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

    if len(arr) <= 1: return arr
    quicksort(arr, 0, len(arr)-1)
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
    arr = [23,14,132,23,4,3,213,13,1234,221,14,2,23,21]
    print(arr, '\n', QuickSort([*arr]), '\n')
    print(arr, '\n', MergeSort([*arr]), '\n')

