n = int(input("importer un entier n: "))
def fibo(n)->int:
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    elif n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        a, b = 1, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
print(f"F({n}) = {fibo(n)}")