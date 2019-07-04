from math import sqrt
from itertools import count, islice
from iqoqo import iqoqo_job

def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))

# Adding this decorator utilizes using iqoqo
@iqoqo_job
def find_primes(start_range, end_range):
    return [n for n in range(start_range, end_range) if is_prime(n)]

