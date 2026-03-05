a, b, r, x, y = map(float, input("Importer a, b, r, x, y: ").split())
def is_inside_circle(a, b, r, x, y)->bool:
    return (x - a) ** 2 + (y - b) ** 2 < r ** 2
print(is_inside_circle(a, b, r, x, y))