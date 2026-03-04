y = 20
def test():
    y = 25
    def inner():
        global y
        y = 30
    inner()
    return y
test()
print(y)