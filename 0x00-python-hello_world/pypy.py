#!/usr/bin/python3
# str = "Holberton School"
# print(f"{str*3}\n{str[:8]}\n")
#5-print

#6-concatinate

# str1 = "Holberton"
# str2 = "School"
# str={str1} + " " +{str2}
# print(f"Welcome to {str}!")

#7-edges

# word = "Holberton"
# word_first_3 = word[:3]
# word_last_2 = word[-2:]
# middle_word = word[1:-1]

# 8-concaat_edges
# str = "Python is an interpreted, interactive, object-oriented programming\
#          language that combines remarkable power with very clear syntax"
# str1=str[39:66] + " "
# str2=str[115:119] + " "
# str3=str[:6] + " "

# print(f"{str1}{str2}{str3}")

#9-The zen of Python, 

"""
This is the "example" module.

The example module supplies one function, factorial().  For example,

>>> factorial(5)
120
"""

def factorial(n):
    """Return the factorial of n, an exact integer >= 0.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000
    >>> factorial(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 0

    Factorials of floats are OK, but the float must be an exact integer:
    >>> factorial(30.1)
    Traceback (most recent call last):
        ...
    ValueError: n must be exact integer
    >>> factorial(30.0)
    265252859812191058636308480000000

    It must also not be ridiculously large:
    >>> factorial(1e100)
    Traceback (most recent call last):
        ... 
    OverflowError: n too large
    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod( verbose = True)
   
    