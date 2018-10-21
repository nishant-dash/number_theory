import math
from functools import lru_cache
import matplotlib.pyplot as plt
import csv
import webbrowser
import os


class primeFactorsObject():
    def __init__(self):
        self.largest_factor = 0
        self.smallest_factor = math.inf
        self.num_factors = 0
        self.prime_factors = {}
        self.number = 1

    def add_factor(self, x):
        if x not in self.prime_factors:
            self.prime_factors[x] = 1
        else:
            self.prime_factors[x] += 1

        self.num_factors += 1

        if x < self.smallest_factor:
            self.smallest_factor = x

        if x > self.largest_factor:
            self.largest_factor = x

        self.number *= x

    def remove_factor(self, x):
        if x in self.prime_factors:
            if self.prime_factors[x] == 1:
                del self.prime_factors[x]
            else:
                self.prime_factors[x] -= 1
        else:
            return

        self.num_factors -= 1
        if self.num_factors == 0:
            return

        pF = list(self.prime_factors)
        if x == self.smallest_factor:
            self.smallest_factor = min(pF)

        if x == self.largest_factor:
            self.largest_factor = max(pF)

        self.number = int(self.number / x)

    def print_info(self):
        print("Prime factors of ", self.number, " are ")
        for k, v in self.prime_factors.items():
            print('  ', k, ' with exponent ', v)
        print()


# uncomment lru_cache code line if factorial is going to be used
# multiple times with posiibly same input
# @lru_cache(maxsize=64)
def factorial(n):
    f = 1
    for i in range(n):
        f *= (i + 1)
    return f


@lru_cache(maxsize=1024)
def primeFactorization(n):
    prime_factors = []

    while n % 2 == 0:
        prime_factors.append(2)
        n >>= 1

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            prime_factors.append(i)
            n /= i

    if n > 2:
        prime_factors.append(n)

    return prime_factors


@lru_cache(maxsize=1024)
def primeFactorization_condensed(n):
    prime_factors = primeFactorsObject()

    while n % 2 == 0:
        prime_factors.add_factor(2)
        n >>= 1

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            prime_factors.add_factor(i)
            n /= i

    if n > 2:
        prime_factors.add_factor(n)

    return prime_factors


@lru_cache(maxsize=256)
def Moebius(n):
    if n == 1:
        return 1

    pF = primeFactorization(n)

    if len(set(pF)) == len(pF):
        return (-1)**len(pF)

    return 0


def char_fn_square(n):
    summation = 0
    rl = [i for i in range(int(math.sqrt(n)))]

    for i in rl:
        d = i + 1
        if n % (d * d) == 0:
            summation += Moebius(d)

    return summation


def testing_fn():
    for i in range(1000):
        x = char_fn_square(i)
        if (x != 0):
            pf = primeFactorization(i)
            print("f(" + str(i) + ") = ", x, "with prime factors ",
                  pf, "and u(" + str(i) + ") = ", Moebius(i))

    sqs = [i for i in [4, 16, 25, 75, 48]]
    for i in sqs:
        print(char_fn_square(i))


def EulerPhi(n):
    unique_pF = set(primeFactorization(n))
    prod = n

    for i in unique_pF:
        prod *= ((i - 1) / (i))

    return int(prod)


def visualize():
    fs = []
    factor = 9

    for num in range(0, factor * 100):
        temp = char_fn_square(num)
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


def desmos():
    data = [Moebius(i + 1) for i in range(100)]
    with open('to_plot.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    csvfile.close()
    data = [EulerPhi(i + 1) for i in range(100)]
    with open('to_plot2.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    csvfile.close()

    webbrowser.open('file://' + os.path.realpath('parabola.html'))


# deprecated function, too slow
# def EulerPhi_old(n):
#     summation = 0

#     for i in range(n):
#         m = i + 1
#         summation += 1 if math.gcd(m, n) == 1 else 0

#     return summation


# invEP_list = set()
# for i in range(20):
#     x = i + 1
#     invEP = 1 / EulerPhi(x)
#     invEP_list.add(invEP)
#     print("InvEulerPhi(" + str(x) + ") = ", invEP)

desmos()
