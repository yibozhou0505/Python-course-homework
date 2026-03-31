def get_tick_level(position: int, n: int) -> int:
    """
    计算给定位置的刻度级别
    这里的 position 指的是两个最大刻度之间的中间刻度位置（从 0 开始）
    """
    if n <= 1:
        return 0

    total = (1 << (n - 1)) - 1
    if position < 0 or position >= total:
        return 0

    mid = total // 2
    if position == mid:
        return n - 1
    if position < mid:
        return get_tick_level(position, n - 1)
    return get_tick_level(position - mid - 1, n - 1)


def draw_interval(level: int) -> None:
    if level == 0:
        return
    draw_interval(level - 1)
    print("-" * level)
    draw_interval(level - 1)


def draw_ruler(n: int, length: int) -> None:
    """
    绘制标尺
    """
    for i in range(length + 1):
        print("-" * n + " " + str(i))
        if i < length:
            draw_interval(n - 1)


def main():
    line = input().strip()
    parts = line.split()
    n = int(parts[0])
    length = int(parts[1])

    draw_ruler(n, length)


if __name__ == "__main__":
    main()