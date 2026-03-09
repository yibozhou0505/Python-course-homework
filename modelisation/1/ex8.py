n = int(input("Enter a number: "))
def factorial(n)->int:
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
print(factorial(n))

n, p = int(input("importer un entier n: ")), int(input("importer autre entier p: "))
def C_n_p(n, p)->int:
    if p > n:
        raise ValueError("p must be less than or equal to n.")
    return factorial(n) // (factorial(p) * factorial(n - p))
print(C_n_p(n, p))