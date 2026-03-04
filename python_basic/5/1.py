def bubble_sort(arr):
    n = len(arr)
    comparisons = swaps = 0

    for i in range(n-1):  # 必执行n-1次
        for j in range(n-1-i):  # 每轮比较次数递减
            comparisons += 1  # 比较次数

            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swaps += 1
    return comparisons, swaps

if __name__ == '__main__':
    arr = [5, 3, 8, 6, 7, 2, 9, 1, 4, 0]
    print(bubble_sort(arr.copy()))  # 输出(45, 26)
'''
实际上代码运行结果输出应该是(45, 29)....
'''