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
        self.unique_factors = set()
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

        self.unique_factors.add(x)

    def remove_factor(self, x):
        if x in self.prime_factors:
            if self.prime_factors[x] == 1:
                del self.prime_factors[x]
            else:
                self.prime_factors[x] -= 1
        else:
            return

        if x not in self.prime_factors:
            self.unique_factors.remove(x)

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
    if n <= 1:
        return n

    pF = primeFactorization(n)

    if len(set(pF)) == len(pF):
        return (-1)**len(pF)

    return 0


def something(n):
    summation = 0
    rl = [i + 1 for i in range(int(math.sqrt(n)))]

    for i in rl:
        d = i + 1
        if n % (d * d) == 0:
            summation += Moebius(d)

    return summation


# returns true if a number is squarefull
def is_a_squarefull_number(n):
    pF = primeFactorization_condensed(n)
    for k, v in pF:
        if v < 2:
            return False

    return True

# returns true if a number is squarefree


def is_a_squarefree_number(n):
    pF = primeFactorization_condensed(n)
    for k, v in pF:
        if v >= 2:
            return False

    return True


def testing_fn():
    for i in range(1000):
        x = something(i)
        if (x != 0):
            pf = primeFactorization(i)
            print("f(" + str(i) + ") = ", x, "with prime factors ",
                  pf, "and u(" + str(i) + ") = ", Moebius(i))

    sqs = [i for i in [4, 16, 25, 75, 48]]
    for i in sqs:
        print(something(i))


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
        temp = something(num)
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
    # data = [Moebius(i) for i in range(1, 1000)]
    data = [-1 * Moebius(int((2**(i - 1))**2)) for i in range(0, 10)]
    with open('to_plot12.txt', 'w') as csvfile:
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


def char_fn_squarefree(n):
    if is_a_squarefree_number(n):
        return 1
    return 0


def num_sqfull_lessthanx(x):
    sqfull = 0
    num = x
    for i in range(num):
        if is_a_squarefull_number(i + 1):
            sqfull += 1
    # print("Number of squarefull numbers less than ", num, " is ", sqfull)
    return sqfull


def b(num):
    s = 0
    for b in range(1, int(num**(1 / 3))):
        if is_a_squarefree_number(b):
            temp = char_fn_squarefree(b)
            # if temp == 1:
            #     print(b, end=' \n')
            s += temp
    # print("Summation of u^2(squarefree numbers less than ",
          # int(num**(1 / 3)) + 1, ") is ", s)
    return s


# desmos()


# def main_ans(x, a):
#     # odd numbers less than x/a
#     count = 0
#     for i in range(0, (x // a) + 1):
#         even = i % 2 == 0
#         if not even:
#             # print(i, end=' ')
#             count += 1
#     # print(" count is ", count)
#     return count


# def check(x, a):
#     # print(' and ', (x + a) // (2 * a))
#     # return (x + a) // (2 * a)
#     return (x // a - 1) // 2 + 1


# val = True
# for a in range(3, 100):
#     for x in range(1, 125):
#         if (x < a):
#             continue
#         else:
#             val &= main_ans(x, a) == check(x, a)
# print(val)

def omega(n):
    return len(primeFactorization_condensed(n).unique_factors)


def special_omega(n):
    return 2 ** omega(n)


def d(n):
    count = 0
    for i in range(1, n + 1):
        if n % i == 0:
            count += 1
    return count


def d_alt(n):
    p = 1
    x = primeFactorization_condensed(n).prime_factors
    for k, v in x.items():
        p *= (v + 1)
    return p
# main_ans(10, 3)


def sum_of_div(n):
    p = 1
    x = primeFactorization_condensed(n).prime_factors
    for k, v in x.items():
        p *= ((-1 / (k**(v))) + k) / (k - 1)
    return p


def perfect_number(p):
    # if p not prime, throw and error
    return (2**(p - 1)) * ((2**p) - 1)


# desmos()
num = [2, 3, 5, 7, 11, 13, 17, 19]
for i in num:
    print(perfect_number(i))
# print(d_alt())
print(sum_of_div(num))
