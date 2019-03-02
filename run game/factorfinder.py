def factorfinder(value):
    from numpy import sqrt
    value = float(value)
    factors = []
    bigfactors = []
    i = 1
    while i < sqrt(value):
        if value/i == int(value/i):
            factors.append(i)
            bigfactors = [int(value/i)] + bigfactors
        i += 1
    if sqrt(value) == int(sqrt(value)):
        factors.append(int(sqrt(value)))
    factors = factors + bigfactors
    return factors

