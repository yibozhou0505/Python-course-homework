import sys
import os

SUBMIT_DIR = "/coursegrader/submit"
OUTPUT_FILE = os.path.join(SUBMIT_DIR, "output.txt")


def main():
    data = sys.stdin.read().strip().splitlines()
    if not data:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            pass
        return

    n = int(data[0].strip())
    children = {}
    all_nodes = set()
    child_nodes = set()

    for i in range(1, n + 1):
        root, left, mid, right = map(int, data[i].split())
        children[root] = [left, mid, right]
        all_nodes.add(root)
        for c in [left, mid, right]:
            if c != -1:
                child_nodes.add(c)

    root = (all_nodes - child_nodes).pop()

    best_node = None
    best_visit = None
    best_branch = -1
    best_depth = -1
    visit_idx = 0

    sys.setrecursionlimit(20000)

    def dfs(u, depth):
        nonlocal best_node, best_visit, best_branch, best_depth, visit_idx
        if u == -1:
            return

        visit_idx += 1
        cur_visit = visit_idx
        branch_cnt = sum(1 for x in children[u] if x != -1)

        # 1. 子分支数大
        # 2. 深度更大
        # 3. 前序更早 -> 如果前两项都相同，不更新
        if (branch_cnt > best_branch) or (branch_cnt == best_branch and depth > best_depth):
            best_branch = branch_cnt
            best_depth = depth
            best_node = u
            best_visit = cur_visit

        left, mid, right = children[u]
        dfs(left, depth + 1)
        dfs(mid, depth + 1)
        dfs(right, depth + 1)

    dfs(root, 0)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"{best_node} {best_visit}\n")


if __name__ == "__main__":
    main()