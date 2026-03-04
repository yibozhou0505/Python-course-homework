n = int(input())  # 将输入的数字转换为整数
i = 2  # 定义一个整型变量i，初始值为2
factors = {}  # 定义一个字典factors，用于存储因数及其指数
while i * i <= n:  # 循环条件为i的平方小于等于n
    while n % i == 0:  # 当n能被i整除时
        factors[i] = factors.get(i, 0) + 1  # 若factors中已有i，则指数加1；
        n = n // i  # 除以i，继续循环
    i += 1  # 否则，i加1，继续循环
if n > 1:  # 若n大于1，则将其加入factors中
    factors[n] = 1  # 指数为1
result = []  # 定义一个列表result，用于存储因数的字符串表示
for factor, exp in factors.items():  # 遍历factors中的键值对
    if exp == 1:  # 若指数为1，则直接输出因数
        result.append(f"{factor}")  # 因数的字符串表示
    else:  # 否则
        result.append(f"{factor}^{exp}")    # 因数的字符串表示加上指数
print("*".join(result))  # 将因数的字符串表示用*连接
