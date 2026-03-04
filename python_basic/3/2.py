class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

# 测试代码
q = Queue()
for word in input("").split():
    q.enqueue(word)
while not len(q.items) == 0:
    print(q.dequeue(), end=" ")