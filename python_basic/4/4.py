def fibonacci(n):
    if n == 0 or n == 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def process_fibonacci(k):
    return [fibonacci(i) for i in range(k)]

def final_operation(lst):
    return sum(lst)

print(final_operation(process_fibonacci(6)))
