
def fibonacci_series():
    a, b = 0, 1
    while a < 100:
        if a >= 0:
            print(a)
        a, b = b, a + b

fibonacci_series()
