import dask
from dask import compute, delayed
from dask_func import inc, double, add
from iqoqo import iqoqo_job


data = range(5)

output = []
for x in data:
    a = dask.delayed(inc)(x)
    b = dask.delayed(double)(x)
    c = dask.delayed(add)(a, b)
    output.append(c)

total = dask.delayed(sum)(output)
print(total.compute())