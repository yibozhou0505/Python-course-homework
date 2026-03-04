class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items != []:
            return self.items.pop()  # 错误代码
        else:
            return "栈已空"
# 输入测试代码
s = Stack()
for num in map(int, input("").split()):
    s.push(num)
for _ in range(4):
    print(s.pop())
