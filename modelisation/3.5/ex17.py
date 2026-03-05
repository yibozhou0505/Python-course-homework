c = str(input("Enter a character: "))
def lettres_consecutives_id(texte)->bool:
    for i in range(len(texte)-1):
        if texte[i] == texte[i+1]:
           return True
    return False

print(lettres_consecutives_id(c))   
