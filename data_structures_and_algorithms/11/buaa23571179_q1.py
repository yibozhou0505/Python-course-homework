import sys
import heapq  # python最小堆->实现dijkstra


def solve():
    data = sys.stdin.buffer.read().split()  # 一次性读完得到字节串，split()按空格切开
    if not data:
        return

    it = iter(data)  # 变成迭代器对象，可以通过next(it)读下一个token

    # 通过迭代器读取开头的输入
    N = int(next(it))  # 站点数
    L = int(next(it))  # 线路数
    M = int(next(it))  # 轨道区间数
    R = int(next(it))  # 换乘记录数
    Q = int(next(it))  # 乘客行程数

    # 读N个站点名字，.decode()要把输入读出来的字节转成字符串
    stations = [next(it).decode() for _ in range(N)]
    station_id = {name: i for i, name in enumerate(stations)}  # 方便graph用id查找

    line_company = {}
    for _ in range(L):
        line = next(it).decode()      # 线路
        company = next(it).decode()   # 公司
        line_company[line] = company  # key是线路；value是公司名

    # 初始化
    raw_edges = []  # 保存原始轨道边(u,v,line,dist)
    station_lines = [set() for _ in range(N)]  # 记录某一个站上有哪一些线路经过
    graph_dist = [[] for _ in range(N)]  # graph_dist[u] = [(to, line, dist), ...] 从u出发的所有边

    # 读取轨道区间建立站点图 e.g. A B L1 4
    for _ in range(M):
        u_name = next(it).decode()  # 'A'
        v_name = next(it).decode()  # 'B'
        line = next(it).decode()    # 'L1'
        dist = int(next(it))        # 4

        # 当前站，下一站，字符串转编号
        u = station_id[u_name]      # 0
        v = station_id[v_name]      # 1

        raw_edges.append((u, v, line, dist))  # 保存原始边 (0,1,"L1",4)

        # 建立最短距离图：轨道是无向边要加两次
        graph_dist[u].append((v, line, dist))  # 从0出发的所有边+1：(1,'L1',4)
        graph_dist[v].append((u, line, dist))  # (0,'L1',4)

        # 记录站点有哪一些线
        station_lines[u].add(line)
        station_lines[v].add(line)

    # 读取换乘记录
    transfer_records = []  # 假设进来的是 (C, L1, L2, 4)
    for _ in range(R):
        s_name = next(it).decode()
        line_a = next(it).decode()
        line_b = next(it).decode()
        t = int(next(it))

        s = station_id[s_name]  # 转成idx
        transfer_records.append((s, line_a, line_b, t))  # (station_idx, "L1", "L2", 4)

        # 记录站点有哪一些线
        station_lines[s].add(line_a)
        station_lines[s].add(line_b)

    # 读取乘客查询
    queries = []  # 假设进来的是 A G
    for _ in range(Q):
        o_name = next(it).decode()
        d_name = next(it).decode()
        queries.append((station_id[o_name], station_id[d_name]))  # (0, 6)

    # 建立站点-线路状态图
    state_id = {}
    state_station = []
    state_line = []

    for s in range(N):
        for line in station_lines[s]:  # 对于站点s的每一条线路分配一个sid
            sid = len(state_station)   # 一开始state_station为[]，sid=0；然后append之后len变长，相当于在做id分配
            state_id[(s, line)] = sid  # (站点,线路) -> sid
            state_station.append(s)    # 可以通过state_station[sid]查到这个状态对应的站点
            state_line.append(line)    # 可以通过state_line[sid]查到这个状态对应的线路

    # 初始化时间图 / 状态图
    S = len(state_station)   # 所有“站点-线路”状态总数
    graph_time = [[] for _ in range(S)]  # 状态图

    for u, v, line, dist in raw_edges:
        su = state_id[(u, line)]  # 对应的站点-线路的sid
        sv = state_id[(v, line)]
        # (到达的新状态sid, 时间增加多少, 距离增加多少, 换乘次数增加多少, 路径字符串新增部分)
        graph_time[su].append((sv, dist, dist, 0, "-" + line + "-" + stations[v]))
        graph_time[sv].append((su, dist, dist, 0, "-" + line + "-" + stations[u]))

    for s, line_a, line_b, t in transfer_records:
        if (s, line_a) in state_id and (s, line_b) in state_id:
            sa = state_id[(s, line_a)]
            sb = state_id[(s, line_b)]
            # (新状态sid, 时间增加多少, 距离增加多少, 换乘次数+1, 路径字符串不变)
            # 因为换乘发生在站内，不会新增一个“站点-线路-站点”的轨道片段
            graph_time[sa].append((sb, t, 0, 1, ""))
            graph_time[sb].append((sa, t, 0, 1, ""))

