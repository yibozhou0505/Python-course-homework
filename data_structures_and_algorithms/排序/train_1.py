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