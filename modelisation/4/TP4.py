"""
TP4 - Algorithmes de tri

这个文件按照题目顺序给出整份作业的代码解答。
为了便于交作业和复习，我把需要文字说明的理论题也写成了注释。

整体约定：
- 除题目特别要求“原地修改”外，函数尽量返回结果，便于直接测试。
- 某些排序函数会“原地排序 + 返回同一个列表”，这样既符合课程中的算法写法，
  也便于在交互式环境中直接查看结果。
- 注释尽量解释“为什么这样做”，而不只说明“这行代码做了什么”。
"""


# ============================================================
# Exercice 1
# ============================================================
def recherche(T, x):
    """
    在已经按升序排列的列表 T 中进行二分查找。

    返回值约定：
    - 如果找到 x，返回它的一个下标；
    - 如果没有找到，返回 -1。

    这是课程中“recherche dichotomique”的一个标准 Python 写法。
    每一步都把搜索区间缩小一半，因此时间复杂度是 O(log n)。
    """

    gauche = 0
    droite = len(T) - 1

    # 当搜索区间还没有空时，就继续查找。
    while gauche <= droite:
        milieu = (gauche + droite) // 2

        if T[milieu] == x:
            return milieu
        if T[milieu] < x:
            # x 只能出现在右半部分。
            gauche = milieu + 1
        else:
            # x 只能出现在左半部分。
            droite = milieu - 1

    # 搜索区间已经为空，说明 x 不在列表中。
    return -1


# ============================================================
# Exercice 2
# ============================================================
def tri_comptage(L):
    """
    计数排序。

    题目要求列表元素都在 0 到 50 之间，因此可以直接建立一个长度为 51 的计数表。
    计数表的第 k 个位置记录“值 k 一共出现了几次”。

    返回一个新的升序列表，不修改原列表。
    """
    compteur = [0] * 51

    for i in L:
        compteur[i] += 1

    resultat = []
    for i in range(len(compteur)):
        if compteur[i] == 0:
            continue
        if compteur[i] >= 1:
            for _ in range(compteur[i]):
                resultat.append(i)

    return resultat



def tri_comptage_ai(L):
    compteur = [0] * 51

    for valeur in L:
        if valeur < 0 or valeur > 50:
            raise ValueError("tri_comptage 只接受 0 到 50 之间的整数。")
        compteur[valeur] += 1

    resultat = []

    # 按从小到大的顺序，把每个值重复对应次数加入结果列表。
    for valeur in range(51):
        for _ in range(compteur[valeur]):
            resultat.append(valeur)

    return resultat


# ============================================================
# Exercice 3
# ============================================================
# 1. 理论题答案：
#    在第 i 轮外层循环中，第二层循环结束时，变量 indice 对应区间 L[i: ]
#    中最小元素的下标。换句话说，它记录了“还未排好序的部分”里最小值的位置。


def tri_selection(L):
    """
    选择排序。

    算法思想：
    - 第 0 轮，把整个列表中最小的元素放到位置 0；
    - 第 1 轮，把后面剩余部分中最小的元素放到位置 1；
    - ...
    - 最后列表就按升序排好了。

    该函数原地修改列表 L，同时返回 L 本身，便于直接显示结果。
    """
    n = len(L)
    for i in range(n):
        indice = i
        for j in range(i + 1, n):
            if L[j] < L[indice]:
                indice = j
        L[i], L[indice] = L[indice], L[i]
    return L


def tri_selection_ai(L):
    n = len(L)

    for i in range(n):
        # 假设当前位置 i 就是当前未排序区间里最小元素的位置。
        indice = i

        # 在区间 [i + 1, n - 1] 中寻找真正的最小元素。
        for j in range(i + 1, n):
            if L[j] < L[indice]:
                indice = j

        # 把找到的最小元素交换到位置 i。
        L[i], L[indice] = L[indice], L[i]

    return L


# ============================================================
# Exercice 4
# ============================================================
# 1. 星号理论题简述（归纳法思路）：
#    - 初始化：做完第 1 次插入后，前 1 个元素显然有序。
#    - 归纳假设：假设做完第 k 次插入后，前 k 个元素已经按升序排列。
#    - 归纳步骤：第 k + 1 次插入时，把第 k + 1 个元素向左移动，直到它前面的元素
#      都不大于它。这样插入后的前 k + 1 个元素仍保持升序。
#    - 所以对任意 k，做完 k 次插入后，前 k 个元素有序。


