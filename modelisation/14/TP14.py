from english_trigrams import trigrams

message = "ZYBAIRUI"

# q1
def trigrammes(str):
    out = []
    for i in range(len(str)-2):
        char = str[i:i+3]
        out.append(char)
    return out

# print(trigrammes("zybairui"))

# q2
def rand_car():
    import numpy as np
    key = np.random.randint(65,91)
    char = chr(key)
    return char
# print(rand_car())

# q3
def proba_trigrams(d):
    total_value = sum(d.values())
    proba_dict = {}
    for key, value in d.items():
        proba_dict[key] = value / total_value
    return proba_dict

# print(proba_trigrams(trigrams))

# q4
def show_top_k(d,k=10):
    out = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]
    return out
# print(show_top_k(proba_trigrams(trigrams)))


# q5
def log_vraiseblance(str):
    tgs = trigrammes(str)
    proba = proba_trigrams(trigrams)
    min_proba = 1/sum(trigrams.values())

    total = 0.0
    for tg in tgs:
        p = proba.get(tg,min_proba)
        import math
        total += math.log(p)
    return total
# print(log_vraiseblance("zybairui"))

# q6
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
perm_init = {c: c for c in alphabet}
# print(perm_id)

# q7
def dechiffrer(str, perm):
    out = ""
    for c in str:
        out += perm[c]
    return out

# q8
def descente(str, perm0, nb_etapes):
    perm = perm0.copy()
    best_log = log_vraiseblance(dechiffrer(str,perm))
    couts = [-best_log]

    for _ in range(nb_etapes):
        #随机选择两个不同字母
        a = rand_car()
        b = rand_car()
        while b == a:
            b = rand_car()

        new_perm = perm.copy()
        new_perm[a], new_perm[b] = new_perm[b], new_perm[a]
        new_log = log_vraiseblance(dechiffrer(str,new_perm))
        if new_log > best_log:
            perm = new_perm
            best_log = new_log

        couts.append(-best_log)

    return perm, couts

# q9
perm_final, couts = descente(message, perm_init, 5000)
texte = dechiffrer(message, perm_final)
print(texte)
