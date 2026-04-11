import sys
import os

SUBMIT_DIR = "/coursegrader/submit"
OUTPUT_FILE = os.path.join(SUBMIT_DIR, "output.txt")


def build_path_to_root(node, parent):
    path = []
    while node != -1:
        path.append(node)
        node = parent.get(node, -1)
    return path  # 从当前节点一路到根


def path_between(u, v, parent):
    # u->root
    path_u = build_path_to_root(u, parent)
    # v->root
    path_v = build_path_to_root(v, parent)

    set_u = set(path_u)

    # 找LCA：v向上第一个出现在u祖先链里的点
    lca = None
    for x in path_v:
        if x in set_u:
            lca = x
            break

    # u -> lca
    part1 = []
    cur = u
    while cur != lca:
        part1.append(cur)
        cur = parent[cur]
    part1.append(lca)

    # lca -> v
    part2 = []
    cur = v
    while cur != lca:
        part2.append(cur)
        cur = parent[cur]
    part2.reverse()

    return part1 + part2


def main():
    data = sys.stdin.read().strip().splitlines()
    if not data:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            pass
        return

    idx = 0
    n = int(data[idx].strip())
    idx += 1

    children = {}
    parent = {}

    start = None

    for i in range(n):
        root, c1, c2, c3 = map(int, data[idx].split())
        idx += 1
        if i == 0:
            start = root  # 第一组结点信息中的第一个编号就是起点
        children[root] = [c1, c2, c3]
        for c in [c1, c2, c3]:
            if c != -1:
                parent[c] = root

    parent[start] = -1

    m = int(data[idx].strip())
    idx += 1

    customers = []
    for _ in range(m):
        target, priority = map(int, data[idx].split())
        idx += 1
        customers.append((priority, target))

    # 按优先级从小到大排序
    customers.sort()

    targets = [target for priority, target in customers]

    lines = []
    cur = start

    for target in targets:
        path = path_between(cur, target, parent)
        lines.append(" ".join(map(str, path)))
        cur = target

    # 最后返回起点
    path = path_between(cur, start, parent)
    lines.append(" ".join(map(str, path)))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":
    main()