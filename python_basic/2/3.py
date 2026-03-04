num1 = list(map(int, input().split()))
num2 = list(map(int, input().split()))

nums = num1 + num2
nums.sort()

for i in nums:
    print(i, end=' ')