def tri_insertion(L):
    """
    插入排序。

    算法思想：
    把列表左边部分始终看作“已经排好序”。
    每次取出一个新元素 key，把它插入到左边合适的位置。

    该函数原地修改列表 L，同时返回 L 本身。
    """
    for i in range(1, len(L)):
        key = L[i]
        j = i - 1
        while j >= 0 and L[j] > key:
            L[j + 1] = L[j]
            j -= 1
        L[j + 1] = key
    return L


def tri_insertion_ai(L):

    for i in range(1, len(L)):
        key = L[i]
        j = i - 1

        # 只要左边元素比 key 大，就把左边元素向右挪一格。
        # 这样空出来的位置最终就是 key 应该插入的位置。
        while j >= 0 and L[j] > key:
            L[j + 1] = L[j]
            j -= 1

        L[j + 1] = key

    return L


# ============================================================
# Exercice 5
# ============================================================
# ex5.1
def fusion(L, M):
    """
    递归地合并两个已经排好序的列表 L 和 M，并返回新的有序列表。

    这里故意使用题目给出的递归思路，而不是更高效的双指针迭代版，
    这样和题目伪代码最一致。
    """
    if L == [] or M == []:
        return L + M
    
    if L[0] < M[0]:
        return [L[0]] + fusion(L[1:], M)
    return [M[0]] + fusion(L, M[1:])

def fusion_ai(L, M):

    # 只要有一个列表为空，另一个列表本身就是已经排好序的剩余部分。
    if L == [] or M == []:
        return L + M

    if L[0] < M[0]:
        return [L[0]] + fusion(L[1:], M)
    return [M[0]] + fusion(L, M[1:])

# ex5.2
def tri_fusion(L):
    """
    归并排序。

    做法：
    - 如果列表长度为 0 或 1，它已经有序；
    - 否则把列表分成左右两半，分别排序；
    - 最后用 fusion 把两个有序列表合并起来。

    返回一个新的有序列表，不修改原列表。
    """
    if len(L) <= 1:
        return L[:]
    
    midien = len(L) // 2
    left = tri_fusion(L[:midien])
    right = tri_fusion(L[midien:])
    return fusion(left, right)

def tri_fusion_ai(L):
    if len(L) <= 1:
        return L[:]

    milieu = len(L) // 2
    gauche = tri_fusion(L[:milieu])
    droite = tri_fusion(L[milieu:])
    return fusion(gauche, droite)


# 3. 星号理论题简述（证明 fusion 的正确性）：
#    对 n = len(L) + len(M) 做归纳。
#    - 初始情形：如果 n = 0 或其中一个列表为空，那么结果直接是 L + M，
#      显然有序。
#    - 归纳假设：假设总长度不超过 n 的任意两个有序列表，其 fusion 结果都仍有序。
#    - 归纳步骤：当总长度为 n + 1 时，比较 L[0] 和 M[0]。
#      较小者一定是整体最小元素，因此应放在结果最前面。
#      去掉这个最小元素后，剩余两表总长度不超过 n，依据归纳假设，
#      递归得到的剩余部分有序，因此整体仍有序。


# ============================================================
# Exercice 6
# ============================================================
# 1. 对题目给出的例子：
#    L = [3, 5, 6, 1, 6, 7, 22, 1, 5]
#    pivot = 3
#
#    初始：
#    [3, 5, 6, 1, 6, 7, 22, 1, 5]
#
#    交换 L[1] 和 L[8]（两者都是 5，列表看起来不变）：
#    [3, 5, 6, 1, 6, 7, 22, 1, 5]
#
#    交换 L[1] 和 L[7]：
#    [3, 1, 6, 1, 6, 7, 22, 5, 5]
#
#    交换 L[2] 和 L[6]：
#    [3, 1, 22, 1, 6, 7, 6, 5, 5]
#
#    交换 L[2] 和 L[5]：
#    [3, 1, 7, 1, 6, 22, 6, 5, 5]
#
#    交换 L[2] 和 L[4]：
#    [3, 1, 6, 1, 7, 22, 6, 5, 5]
#
#    交换 L[2] 和 L[3]：
#    [3, 1, 1, 6, 7, 22, 6, 5, 5]
#
#    跳出 while 后，因为 pivot = 3 不小于 L[2] = 1，
#    所以交换 L[0] 和 L[2]：
#    [1, 1, 3, 6, 7, 22, 6, 5, 5]
#
#    这时 pivot = 3 已经在正确位置，下标是 2。
#
# 2. 为什么 pivot 放置正确：
#    在 while 循环过程中可以维持两个不变式：
#    - 区间 [debut + 1, plus_petit - 1] 中的元素都 <= pivot；
#    - 区间 [plus_grand + 1, fin] 中的元素都 > pivot。
#    循环结束时，未处理区域只剩一个位置（或为空）。
#    再根据 pivot 与 L[plus_petit] 的大小关系，把 pivot 放到
#    “最后一个 <= pivot 的元素后面”或“第一个 > pivot 的元素前面”，
#    因而 pivot 左边都 <= pivot，右边都 > pivot，所以位置正确。
#
# 4. 星号理论题简述：
#    当每次选到的 pivot 都是当前区间的最小值或最大值时，划分极不平衡，
#    例如对已经升序或降序排列的列表就可能发生这种情况。
#    这时递归规模会变成 n-1、n-2、...、1，总比较次数量级为
#    1 + 2 + ... + (n - 1) = O(n^2)。


