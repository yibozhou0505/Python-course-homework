# 题目 1：计算正弦函数 - 学生代码框架
# 希冀平台提交文件名：{学号}_q1.py（全部小写）
# 输出文件：hw11.txt（框架自动写入）
import sys
import time
import tracemalloc


def my_sin(x):
    """
    计算正弦函数 sin(x)
    要求：不得调用任何数学库中的三角函数，允许使用基本四则运算、比较运算和常量。
    """
    # ==========================================
    # TODO: 在此处编写你的算法逻辑
    # ==========================================
    PI = 3.1415926535897932384626433832795028841971
    x = x % (2*PI)
    if x > PI:
        x -= 2*PI

    if x > PI/2:
        x = PI - x
    elif x < -PI/2:
        x = -PI - x

    term = x
    sin_x = x
    n = 1

    while abs(term) > 1e-16:
        term *= -x * x / ((2*n)*(2*n+1))
        sin_x += term
        n += 1

    return sin_x


def main():
    # ==========================================================
    # 请勿修改以下代码，这是评测机进行自动化批改和性能测试的关键依赖
    # ==========================================================
    tracemalloc.start()
    start = time.perf_counter()

    # 读取输入
    data = sys.stdin.read().strip().split()
    if not data:
        return
    nums = [float(x) for x in data]

    # 执行计算
    results = []
    for x in nums:
        results.append(my_sin(x))

    # 停止监控
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 写入文件（含运行时间与内存占用）
    with open("hw11.txt", "w", encoding="utf-8") as f:
        for r in results:
            f.write("{:.15f}\n".format(r))

        # 最后输出运行时间和内存占用到文件（占一行，无多余空行）
        elapsed = end - start
        peak_kb = peak // 1024
        f.write("运行时间: {:.6f} s  内存占用: {} KB\n".format(elapsed, peak_kb))


if __name__ == "__main__":
    main()