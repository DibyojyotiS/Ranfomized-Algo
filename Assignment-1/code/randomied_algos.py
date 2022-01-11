# randomized algo 

# randomized quick-sort
def RandomizedQuickSort(arr:list):
    from random import randint

    def rando_partition(arr, low, high):
        curr = low - 1

        rando = randint(low+1, high)
        arr[high], arr[rando] = arr[rando], arr[high]

        pivot = arr[high]
        for i in range(low, high):
            if arr[i] <= pivot:
                curr += 1
                arr[i], arr[curr] = arr[curr], arr[i]
        arr[curr+1], arr[high] = arr[high], arr[curr+1]
        return curr + 1

    def quicksort(arr, low, high):
        if low < high:
            curr = rando_partition(arr, low, high)
            quicksort(arr, low, curr-1)
            quicksort(arr, curr+1, high)

    if len(arr) <= 1: return arr
    quicksort(arr, 0, len(arr)-1)
    return arr



if __name__ == "__main__":
    arr = [23,14,132,23,4,3,213,13,1234,221,14,2,23,21]
    print(arr, '\n', RandomizedQuickSort([*arr]), '\n')

