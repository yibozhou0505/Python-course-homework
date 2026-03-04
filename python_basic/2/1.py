numbers = list(map(int, input().split()))

max_diff = 0

for i in range(len(numbers) - 1):

    diff = numbers[i + 1] - numbers[i]

    if diff > max_diff:

        max_diff = diff

print(max_diff)