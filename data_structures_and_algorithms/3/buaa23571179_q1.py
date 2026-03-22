import sys
import time
import tracemalloc
import ast


def process_polynomials(arrays):
    if not isinstance(arrays, list):
        return tuple()

    max_len = 0
    for arr in arrays:
        if isinstance(arr, list):
            max_len = max(max_len, len(arr))

    if max_len == 0:
        return tuple()

    coef = [0.0] * max_len

    for arr in arrays:
        if not isinstance(arr, list):
            continue
        for i, v in enumerate(arr):
            try:
                coef[i] += float(v)
            except Exception:
                continue

    ans = []
    for i, v in enumerate(coef):
        if abs(v) > 1e-12:
            ans.append((i, float(v)))

    return tuple(ans)


def main():
    tracemalloc.start()
    start = time.perf_counter()

    raw_input = sys.stdin.read().strip()
    if not raw_input:
        return
    try:
        arrays = ast.literal_eval(raw_input)
    except Exception:
        arrays = []

    final_tuple = process_polynomials(arrays)

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(str(final_tuple) + "\n")
        elapsed = end - start
        peak_kb = peak // 1024
        f.write("运行时间: {:.6f} s 内存占用: {} KB\n".format(elapsed, peak_kb))


if __name__ == "__main__":
    main()