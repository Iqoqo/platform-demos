from math import sqrt
from itertools import count, islice
from iqoqo import iqoqo_job

# A function for checking if a number is prime
def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))

@iqoqo_job # uncomment this to run on iqoqo platform
def find_primes(start_range, end_range):
    return [n for n in range(start_range, end_range) if is_prime(n)]

