n_raw = int(input())
n = n_raw
factorial = 1
while True:
    if n > 0:
        factorial *= n
        n -= 1
        if n == 0:
            break
    else:
        print("输入错误，请重新输入！")
        break
print(f"{n_raw}! = {factorial}")

