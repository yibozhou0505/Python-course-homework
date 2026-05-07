import sys
from bisect import bisect_left, bisect_right

# 分块大小：700~1000 通常比较稳
B = 800
INF_ID = 10 ** 30


class SortedBlocks:
    def __init__(self):
        self.blocks = []
        self.maxes = []
        self.n = 0

    def _rebuild_max(self, i):
        self.maxes[i] = self.blocks[i][-1]

    def insert(self, key):
        blocks = self.blocks
        maxes = self.maxes

        if not blocks:
            blocks.append([key])
            maxes.append(key)
            self.n = 1
            return

        i = bisect_left(maxes, key)

        if i == len(blocks):
            i -= 1
            block = blocks[i]
            block.append(key)
        else:
            block = blocks[i]
            pos = bisect_left(block, key)
            block.insert(pos, key)

        self.n += 1

        if len(block) > 2 * B:
            mid = len(block) // 2
            new_block = block[mid:]
            del block[mid:]

            blocks.insert(i + 1, new_block)
            maxes[i] = block[-1]
            maxes.insert(i + 1, new_block[-1])
        else:
            maxes[i] = block[-1]

    def discard(self, key):
        blocks = self.blocks
        maxes = self.maxes

        if not blocks:
            return

        i = bisect_left(maxes, key)
        if i == len(blocks):
            return

        block = blocks[i]
        pos = bisect_left(block, key)

        if pos == len(block) or block[pos] != key:
            return

        block.pop(pos)
        self.n -= 1

        if block:
            maxes[i] = block[-1]
        else:
            blocks.pop(i)
            maxes.pop(i)

    def rank_query(self, l, r):
        """
        查询排名 [l, r]，排名从 1 开始。
        """
        if l > self.n:
            return ""

        if r > self.n:
            r = self.n

        start = l - 1
        need = r - l + 1

        blocks = self.blocks
        i = 0

        # 找到 start 所在块
        while i < len(blocks):
            blen = len(blocks[i])
            if start < blen:
                break
            start -= blen
            i += 1

        ans = []

        while i < len(blocks) and need > 0:
            block = blocks[i]
            take = min(len(block) - start, need)

            for neg_score, pid in block[start:start + take]:
                ans.append(f"{pid}:{-neg_score}")

            need -= take
            i += 1
            start = 0

        return " ".join(ans)

    def score_query(self, low, high):
        """
        查询分数在 [low, high] 内的玩家。
        排序仍然按当前排名升序输出。

        key = (-score, id)

        score in [low, high]
        等价于：
        -score in [-high, -low]
        """
        if self.n == 0:
            return ""

        lo = (-high, -1)
        hi = (-low, INF_ID)

        blocks = self.blocks
        maxes = self.maxes

        i = bisect_left(maxes, lo)
        if i == len(blocks):
            return ""

        ans = []

        while i < len(blocks):
            block = blocks[i]

            if block[0] > hi:
                break

            if i == bisect_left(maxes, lo):
                left = bisect_left(block, lo)
            else:
                left = 0

            right = bisect_right(block, hi)

            if left < right:
                for neg_score, pid in block[left:right]:
                    ans.append(f"{pid}:{-neg_score}")

            if right < len(block):
                break

            i += 1

        return " ".join(ans)


def main():
    input = sys.stdin.buffer.readline
    write = sys.stdout.write

    first = input()
    if not first:
        return

    q = int(first)

    scores = {}
    board = SortedBlocks()

    out = []

    for _ in range(q):
        parts = input().split()
        if not parts:
            continue

        op = parts[0]

        if op == b'U':
            pid = int(parts[1])
            score = int(parts[2])

            old = scores.get(pid)

            # 如果分数没变，排名也不会变，直接跳过有序表操作
            if old == score:
                continue

            if old is not None:
                board.discard((-old, pid))

            scores[pid] = score
            board.insert((-score, pid))

        elif op == b'R':
            l = int(parts[1])
            r = int(parts[2])
            out.append(board.rank_query(l, r))

        else:  # b'S'
            low = int(parts[1])
            high = int(parts[2])
            out.append(board.score_query(low, high))

        # 分批输出，避免结果列表过大
        if len(out) >= 512:
            write("\n".join(out) + "\n")
            out.clear()

    if out:
        write("\n".join(out))


if __name__ == "__main__":
    main()