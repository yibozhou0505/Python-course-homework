# 题目 3：性能测试与分析 - 学生代码框架
# 希冀平台提交文件名：{学号}_q3.py（全部小写）
# 输出文件：hw13.txt（框架自动写入）

import time


def test1(n):
    lst = []
    for i in range(n * 10000):
        lst = lst + [i]
    return lst


def test2(n):
    lst = []
    for i in range(n * 10000):
        lst.append(i)
    return lst


def test3(n):
    return [i for i in range(n * 10000)]


def test4(n):
    return list(range(n * 10000))


def measure_time(func, n, repeat=3):
    """
    测量函数运行时间（毫秒）
    重复多次取平均值以减少误差
    """
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        func(n)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # 转换为毫秒
    return sum(times) / len(times)


def main():
    # TODO: 在此处编写你的核心算法逻辑
    # 题目要求：
    # 1. 实现 test1, test2, test3, test4 四个函数
    # 2. 测量每个函数的运行时间
    # 3. 返回结果和分析
    
    # ------------------- 输入格式要求提醒 -------------------
    # 1. 输入一个正整数 n（用于测试的规模参数）
    # 从 sys.stdin 读取输入
    # --------------------------------------------------------

    # ------------------- 返回值格式要求 -------------------
    # 请返回一个字典，包含以下内容：
    # {
    #     "timings": {"test1": 毫秒数，"test2": 毫秒数，"test3": 毫秒数，"test4": 毫秒数},
    #     "analysis": "你的分析结论（字符串）"
    # }
    # 框架会自动将结果写入 hw13.txt 文件
    # ------------------------------------------------------
    n = int(sys.stdin.read().strip())
    t1 = measure_time(test1, n)
    t2 = measure_time(test2, n)
    t3 = measure_time(test3, n)
    t4 = measure_time(test4, n)

    analysis = "test1 采用列表拼接，每次都会新建列表并复制原有元素，因此耗时最多；test2 使用 append 在原列表末尾追加元素，效率明显更高；test3 使用列表推导式，写法更紧凑，效率也较好；test4 直接使用内置 list(range())，通常效率最高。"

    return {
        "timings": {
            "test1": t1,
            "test2": t2,
            "test3": t3,
            "test4": t4
        }, 
        "analysis": analysis
        }


if __name__ == "__main__":
    # ==========================================================
    # 请勿修改以下代码，这是评测机获取运行时间与内存占用的关键依赖
    # 框架会自动将结果写入 hw13.txt 文件
    # ==========================================================

    import sys
    import tracemalloc

    # 1. 开启内存分配跟踪
    tracemalloc.start()

    # 2. 记录开始时间
    start_time = time.perf_counter()

    # 3. 执行学生编写的主逻辑
    result = main()

    # 4. 记录结束时间并获取内存峰值
    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 5. 计算性能指标
    runtime = end_time - start_time
    memory_kb = peak_memory / 1024

    # 6. 自动写入文件（框架自动处理）
    output_file = "hw13.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入测试结果
        timings = result.get("timings", {})
        for i in range(1, 5):
            key = f"test{i}"
            ms = timings.get(key, 0.0)
            f.write(f"{key},{ms:.2f}\n")
        
        # 写入分析
        analysis = result.get("analysis", "")
        if analysis:
            f.write(f"{analysis}\n")
        
        # 写入时间和内存（最后一行）
        f.write(f"time: {runtime:.6f}s memory: {memory_kb:.0f}KB\n")