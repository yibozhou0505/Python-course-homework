# 题目 2-2：排列合法性验证 - 学生代码框架
# 希冀平台提交文件名：{学号}_q22.py（全部小写）
# 输出文件：hw12_2.txt（框架自动写入）


def main():
    # TODO: 在此处编写你的核心算法逻辑
    # 题目要求：验证输入的字符串是否为合法的 python 字母排列
    # - 合法条件：只包含 p,y,t,h,o,n（小写），无重复字符，长度 1-6
    # - 输入格式：第一行是正整数 n，接下来 n 行每行一个字符串
    
    # ------------------- 输入格式要求提醒 -------------------
    # 1. 首先输入一个正整数 n
    # 2. 接下来输入 n 个字符串（每行一个）
    # 从 sys.stdin 读取输入
    # --------------------------------------------------------
    import sys

    def check(s):
        if len(s) < 1 or len(s) > 6:
            return False

        for ch in s:
            if ch not in "python":
                return False
            
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                if s[i] == s[j]:
                    return False

        return True


    lines = sys.stdin.read().splitlines()

    n = int(lines[0])
    results = []

    for i in range(1, n + 1):
        s = lines[i]
        results.append(check(s))

    return results


if __name__ == "__main__":
    # ==========================================================
    # 请勿修改以下代码，这是评测机获取运行时间与内存占用的关键依赖
    # 框架会自动将结果写入 hw12_2.txt 文件
    # ==========================================================

    import time
    import tracemalloc

    # 1. 开启内存分配跟踪
    tracemalloc.start()

    # 2. 记录开始时间
    start_time = time.perf_counter()

    # 3. 执行学生编写的主逻辑
    results = main()

    # 4. 记录结束时间并获取内存峰值
    end_time = time.perf_counter()
    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 5. 计算性能指标
    runtime = end_time - start_time
    memory_kb = peak_memory / 1024

    # 6. 自动写入文件（框架自动处理）
    output_file = "hw12_2.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入所有结果
        for result in results:
            f.write(f"{result}\n")
        # 写入时间和内存（最后一行）
        f.write(f"time: {runtime:.6f}s memory: {memory_kb:.0f}KB\n")