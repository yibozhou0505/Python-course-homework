x = input("demandez un nombre reel: ")
def return_abs(x):
    if x < 0:
        return -x
    else:
        return x
print(return_abs(float(x)))