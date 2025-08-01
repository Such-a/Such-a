import cmath

def function(a, b, c):
    d = (b**2) - (4*a*c)

    option1 = (-b-cmath.sqrt(d))/(2*a)
    option2 = (-b+cmath.sqrt(d))/(2*a)

    return option1, option2

a = 1
b = 5
c = 6
option1, option2 = function(a, b, c)
print('The solutions are {0} and {1}'.format(option1, option2))



