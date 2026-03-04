def bubble_sort_all_equal(arr):
    n = len(arr)
    swaps = 0
    for i in range(n-1):
        for j in range(n-1-i):
            if arr[j] > arr[j+1]:  # 条件永远为False，所以不会进行交换
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
    return swaps

if __name__ == '__main__':
    arr = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    print(bubble_sort_all_equal(arr))