def compress():
    # 从用户输入读取字符串
    s = input()
    # 如果输入为空字符串，直接输出空字符串并返回
    if not s:
        print("")
        return
    # 初始化结果列表和计数器
    res = []
    count = 1
    # 记录前一个字符
    prev = s[0]
    # 遍历字符串的剩余部分
    for c in s[1:]:
        # 如果当前字符与前一个字符相同，计数器加一
        if c == prev:
            count +=1
        # 如果当前字符与前一个字符不同，将前一个字符及其计数（如果计数大于一）添加到结果列表
        else:
            res.append(prev + (str(count) if count>1 else ''))
            prev = c
            count = 1
    # 处理最后一个字符序列
    res.append(prev + (str(count) if count>1 else ''))
    # 输出压缩后的字符串
    print(''.join(res))

compress()

