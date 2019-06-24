from celery import Celery
from math import sqrt
from itertools import count, islice
from iqoqo import iqoqo_job, set_credentials
import os

"""
This module holds the Celery task
The task accepts two numbers and finds all the primes numbers between the two numbers
"""

# Defining the celery app, using RabbitMQ as the message broker and RPC as backend for getting the results
app = Celery('prime_finder_task', backend='rpc://', broker='amqp://guest:guest@localhost//')
# These environment variables should be defined in your environment  or iqoqo
# file and are defined here for simplicity
os.environ['IQOQO_EMAIL'] = 'enter your email here'
os.environ['IQOQO_PASSWORD'] = 'place your password here'


# A function for checking if a number is prime
def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n) - 1)))


# Defining this function as a celery task
@app.task
# @iqoqo_job # uncomment this to run on iqoqo platform
def find_primes(start_range, end_range):
    return [n for n in range(start_range, end_range) if is_prime(n)]
