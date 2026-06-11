# 插排
L = [2, 5, 7, 1, 9, 0, 4, 1]
def insertion_sort(L):
    n = len(L)
    for i in range(1,n):
        j = i - 1
        key = L[i]
        while j >= 0 and L[j] > key:
            L[j+1] = L[j]
            j -= 1
        L[j+1] = key
    return L
print(insertion_sort(L))

# 选择
def select_sort(L):
    n = len(L)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1,n):
            if L[j] < L[min_idx]:
                min_idx = j
        if min_idx != i:
            L[i], L[min_idx] = L[min_idx], L[i]
    return L


# 冒泡
def bubble_sort(L):
    n = len(L)
    for i in range(n):
        swapped = False
        for j in range(n-i-1):
            if L[j] > L[j+1]:
                L[j],L[j+1] = L[j+1],L[j]
                swapped = True
        if not swapped:
            break
    return L
print(bubble_sort(L))


# 归并排序
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    sorted_left = merge_sort(left)
    sorted_right = merge_sort(right)

    return merge(sorted_left,sorted_right)

def merge(L, R):
    result = []
    i = 0
    j = 0

    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            result.append(L[i])
            i += 1
        else:
            result.append(R[j])
            j += 1

    result.extend(L[i:])
    result.extend(R[j:])
    return result



# 快速排序
def quick_sort(arr,low,high):
    if low < high:
        pivot_index = partition(arr,low,high)
        quick_sort(arr,low,pivot_index - 1)
        quick_sort(arr,pivot_index + 1,high)

def partition(arr,low,high):
    pivot = arr[high]
    i = low -1

    for j in range(low,high):
        if arr[j] <= pivot:
            i+=1
            arr[i],arr[j] = arr[j],arr[i]

    arr[i+1],arr[high] = arr[high], arr[i+1]
    return i+1


# 桶排序
def bucket_sort(arr):
    '''根据数据分布指定范围'''
    min_val, max_val = min(arr), max(arr)
    n = len(arr)

    bucket_count = n
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        if max_val == min_val:
            idx = 0
        else:
            idx = int((num - min_val) / (max_val - min_val) * (bucket_count - 1))
        buckets[idx].append(num)

    for bucket in buckets:
        insertion_sort(bucket)

    result = []
    for bucket in buckets:
        result.extend(bucket)

    return result


# 基数排序
def radix_sort(arr):
    max_val = max(arr)
    exp = 1  

    while max_val // exp > 0:
        buckets = [[] for _ in range(10)]

        for num in arr:
            digit = (num // exp) % 10
            buckets[digit].append(num)

        arr = [num for bucket in buckets for num in bucket]

        exp *= 10

    return arr


# 剪枝搜索
# def partition(arr, left, right):
#     """
#     对 arr[left:right+1] 做划分。
#     选择 arr[right] 作为 pivot。

#     划分完成后：
#     - pivot 左边的元素 <= pivot
#     - pivot 右边的元素 > pivot
#     - 返回 pivot 的最终下标
#     """

#     pivot = arr[right]

#     # i 表示“小于等于 pivot 区域”的最后一个位置
#     i = left - 1

#     for j in range(left, right):
#         if arr[j] <= pivot:
#             i += 1
#             arr[i], arr[j] = arr[j], arr[i]

#     # 把 pivot 放到最终位置
#     arr[i + 1], arr[right] = arr[right], arr[i + 1]

#     return i + 1


def pruning_search(arr, k):
    """
    剪枝搜索：找第 k 小元素。
    k 从 1 开始，例如 k=1 表示最小值。

    注意：这个函数会修改原数组。
    """

    if k < 1 or k > len(arr):
        raise ValueError("k 必须在 1 到 len(arr) 之间")

    left = 0
    right = len(arr) - 1

    while left <= right:
        pivot_index = partition(arr, left, right)

        # pivot 是当前整个数组中的第 rank 小
        rank = pivot_index - left + 1

        if k == rank:
            return arr[pivot_index]

        elif k < rank:
            # 第 k 小在左边，只搜索左边
            right = pivot_index - 1

        else:
            # 第 k 小在右边
            # 右边要找的是第 k-rank 小
            k -= rank
            left = pivot_index + 1

# 随机快速选择
import random


def randomized_partition(arr, left, right):
    """
    随机选择 pivot，然后做 partition。
    """

    # 在 [left, right] 之间随机选一个下标
    pivot_index = random.randint(left, right)

    # 把随机选中的 pivot 放到最后
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]

    # 调用普通 partition
    return partition(arr, left, right)


def randomized_quickselect(arr, k):
    """
    随机快速选择：找第 k 小元素。
    k 从 1 开始。

    注意：这个函数会修改原数组。
    """

    if k < 1 or k > len(arr):
        raise ValueError("k 必须在 1 到 len(arr) 之间")

    left = 0
    right = len(arr) - 1

    while left <= right:
        pivot_index = randomized_partition(arr, left, right)

        rank = pivot_index - left + 1

        if k == rank:
            return arr[pivot_index]

        elif k < rank:
            right = pivot_index - 1

        else:
            k -= rank
            left = pivot_index + 1


text = "i am hungry",'help'
print(text)
it=iter(text)
a=next(it)
print (a)
b=next(it)
print (b)

