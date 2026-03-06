x = float(input("Enter a number: "))

PI = 3.14159265358979323846
x = x % (2*PI)
if x > PI:
    x -= 2*PI

if x > PI/2:
    x = PI - x
elif x < -PI/2:
    x = -PI - x

term = x
sin_x = x
n = 1

while abs(term) > 1e-15:
    term *= -x * x / ((2*n)*(2*n+1))
    sin_x += term
    n += 1
if abs(sin_x) < 1e-6:
    sin_x = 0.0


print(f"{sin_x:.6f}")

