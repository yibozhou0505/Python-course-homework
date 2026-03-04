positive_count = 0
negative_count = 0
odd_count = 0
even_count = 0

while True:
    num = int(input())
    if num == 0:
        break
    if num > 0:
        positive_count += 1
    elif num < 0:
        negative_count += 1
    if num % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

# even_count = even_count + 1
print(f"正数: {positive_count}, 负数: {negative_count}, 奇数: {odd_count}, 偶数: {even_count}")

