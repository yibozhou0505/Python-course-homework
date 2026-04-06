import sys
import time
import tracemalloc
from collections import deque


# ==========================================
# 核心要求：
# 1. 只能使用 A~J 共 10 个中间容器
# 2. 必须遵守读一个、放一个的输入原则
# 3. 不允许直接 sort / sorted
# 4. 必须输出完整操作日志与状态
# ==========================================

CONTAINER_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
RANGE = [
    ("A", 1, 13),    # 1~13
    ("B", 14, 13),   # 14~26
    ("C", 27, 13),   # 27~39
    ("D", 40, 13),   # 40~52
    ("E", 53, 12),   # 53~64
    ("F", 65, 12),   # 65~76
    ("G", 77, 12),   # 77~88
    ("H", 89, 12),   # 89~100
]

containers = {}
output_queue = []
logs = []
cost = 0

class Container:
    def __init__(self, name, ctype="queue"):
        self.name = name
        self.ctype = ctype
        self.data = deque()

    def push(self, value, end):
        '''从指定端插入'''
        if self.ctype == "queue":
            if end != "T":
                raise ValueError(f"Queue {self.name} 只能从T端插入")
            self.data.append(value)
        else:
            raise ValueError("就用queue")

    def pop(self, end):
        """从指定端弹出"""
        if not self.data:
            raise IndexError(f"Container {self.name} 为空")

        if self.ctype == "queue":
            if end != "F":
                raise ValueError(f"Queue {self.name} 只能从F端弹出")
            return self.data.popleft()

        else:
            raise ValueError("只用queue")

    def __len__(self):
        return len(self.data)

    def out(self):
        return ",".join(map(str, self.data))


def init_containers():
    """A~J 全部初始化为queue"""
    for n in CONTAINER_NAMES:
        containers[n] = Container(n, ctype="queue")


def make_state_line():
    '''返回当前状态：：容器+OUT'''
    parts = []
    for n in CONTAINER_NAMES:
        parts.append(f"{n}" + "{" + containers[n].out() + "}")
    parts.append("OUT{" + ",".join(map(str, output_queue)) + "}")
    return ", ".join(parts)  # A{41,63}, B{12,25,78}, C{}, D{}, E{}, F{}, G{}, H{}, I{}, J{}, OUT{1,2,3}


def log_step(op_desc):
    '''操作日志'''
    logs.append(op_desc + ", " + make_state_line())  # AF25-BT, A{41,63}, B{12,25,78}, C{}, D{}, E{}, F{}, G{}, H{}, I{}, J{}, OUT{1,2,3}


def which_bucket(x):
    """返回x应该进入哪个桶"""
    for name, start, width in RANGE:
        if start <= x <= start + width - 1:
            return name
    raise ValueError(f"value out of range: {x}")


def bucket_info(name):
    """根据桶名返回 (start, width)"""
    for n, start, width in RANGE:
        if n == name:
            return start, width
    raise ValueError(f"unknown bucket: {name}")


def move_one(src_name, src_end, dst_name, dst_end):
    """
    容器之间合法搬运一次cost += 1
    """
    global cost
    x = containers[src_name].pop(src_end)
    containers[dst_name].push(x, dst_end)
    cost += 1
    log_step(f"{src_name}{src_end}{x}-{dst_name}{dst_end}")  # AF25-BT


def process_input_stream(nums):
    """
    接收阶段：依次读取输入流，每读一个数字立刻放入某个容器。
    禁止利用缓存先排序。

    规则：
    1. 读入阶段 cost = 0；
    2. 每读取一个数字后必须立即放入某个容器；
    3. 每次放入后要记录当前状态。
    """
    for x in nums:
        bucket = which_bucket(x)
        containers[bucket].push(x, "T")
        log_step(f"IN{x}-{bucket}T")


def sort_one_bucket(bucket_name):
    """单个桶排序：把有序结果放到 J"""
    global cost

    src = bucket_name
    buffer = "I"
    dst = "J"

    start, width = bucket_info(bucket_name)
    end = start + width - 1

    for target in range(start, end + 1):
        n = len(containers[src])
        is_found = False

        for _ in range(n):
            x = containers[src].pop("F")

            if x == target and not is_found:
                containers[dst].push(x, "T")
                cost += 1
                log_step(f"{src}F{x}-{dst}T")
                is_found = True
            else:
                containers[buffer].push(x, "T")
                cost += 1
                log_step(f"{src}F{x}-{buffer}T")

        src, buffer = buffer, src

def rearrange_and_output():
    """
    外层排序，cost += 5 / 10个
    """
    global cost

    batch_ops = []

    for bucket_name, _, _ in RANGE:
        sort_one_bucket(bucket_name)

        while len(containers["J"]) > 0:
            x = containers["J"].pop("F")
            output_queue.append(x)
            batch_ops.append(f"JF{x}-OUT")

            if len(batch_ops) == 10:
                cost += 5
                log_step(", ".join(batch_ops))
                batch_ops = []

        if batch_ops:
            cost += 5
            log_step(", ".join(batch_ops))
            batch_ops.clear()
    if batch_ops:
            cost += 5
            log_step(", ".join(batch_ops))
            batch_ops.clear()

def count_errors():
    """检查最终输出是不是严格的 1 to 100"""
    if len(output_queue) != 100:
        return 100

    err = 0
    for i, x in enumerate(output_queue, start=1):
        if x != i:
            err += 1
    return err

def get_type_declaration():
    return "TYPE A=queue,B=queue,C=queue,D=queue,E=queue,F=queue,G=queue,H=queue,I=queue,J=queue"

# --- . 评测系统入口（请勿修改） ---

def main():
    global cost

    tracemalloc.start()
    start = time.perf_counter()

    # 输入格式：100 个 1~100 的整数，空格或换行分隔
    data = sys.stdin.read().replace("\n", " ").split()
    nums = list(map(int, data))

    try:
        init_containers()
        process_input_stream(nums)
        rearrange_and_output()

        error_cnt = count_errors()
        if error_cnt > 0:
            cost += 100 * (error_cnt - 1)

    except Exception as e:
        logs.append(f"Error: {type(e).__name__} -> {str(e)}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 将全过程日志、最终输出、总代价写入 output.txt
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(get_type_declaration() + "\n")
        for line in logs:
            f.write(line + "\n")

        f.write("FINAL OUT{" + ",".join(map(str, output_queue)) + "}\n")
        f.write(f"FINAL COST: {cost}\n")

        elapsed = end - start
        peak_kb = peak // 1024
        f.write("运行时间: {:.6f} s  内存占用: {} KB\n".format(elapsed, peak_kb))


if __name__ == "__main__":
    main()