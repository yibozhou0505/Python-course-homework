import sys
import os

SUBMIT_DIR = "/coursegrader/submit"
OUTPUT_FILE = os.path.join(SUBMIT_DIR, "output.txt")


def insert_path(tree, path):
    parts = path.strip().split("/")
    cur = tree
    for name in parts:
        if name not in cur:
            cur[name] = {}
        cur = cur[name]


def dfs(tree, depth, lines):
    for name, child in tree.items():
        lines.append("  " * depth + name)
        dfs(child, depth + 1, lines)


def main():
    data = sys.stdin.read().splitlines()
    if not data:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            pass
        return

    n = int(data[0].strip())
    paths = [data[i + 1].rstrip("\n") for i in range(n)]

    paths.sort()

    root = {}
    for path in paths:
        insert_path(root, path)

    lines = []
    dfs(root, 0, lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":
    main()