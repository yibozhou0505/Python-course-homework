import os


class StackEmptyError(Exception):
    pass


class StackFullError(Exception):
    pass


class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if not self.data:
            raise StackEmptyError("栈已空")
        return self.data.pop()

    def clear(self):
        self.data.clear()

    def empty(self):
        return len(self.data) == 0

    def __len__(self):
        return len(self.data)


def parse_command(line):
    line = line.strip()  # 去掉两端空白
    if not line.startswith("(") or not line.endswith(")"):
        return None, None
    content = line[1:-1]
    parts = content.split(",")
    if len(parts) != 2:
        return None, None
    op = parts[0].strip()
    try:
        mem = int(parts[1].strip())
    except Exception:
        return None, None
    return op, mem


def process_case(case_name, max_memory, commands):
    undo_stack = Stack()
    redo_stack = Stack()

    # 为了支持“超内存时删最早操作”，额外维护顺序表
    active_ops = []  # [(name, mem), ...]

    current_mem = 0

    for op, mem in commands:
        if op == "undo":
            try:
                if not active_ops:
                    raise StackEmptyError("栈已空")
                last = undo_stack.pop()
                redo_stack.push(last)
                if active_ops:
                    removed = active_ops.pop()
                    current_mem -= removed[1]
            except StackEmptyError:
                pass

        elif op == "redo":
            try:
                item = redo_stack.pop()
                name, need_mem = item
                # 恢复前先检查内存，若不够就像普通操作一样淘汰最早项
                while current_mem + need_mem > max_memory and active_ops:
                    old = active_ops.pop(0)
                    current_mem -= old[1]
                if current_mem + need_mem > max_memory:
                    raise StackFullError("栈已满")
                undo_stack.push(item)
                active_ops.append(item)
                current_mem += need_mem
            except (StackEmptyError, StackFullError):
                pass

        else:
            # 普通操作：清空 redo
            redo_stack.clear()

            # 超出内存就删除最早操作
            while current_mem + mem > max_memory and active_ops:
                old = active_ops.pop(0)
                current_mem -= old[1]

            try:
                if current_mem + mem > max_memory:
                    raise StackFullError("栈已满")
                item = (op, mem)
                undo_stack.push(item)
                active_ops.append(item)
                current_mem += mem
            except StackFullError:
                pass

    lines = []
    if not active_ops:
        lines.append(f"{case_name}: ")
    else:
        for name, mem in active_ops:
            lines.append(f"{case_name}: {name}")
    return lines


def solve_all_cases(lines):
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        if line.startswith("=== CASE"):
            case_name = line.replace("===", "").strip().lower().replace(" ", "_")
            i += 1

            while i < len(lines) and (not lines[i].strip() or lines[i].strip().startswith("#")):
                i += 1
            if i >= len(lines):
                break

            max_memory = int(lines[i].strip())
            i += 1

            commands = []
            while i < len(lines):
                now = lines[i].strip()
                if now.startswith("=== CASE"):
                    break
                if now and (not now.startswith("#")):
                    op, mem = parse_command(now)
                    if op is not None:
                        commands.append((op, mem))
                i += 1

            results.extend(process_case(case_name, max_memory, commands))
        else:
            i += 1

    return results



def main():
    input_path = "/coursegrader/testdata/cases.txt"
    output_path = "/coursegrader/submit/hw5_q2.txt"

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        lines = []

    results = solve_all_cases(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")


if __name__ == "__main__":
    main()