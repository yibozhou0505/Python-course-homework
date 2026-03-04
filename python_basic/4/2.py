result = []
data = [1, 3, 5]
def test():
    global result
    def helper():
        global data
        data = [i + 1 for i in data]
        for num in data:
            if num % 2 == 0:
                result.append(num)
    helper()
    return result
test()
print(result)