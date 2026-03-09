# 题目 4：交叉路口红绿灯安全调度 - 学生代码框架
# 希冀平台提交文件名：{学号}_q4.py（全部小写）
# 输出文件：hw14.txt（框架自动写入）

import time
import tracemalloc


def solve():
    """
    计算交叉路口红绿灯分组方案

    返回:
        list[str]: 包含恰好 2 个合法分组方案字符串的列表。

    格式要求:
        1. 每套方案的字符串必须严格符合格式：((路线1,路线2,...),(路线3,路线4,...),...)
        2. 内部不要有任何多余的空格。
        3. 请自行在代码中处理组内排序（起点终点字典序）、组间排序及整行结果的字典序。
    """
    # ==========================================
    # TODO: 在此处编写你的算法逻辑，并自己完成字符串拼接
    # ==========================================

    # passable
    routes = [
        "AB", "AC", "AD",
        "BA", "BC", "BD",
        "DA", "DB", "DC",
        "EA", "EB", "EC", "ED"
    ]
    pos = {"C": 0, "D": 1, "E": 2, "A": 3, "B": 4}

    def between(x, a, b):
        """judge if x is between a and b"""
        if a < b:
            return a < x < b
        return x > a or x < b

    def conflict(r1, r2):
        """judge if r1 and r2 conflict"""
        # same start
        if r1[0] == r2[0]:
            return False
        # same end
        if r1[1] == r2[1]:
            return False

        a = pos[r1[0]]
        b = pos[r1[1]]
        c = pos[r2[0]]
        d = pos[r2[1]]

        # non intersect -> non conflict
        if len({a, b, c, d}) < 4:
            return False

        return (between(c, a, b) != between(d, a, b) and
                between(a, c, d) != between(b, c, d))

    n = len(routes)

    # ---------- graph ----------
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if conflict(routes[i], routes[j]):
                g[i][j] = 1
                g[j][i] = 1

    def can_add(idx, group):
        """judge if can add"""
        for j in group:
            if g[idx][j] == 1:
                return False
        return True

    def scheme_to_string(groups):
        # sort in group
        parts = []
        for g in groups:
            names = [routes[i] for i in g]
            names.sort()
            parts.append("(" + ",".join(names) + ")")

        # sort between group
        parts.sort()
        return "(" + ",".join(parts) + ")"

    def greedy(seed_reverse=False, scan_reverse=False):
        remaining = list(range(n))
        remaining.sort(key=lambda i: routes[i], reverse=seed_reverse)

        groups = []

        while remaining:
            # select une node without grouped -> new grouop
            first = remaining.pop(0)
            group = [first]

            # scan rest
            scan_list = remaining[::-1] if scan_reverse else remaining[:]
            added = []
            for idx in scan_list:
                if can_add(idx, group):
                    group.append(idx)
                    added.append(idx)

            # revoke
            for idx in added:
                remaining.remove(idx)

            groups.append(group)

            # remaining
            remaining.sort(key=lambda i: routes[i], reverse=seed_reverse)

        return scheme_to_string(groups)

    # get diff ways by greedy
    answers = set()
    answers.add(greedy(False, False))
    answers.add(greedy(False, True))
    answers.add(greedy(True, False))
    answers.add(greedy(True, True))

    answers = sorted(answers)
    return [answers[0], answers[1]]


def main():
    # ==========================================================
    # 请勿修改以下代码，这是评测机进行自动化批改和性能测试的关键依赖
    # ==========================================================

    # 1. 开启性能监控
    tracemalloc.start()
    start = time.perf_counter()

    # 2. 调用学生编写的核心算法，获取两行字符串答案
    results = solve()

    # 3. 停止监控并计算性能消耗
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 4. 严格按照题目格式要求，将结果与性能指标写入 hw14.txt
    with open("hw14.txt", "w", encoding="utf-8") as f:
        if results and len(results) >= 2:
            # 输出恰好两套分组方案，每套占一行
            f.write(results[0] + "\n")
            f.write(results[1] + "\n")
        else:
            # 若未按要求返回，则输出占位防报错
            f.write("格式错误\n")
            f.write("格式错误\n")

        # 在上一部分的下一行输出性能指标，无空行
        elapsed = end - start
        peak_kb = peak // 1024
        f.write("运行时间: {:.6f} s  内存占用: {} KB\n".format(elapsed, peak_kb))


if __name__ == "__main__":
    main()