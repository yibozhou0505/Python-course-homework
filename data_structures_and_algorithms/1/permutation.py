chars = ["h", "n", "o", "p", "t", "y"]
used = [0]*len(chars)
selected = []

def permu():
    if len(selected) == len(chars):
        print("".join(selected))
        return
    for i in range(len(chars)):
        if used[i] == 0:
            used[i] = 1
            selected.append(chars[i])

            permu()

            selected.pop()
            used[i] = 0
permu()

        

