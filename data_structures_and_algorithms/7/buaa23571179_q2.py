import sys
import os
import heapq

def get_output_path():
    submit_dir = "/coursegrader/submit"
    if os.path.isdir(submit_dir):
        return os.path.join(submit_dir, "output.txt")
    return "output.txt"

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    k = int(next(it))

    windows = []
    for _ in range(k):
        m = int(next(it))
        arr = []
        for _ in range(m):
            pid = int(next(it))
            level = int(next(it))
            arrive = int(next(it))
            arr.append((pid, level, arrive))
        windows.append(arr)

    heap = []
    for widx, arr in enumerate(windows):
        if arr:
            pid, level, arrive = arr[0]
            heapq.heappush(heap, (-level, arrive, pid, widx, 0))

    ans = []

    while heap:
        neg_level, arrive, pid, widx, pos = heapq.heappop(heap)
        ans.append(str(pid))

        next_pos = pos + 1
        if next_pos < len(windows[widx]):
            npid, nlevel, narrive = windows[widx][next_pos]
            heapq.heappush(heap, (-nlevel, narrive, npid, widx, next_pos))

    with open(get_output_path(), "w", encoding="utf-8") as f:
        f.write(" ".join(ans))

if __name__ == "__main__":
    main()