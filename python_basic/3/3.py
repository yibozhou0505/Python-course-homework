

class CheckIsValid:
    def __init__(self):
        self.stack = []
        self.check_map = {")": "(", "]": "[", "}": "{"}
        self.valid = True

    def add(self, char):
        if not self.valid:
            return
        if char in self.check_map.values():
            self.stack.append(char)
        elif char in self.check_map:
            if not self.stack or self.stack[-1] != self.check_map[char]:
                self.valid = False
            else:
                self.stack.pop()

    def is_valid(self):
        return self.valid and len(self.stack) == 0

s = CheckIsValid()
input_str = input().strip()
for char in input_str:
    s.add(char)
print(s.is_valid())