# =================== 5.1 最短距离 =====================
# 【修改说明】
# 原来你的DIST是在“站点图”上跑，这会默认“到了某个站就能任意切换线路”
# 但题目要求：未给出的换乘视为不可换乘
# 所以DIST也必须在“站点-线路状态图”上跑，只不过：
#   1) 行驶边：距离增加dist
#   2) 合法换乘边：距离增加0
#   3) 非法换乘：根本没有边，所以自然走不过去
    def shortest_distance(src, dst):
        if src == dst:  # 如果起终点相同，距离为0，路径只输出该站
            return (0, stations[src])

        # 起点第一次上车不产生换乘，所以起点可以从任意经过src的线路状态出发
        start_states = []
        for line in station_lines[src]:
            sid = state_id.get((src, line))
            if sid is not None:
                start_states.append(sid)

        if not start_states:
            return None

        # best[state] = (总距离, 经过站点数, 路径字符串)
        # 这里保留题目要求的DIST平局规则：
        # 1. 总距离最小
        # 2. 若总距离相同，经过站点数更少
        # 3. 若仍相同，路径字符串字典序更小
        INF = (10**30, 10**30, "~")
        best = [INF] * S
        pq = []

        start_route = stations[src]  # 初始化路径字符串的第一站
        for sid in start_states:
            best[sid] = (0, 1, start_route)  # 起点到自己距离0；经过自己1个站点；路径字符串
            pq.append((0, 1, start_route, sid))  # (距离, 经过站数, 路径字符串, 当前状态sid)

        heapq.heapify(pq)

        while pq:
            # 弹出最优状态：距离最短优先 -> 站数最少 -> 路径串字典序最小
            cur_dist, cur_cnt, cur_route, u = heapq.heappop(pq)
            if (cur_dist, cur_cnt, cur_route) != best[u]:
                # 同一个状态u可能多次被推入堆中（通过不同路径到达）
                # 后面弹出的旧状态已经不是当前最优，直接跳过
                continue

            # 到达终点站的任意线路状态都可以结束
            if state_station[u] == dst:
                return (cur_dist, cur_route)

            # 在状态图上做松弛
            for v, dt, dd, dc, append_str in graph_time[u]:
                # 对DIST来说，真正关心的是“距离增量dd”
                # 行驶边：dd = dist
                # 换乘边：dd = 0
                nd = cur_dist + dd

                # 只有真正经过一条轨道区间，才新增一个站点
                # 换乘边append_str == ""，说明仍在同一站内切线，不增加站点数
                nc = cur_cnt + (1 if append_str else 0)

                # 换乘边不改变路径字符串；行驶边会追加 "-线路-站点"
                nr = cur_route + append_str

                cand = (nd, nc, nr)
                if cand < best[v]:  # 如果新的路径更优
                    best[v] = cand  # 记录新的路径
                    heapq.heappush(pq, (nd, nc, nr, v))  # 推入堆中

        return None

    '''
    现在DIST也不是直接在“站点图”上跑了，而是在“站点-线路状态图”上跑。

    例如样例 A -> F：

    起点A只有L1，所以起始状态只有 (A, L1)
    初始堆：
    (0, 1, "A", (A,L1))

    - 第一次弹出 (A,L1)
      只能沿L1到 (B,L1)
      更新：
      best[(B,L1)] = (4, 2, "A-L1-B")

    - 第二次弹出 (B,L1)
      可以：
      1) 沿L1继续到 (C,L1)，距离 = 9，路径 "A-L1-B-L1-C"
      2) 若B站存在L1->L3合法换乘，则还能先站内换乘到 (B,L3)，距离仍是4，路径仍是"A-L1-B"

    - 假设B站给了L1<->L3换乘
      弹出 (B,L3) 后，就可以沿L3去 (E,L3)
      更新：
      best[(E,L3)] = (11, 3, "A-L1-B-L3-E")

    - 再从 (E,L3) 如果E站给了L3<->L2合法换乘
      就能先换到 (E,L2)，距离不变仍是11
      再沿L2到F，得到：
      best[(F,L2)] = (14, 4, "A-L1-B-L3-E-L2-F")

    注意：
    如果某个站没有给出 line_a <-> line_b 的换乘记录，
    那么状态图里就没有对应换乘边，DIST也就不能非法换线了。
    这正是你之前丢分的原因。
    '''

