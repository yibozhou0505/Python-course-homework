n, p = int(input("importer un entier positif n: ")), int(input("Enter a power p: "))
def get_sommation_k_power_p(n, p)->int:
    if n < 0 or p < 0:
        raise ValueError("n and p must be positive integers.")
    return sum(k**p for k in range(1, n + 1))

print(get_sommation_k_power_p(n, p))