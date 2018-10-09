import math
import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt


@lru_cache(maxsize=1024)
def primeFactorization(n):

    prime_factors = []
    # Print the number of two's that divide n
    while n % 2 == 0:
        prime_factors.append(2)
        n = n / 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):

        # while i divides n , print i ad divide n
        while n % i == 0:
            prime_factors.append(i)
            n = n / i

    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        prime_factors.append(n)

    return prime_factors


@lru_cache(maxsize=256)
def Moebius(n):
    if n == 1:
        return 1

    pF = primeFactorization(n)

    if len(set(pF)) == len(pF):
        return (-1)**len(pF)

    return 0


def f(n):
    summation = 0
    rl = [i for i in range(int(n**0.5))]
    for i in rl:
        d = i + 1
        if n % (d * d) == 0:
            summation += Moebius(d)

    return summation


def testing_fn():
    for i in range(1000):
        x = f(i)
        if (x != 0):
            pf = primeFactorization(i)
            print("f(" + str(i) + ") = ", x, "with prime factors ",
                  pf, "and u(" + str(i) + ") = ", Moebius(i))

    sqs = [i for i in [4, 16, 25, 75, 48]]
    for i in sqs:
        print(f(i))


def visualize():
    fs = []
    factor = 9

    for num in range(0, factor * 100):
        temp = f(num)
        fs.append(temp)
        # print(strs)

    # draw fs
    plt.figure(figsize=(15, 5))
    plt.title('Plot')
    plt.xlabel('Index')
    plt.ylabel('u^2(n)')

    temp = str(factor) + '11'
    sp = int(temp)
    for i in range(factor):
        plt.subplot(sp)
        plt.stem([j + 1 + (len(fs) // factor) * i for j in range(len(fs) // factor)],
                 fs[len(fs) // factor * i: (len(fs) // factor) * (i + 1)])
        sp += 1

    plt.show()

# print(primeFactorization.cache_info())
# print(Moebius.cache_info())

# x = Moebius(1)
# print(x)
# x = Moebius(2)
# print(x)
# x = Moebius(6)
# print(x)
# x = Moebius(100)
# print(x)


def EulerPhi(n):
    summation = 0
    for i in range(n):
        m = i + 1
        summation += 1 if math.gcd(m, n) == 1 else 0

    return summation


# invEP_list = set()
# for i in range(20):
#     x = i + 1
#     invEP = 1 / EulerPhi(x)
#     invEP_list.add(invEP)
#     print("EulerPhi(" + str(x) + ") = ", invEP)

# print(len(invEP_list))

visualize()
