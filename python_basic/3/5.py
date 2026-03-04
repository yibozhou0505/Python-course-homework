def evaluate():
    # 定义一个栈用于存储操作数
    stack = []
    # 从输入中读取并分割表达式为标记列表
    tokens = input().split()
    # 遍历每个标记
    for token in tokens:  
        # 如果标记是运算符，则从栈中弹出两个操作数进行计算，并将结果压入栈中
        if token in '+-*/':
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))
        # 如果标记是操作数，则将其转换为整数并压入栈中
        else:
            stack.append(int(token))
    # 输出最终计算结果
    print(stack.pop())
evaluate()
