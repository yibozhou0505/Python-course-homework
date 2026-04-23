import sys
import os
import heapq
from collections import deque

def get_output_path():
    submit_dir = "/coursegrader/submit"
    if os.path.isdir(submit_dir):
        return os.path.join(submit_dir, "output.txt")
    return "output.txt"

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    T = int(data[0])
    idx = 1

    queues = [deque() for _ in range(40)]  # priority -20..19 -> idx 0..39
    heap = []
    in_heap = [False] * 40

    def activate(qidx):
        if not in_heap[qidx]:
            heapq.heappush(heap, qidx)
            in_heap[qidx] = True

    def clean_top():
        while heap and not queues[heap[0]]:
            qidx = heapq.heappop(heap)
            in_heap[qidx] = False

    def run_one_slice():
        clean_top()
        if not heap:
            return "idle"

        qidx = heap[0]
        name, remain = queues[qidx].popleft()

        # 如果取出后该优先级队列空了，需要暂时从堆中删掉
        if not queues[qidx]:
            heapq.heappop(heap)
            in_heap[qidx] = False

        remain -= 1

        if remain > 0:
            queues[qidx].append((name, remain))
            activate(qidx)

        return name

    outputs = []

    for _ in range(T):
        cmd = data[idx].decode()
        idx += 1

        if cmd == "add":
            name = data[idx].decode()
            p = int(data[idx + 1])
            n = int(data[idx + 2])
            idx += 3

            qidx = p + 20
            queues[qidx].append((name, n))
            activate(qidx)

        # 不管是 add 还是 noop，这个时间片都要调度一次
        outputs.append(run_one_slice())

    # 输入结束后继续收尾调度
    while True:
        clean_top()
        if not heap:
            break
        outputs.append(run_one_slice())

    with open(get_output_path(), "w", encoding="utf-8") as f:
        f.write("\n".join(outputs))

if __name__ == "__main__":
    main()