# =================== 5.2 最短时间 =====================
# 这个图不是站点图，而是把 state-line 映射为一个 sid，然后在这个状态图上跑最短路
    def shortest_time(src, dst):
        if src == dst:
            return (0, stations[src])

        start_states = []
        for line in station_lines[src]:
            sid = state_id.get((src, line))
            if sid is not None:
                start_states.append(sid)

        if not start_states:
            return None

        INF = (10**30, 10**30, 10**30, "~")
        best = [INF] * S
        pq = []

        # 起点第一次上车不产生换乘时间，所以所有起始线路状态都可以0代价入堆
        for sid in start_states:
            best[sid] = (0, 0, 0, stations[src])  # (总时间, 总距离, 换乘次数, 路径字符串)
            heapq.heappush(pq, (0, 0, 0, stations[src], sid))

        while pq:
            cur_time, cur_dist, cur_trans, cur_route, u = heapq.heappop(pq)
            if (cur_time, cur_dist, cur_trans, cur_route) != best[u]:
                continue

            # 到达终点站的任意线路状态都可以结束
            if state_station[u] == dst:
                return (cur_time, cur_route)

            for v, dt, dd, dc, append_str in graph_time[u]:
                nt = cur_time + dt
                nd = cur_dist + dd
                nc = cur_trans + dc
                nr = cur_route + append_str
                cand = (nt, nd, nc, nr)  # (总时间, 总距离, 换乘次数, 路径字符串)
                if cand < best[v]:
                    best[v] = cand
                    heapq.heappush(pq, (nt, nd, nc, nr, v))

        return None

# ================= 5.3 检测设备部署输出 ===================

    parent = list(range(N))  # 初始每一个站点是自己的根
    rank_ = [0] * N          # 按秩合并

    def find(x):  # 找根
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):  # 合并两个连通块
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        if rank_[ra] < rank_[rb]:
            parent[ra] = rb
        elif rank_[ra] > rank_[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank_[ra] += 1
        return True

# Kruskal思想求一棵生成树
# 这里题目只要求输出任意一棵覆盖全部站点的生成树，不要求最小权生成树
    device_edges = []
    for u, v, line, dist in raw_edges:  # 遍历所有轨道
        if union(u, v):   # 如果u,v当前不连通，就选中这条边
            device_edges.append((u, v, line))

    out = []
    # 对每一个查询，输出最短距离和最短时间
    for i, (src, dst) in enumerate(queries, start=1):
        ans_dist = shortest_distance(src, dst)
        if ans_dist is None:
            out.append(f"RESULT DIST {i} NO_PATH")
        else:
            total_dist, route = ans_dist
            out.append(f"RESULT DIST {i} {total_dist} {route}")

        ans_time = shortest_time(src, dst)
        if ans_time is None:
            out.append(f"RESULT TIME {i} NO_PATH")
        else:
            total_time, route = ans_time
            out.append(f"RESULT TIME {i} {total_time} {route}")

    # 输出设备方案
    out.append(f"RESULT DEVICE {len(device_edges)}")
    for u, v, line in device_edges:
        out.append(f"RESULT DEVICE_EDGE {stations[u]} {stations[v]} {line}")

    # 一次性写入标准输出
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()