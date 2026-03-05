a,b = str(input("Enter two strings separated by a space: ")).split()
def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strings must be of the same length.")
    
    count = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            count += 1
    
    return count

print(distance(a, b))
