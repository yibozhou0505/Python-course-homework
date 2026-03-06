import time

# 方式 1：列表拼接（效率最低）
def test1(n):
    lst = []
    for i in range(n*10000):
        lst = lst + [i]
    return lst


# 方式 2：append 方法
def test2(n):
    lst = []
    for i in range(n*10000):
        lst.append(i)
    return lst


# 方式 3：列表推导式
def test3(n):
    return [i for i in range(n*10000)]


# 方式 4：直接转换（效率最高）
def test4(n):
    return list(range(n*10000))


def get_n():
    try:
        s = input().strip()
        if s == "":
            return 1
        n = int(s)
        if 1 <= n <= 5:
            return n
        return 1
    except (ValueError, EOFError):
        return 1


def cul_t(func, n)->int:
    start = time.perf_counter()
    func(n)
    end = time.perf_counter()
    return int((end - start)*1000)


def main():
    n = get_n()
    t1 = cul_t(test1, n)
    t2 = cul_t(test2, n)
    t3 = cul_t(test3, n)
    t4 = cul_t(test4, n)

    analysis = (
        "分析：test1 使用列表拼接每次创建新列表导致 O(n²) 时间复杂度，"
        "test2/test3/test4 都是 O(n) 但实现优化程度不同，"
        "test4 直接使用内置函数效率最高。"
    )

    with open("hw13.res", "w", encoding="utf-8") as f:
        f.write(f"test1,{t1}\n")
        f.write(f"test2,{t2}\n")
        f.write(f"test3,{t3}\n")
        f.write(f"test4,{t4}\n")
        f.write(analysis)

    print("hw13.res 文件已生成")    # ？？？？这样才对何意味

if __name__ == "__main__":
    main()