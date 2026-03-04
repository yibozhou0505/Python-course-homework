class StringReverser:
    def __init__(self, input_str):
        self.words = input_str.strip().split()

    def reverse(self):
        return ' '.join(reversed(self.words))

# 读取输入并处理
user_input = input().strip()
reverser = StringReverser(user_input)
print(reverser.reverse())