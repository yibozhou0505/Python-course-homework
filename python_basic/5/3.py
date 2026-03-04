def selection_sort(arr):
    n = len(arr)
    comparisons = swaps = 0
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        swaps += 1
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return comparisons, swaps

if __name__ == '__main__':
    arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(selection_sort(arr.copy()))