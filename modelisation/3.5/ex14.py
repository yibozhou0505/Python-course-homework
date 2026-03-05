s = str(input("Enter a string: "))
VOYELLES = "aeiouyAEIOUY"
def count_voyelles(s):
    count = 0
    for C in s:
        if C in VOYELLES:
            count += 1
    return count

print(count_voyelles(s))