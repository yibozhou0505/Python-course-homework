def selection_sort_all_equal(arr):
    n = len(arr)
    swaps = 0
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j  # 找到新的最小值索引
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return swaps
if __name__ == '__main__':
    arr = [2]*10
    print(selection_sort_all_equal(arr))
'''
题干备注有问题，代码逻辑是先找到最小值的索引，如果最小值索引不是i，则交换
'''