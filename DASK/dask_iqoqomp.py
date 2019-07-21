import sys
sys.path.insert(0,"/Users/etalhod/Documents/iqoqomp")
import dask
# from multiprocessing.pool import Pool
import os
from iqoqomp.pool import Pool
from iqoqo import iqoqo_job
from dask import compute, delayed

os.environ['IQOQO_LOGIN_USER'] = 'user@iqoqo.co'
os.environ['IQOQO_LOGIN_PASSWORD'] = '12345678'

mypool = Pool(5)

# dask.config.set(pool=Pool(5))
dask.config.set(pool=mypool)


def do_something(x): return x * x

data = range(1000)
delayed_values = [delayed(do_something)(x) for x in data]
results = compute(*delayed_values, scheduler='processes')