def tri_rapide_aux(L, start, end):
    """
    按题目给出的伪代码，在列表 L 的闭区间 [debut, fin] 上进行原地快速排序。

    这个版本尽量忠实于题目中的变量名和流程。
    """
    if start < end:
        dividing_point = L[start]
        left = start + 1
        right = end
        while left < right:
            if L[left] > dividing_point:
                L[left], L[right] = L[right], L[left]
                right -= 1
            else:
                left += 1
        if dividing_point < L[right]:
            L[start], L[left - 1] = L[left - 1], L[start]
            fin1 = left - 2
        else:
            L[start], L[right] = L[right], L[start]
            fin1 = right - 1
        tri_rapide_aux(L, start, fin1)
        tri_rapide_aux(L, fin1 + 2, end)


def tri_rapide_aux_ai(L, debut, fin):
    if debut < fin:
        pivot = L[debut]
        plus_petit = debut + 1
        plus_grand = fin

        while plus_petit < plus_grand:
            if L[plus_petit] > pivot:
                # 当前元素大于 pivot，应放到右侧区域中。
                L[plus_petit], L[plus_grand] = L[plus_grand], L[plus_petit]
                plus_grand -= 1
            else:
                # 当前元素小于等于 pivot，应留在左侧区域中。
                plus_petit += 1

        # while 结束后，需要把 pivot 放到最终正确的位置。
        if pivot < L[plus_petit]:
            L[debut], L[plus_petit - 1] = L[plus_petit - 1], L[debut]
            fin1 = plus_petit - 2
        else:
            L[debut], L[plus_petit] = L[plus_petit], L[debut]
            fin1 = plus_petit - 1

        # 递归排序 pivot 左右两侧。
        tri_rapide_aux(L, debut, fin1)
        tri_rapide_aux(L, fin1 + 2, fin)


def tri_rapide(L):
    """
    对整个列表做快速排序。

    题目中给的是辅助函数 tri_rapide_aux，因此这里再补一个总入口：
    只需要调用 tri_rapide_aux(L, 0, len(L) - 1) 就能把整个列表排好序。

    该函数原地修改列表 L，同时返回 L 本身。
    """

    if len(L) > 1:
        tri_rapide_aux(L, 0, len(L) - 1)
    return L


# ============================================================
# Pour les plus rapides : tri par tas
# ============================================================
# 1. 理论题答案：
#    (a) L1 = [2, 3, 4, 2, 5, 6] 不是 tas，因为 L1[3] = 2 < L1[1] = 3。
#    (b) L2 = [4, 1, 6, 5, 3] 不是 tas，因为 L2[1] = 1 < L2[0] = 4。
#    (c) L3 = [1, 2, 2, 5, 6, 4, 3] 是 tas。
#    (d) L4 = [0, 0, 1, 1, 2, 4, 6] 是 tas。
#
# 3. est_tas(L) 的最坏情况比较次数量级是 O(n)，其中 n 是列表长度。
#
# 8. ajout(L, a) 的最坏情况比较次数量级是 O(log n)，因为新元素最多沿树高上升。
#
# 10. extraire_min(L) 的最坏情况比较次数量级是 O(log n)，因为根节点替换后
#     最多沿树高下降。
#
# 11(b). tri_par_tas(L) 的最坏情况比较次数量级是 O(n log n)：
#     - successive additions 建堆是 O(n log n)；
#     - 再做 n 次 extraire_min，总计也是 O(n log n)；
#     - 所以整体仍是 O(n log n)。


