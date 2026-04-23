import sys
import os
import heapq  # python最小堆工具

# 题目随机数更新工具 seed = (seed * 1103515245 + 12345) mod 2147483648
MOD = 2147483648

def get_output_path():
    submit_dir = "/coursegrader/submit"
    if os.path.isdir(submit_dir):
        return os.path.join(submit_dir, "output.txt")
    return "output.txt"

def next_rand(seed, L, R):
    '''生成一次随机整数函数，输入当前种子和目标区间'''
    seed = (seed * 1103515245 + 12345) % MOD
    value = L + (seed % (R - L + 1))
    return seed, value

def generate_cars(n, a, b, c, d, seed):
    '''生成全部车辆数据：[a,b]到达间隔范围；[c,d]服务时间范围；种子'''
    arrivals = [0] * n
    services = [0] * n

    seed, services[0] = next_rand(seed, c, d)

    for i in range(1, n):
        seed, gap = next_rand(seed, a, b)
        arrivals[i] = arrivals[i - 1] + gap
        seed, services[i] = next_rand(seed, c, d)

    return arrivals, services

def simulate(arrivals, services, k, total_service):
    free_lanes = list(range(1, k + 1))  # 空闲通道，按编号最小优先
    heapq.heapify(free_lanes)

    busy_lanes = []  # (finish_time, lane_id)

    total_wait = 0
    max_wait = 0
    finish_time = 0

    for arrival, service in zip(arrivals, services):
        # 先释放所有在 arrival 时刻前已经空闲的通道
        while busy_lanes and busy_lanes[0][0] <= arrival:
            end_time, lane_id = heapq.heappop(busy_lanes)
            heapq.heappush(free_lanes, lane_id)

        if free_lanes:
            lane_id = heapq.heappop(free_lanes)
            start_time = arrival
        else:
            earliest_end, lane_id = heapq.heappop(busy_lanes)
            start_time = earliest_end

        wait = start_time - arrival
        end_time = start_time + service

        total_wait += wait
        if wait > max_wait:
            max_wait = wait
        if end_time > finish_time:
            finish_time = end_time

        heapq.heappush(busy_lanes, (end_time, lane_id))

    avg_wait = total_wait / len(arrivals)
    utilization = total_service / (k * finish_time) if finish_time > 0 else 0.0

    return avg_wait, max_wait, finish_time, utilization

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    a = int(next(it))
    b = int(next(it))
    c = int(next(it))
    d = int(next(it))
    seed = int(next(it))
    ks = [int(next(it)) for _ in range(m)]

    arrivals, services = generate_cars(n, a, b, c, d, seed)
    total_service = sum(services)

    out_lines = []
    for k in ks:
        avg_wait, max_wait, finish_time, utilization = simulate(arrivals, services, k, total_service)
        out_lines.append(f"{k} {avg_wait:.4f} {max_wait} {finish_time} {utilization:.4f}")

    with open(get_output_path(), "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

if __name__ == "__main__":
    main()