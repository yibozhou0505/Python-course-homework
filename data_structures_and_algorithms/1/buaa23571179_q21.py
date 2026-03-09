# 题目 2-1：字母排列生成 - 学生代码框架
# 希冀平台提交文件名：{学号}_q21.py（全部小写）
# 输出文件：hw12_1.txt（框架自动写入）


def main():
    # TODO: 在此处编写你的核心算法逻辑
    # 题目要求：生成所有由字母 'p','y','t','h','o','n' 组成的字符串
    # - 字符串长度为 1 到 6
    # - 每个字母在单个字符串中只能使用 1 次
    # - 需要生成所有可能的排列组合
    
    # ------------------- 返回值格式要求 -------------------
    # 请返回一个列表，包含所有生成的字符串组合
    # 框架会自动将结果写入 hw12_1.txt 文件
    # ------------------------------------------------------

    # 示例返回值（仅演示格式，并非正确答案）：
    # return ["p", "y", "t", "h", "o", "n", "py", "pt", ...]

    chars = ["h", "n", "o", "p", "t", "y"]
    used = [0]*len(chars)
    selected = []
    results = []

    def permu():
        if len(selected) >= 1:
            results.append("".join(selected))

        if len(selected) == len(chars):
            return

        for i in range(len(chars)):
            if used[i] == 0:
                used[i] = 1
                selected.append(chars[i])

                permu()

                selected.pop()
                used[i] = 0

    permu()

    return results


if __name__ == "__main__":
    # ==========================================================
    # 请勿修改以下代码，这是评测机获取运行时间与内存占用的关键依赖
    # 框架会自动将结果写入 hw12_1.txt 文件
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
    output_file = "hw12_1.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入所有结果
        for result in results:
            f.write(f"{result}\n")
        # 写入时间和内存（最后一行）
        f.write(f"time: {runtime:.6f}s memory: {memory_kb:.0f}KB\n")