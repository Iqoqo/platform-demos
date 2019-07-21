from iqoqo import iqoqo_job

@iqoqo_job
def inc(x):
    return x + 1

@iqoqo_job
def double(x):
    return x + 2

@iqoqo_job
def add(x, y):
    return x + y
