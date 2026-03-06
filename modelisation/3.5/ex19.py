s, m = map(str, input("Importer deux chaînes de caractères s et m: ").split())

def est_suffixe(s, m)-> bool:
    return m.endswith(s)

print(est_suffixe(s, m))