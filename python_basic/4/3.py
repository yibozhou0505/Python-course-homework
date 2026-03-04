total = 0
def recursive_sum(num):
    global total
    if num == 0:
        return
    total += num
    recursive_sum(num-1)

recursive_sum(5)
print(total)