def est_tas(L):
    """
    判断列表 L 是否表示一个最小堆（min-heap）。

    题目中的定义是：
    对所有 i >= 1，都有 L[i] >= L[(i - 1) // 2]。
    也就是说：每个节点的值都不小于它父节点的值。
    """

    for i in range(1, len(L)):
        parent = (i - 1) // 2
        if L[i] < L[parent]:
            return False
    return True


def diminue(L, i, a):
    """
    在最小堆 L 中尝试把 L[i] 减小为 a。

    - 如果 a > L[i]，这不是“减小”，函数返回 False；
    - 否则完成赋值，并通过不断和父节点交换来恢复堆结构，返回 True。
    """

    if not 0 <= i < len(L):
        raise IndexError("indice i hors de la liste")

    if a > L[i]:
        return False

    L[i] = a

    # 值变小后，只可能破坏“与父节点之间”的堆性质，因此一路向上调整即可。
    while i > 0:
        parent = (i - 1) // 2
        if L[i] < L[parent]:
            L[i], L[parent] = L[parent], L[i]
            i = parent
        else:
            break

    return True


def augmente(L, i, a):
    """
    在最小堆 L 中尝试把 L[i] 增大为 a。

    - 如果 a < L[i]，这不是“增大”，函数返回 False；
    - 否则完成赋值，并通过不断与较小的孩子比较、交换来恢复堆结构，返回 True。
    """

    if not 0 <= i < len(L):
        raise IndexError("indice i hors de la liste")

    if a < L[i]:
        return False

    L[i] = a
    n = len(L)

    # 值变大后，只可能和子节点发生冲突，因此一路向下调整即可。
    while True:
        gauche = 2 * i + 1
        droite = 2 * i + 2

        # 先默认当前位置最小，如果孩子更小，就更新 smallest。
        smallest = i

        if gauche < n and L[gauche] < L[smallest]:
            smallest = gauche
        if droite < n and L[droite] < L[smallest]:
            smallest = droite

        if smallest == i:
            # 已经满足堆性质，不需要继续下沉。
            break

        L[i], L[smallest] = L[smallest], L[i]
        i = smallest

    return True


def ajout(L, a):
    """
    向最小堆 L 中插入元素 a。

    做法：
    - 先把 a 加到列表最后；
    - 然后不断与父节点比较，如果更小就向上交换。
    """

    L.append(a)
    i = len(L) - 1

    while i > 0:
        parent = (i - 1) // 2
        if L[i] < L[parent]:
            L[i], L[parent] = L[parent], L[i]
            i = parent
        else:
            break


def extraire_min(L):
    """
    从非空最小堆 L 中取出最小值，并保持剩余部分仍是最小堆。

    最小值总在根节点 L[0]。
    取出方法：
    - 记录根节点；
    - 用最后一个元素补到根；
    - 删除最后一个元素；
    - 让新的根不断下沉，直到恢复堆结构。
    """

    if L == []:
        raise ValueError("extraire_min ne peut pas être appelé sur une liste vide")

    minimum = L[0]

    if len(L) == 1:
        L.pop()
        return minimum

    # 用最后一个元素替换根节点，然后删除末尾。
    L[0] = L.pop()
    i = 0
    n = len(L)

    while True:
        gauche = 2 * i + 1
        droite = 2 * i + 2
        smallest = i

        if gauche < n and L[gauche] < L[smallest]:
            smallest = gauche
        if droite < n and L[droite] < L[smallest]:
            smallest = droite

        if smallest == i:
            break

        L[i], L[smallest] = L[smallest], L[i]
        i = smallest

    return minimum


def construction_tas(L):
    """
    按题目要求，用“从空列表开始，逐个 ajout”的方式建堆。

    注意：
    这里故意不使用线性时间 heapify，
    因为题目明确要求“effectue des ajouts successifs”。
    """

    T = []
    for valeur in L:
        ajout(T, valeur)
    return T


def tri_par_tas(L):
    """
    使用最小堆进行排序，并返回一个新的升序列表。

    步骤：
    1. 先构造最小堆；
    2. 再反复取出堆顶最小值，依次加入结果列表。
    """

    T = construction_tas(L)
    resultat = []

    while T != []:
        resultat.append(extraire_min(T))

    return resultat
