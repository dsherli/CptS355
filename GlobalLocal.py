z = 10


def inc(x):
    print("inc:", locals())
    return x + z


# print(inc(10))


def outer():
    y = None
    z = 2
    print("outer:", locals())
    y = 35
    print(z)
    # print(inc(10))


outer()
print(z)
