# DASK integration

The following is a summary of the reaserch done about DASK integration.

## About DASK

Transparently handles the brokerage of large datasets

Transparently handles the distribution to workers 

#Two relevant approaches:

#“processes” (using multiprocessing)
Over ~80% of the use cases
#“Distributed” (define a cluster object and pass it to Dask)
Less than ~20% of the use cases
e.g. Dask-YARN handles with clusters but we don’t need this extra layer.

## Attempt with “processes”

Naively we could use iqoqomp instead of multiprocessing (see dask_iqoqomp.py for a sample).
Problem is that DASK has it built-in internally.

Many features are not implemented in iqoqomp.pool (by design).
Using “processes” approach, Dask.compute() expects a complete Pool object and relies on the internal copy of multiprocessing which has additional substantial functionalities.
This approach is rather single-machine-oriented and strongly hardcoded there for that reason.
It could be solved with some adaptations on their side, but this is why they have the “distributed” architecture, so I doubt they will accept any change we may come with.


## Distributed

It is not the most frequent use case because it is “more complex” for random users.
--> Need direct access to the cluster
        --> Dask provides some interfaces with Amazon / Google /… clouds
        --> Example with YARN(irrelevant for us but just to make a point)
            --> It provides the entire machinery that we provide, including the definition of the cluster
If we go that way, we need to write a wrapper that returns the iqoqo “cluster” as a one-liner (like YARN do).

Estimate the implementation to require ~4 weeks at least.

## “Delayed”

One more very esoteric use case, that strips-off most of Dask advantages.
when the usual data structures cannot be used, user has some control on the parallelisation.

Useful for strange data structures and for complex inter-process dependencies.

Small demo (dask_delayed.py) using the iqoqo sdk demonstrates the point but
    --> we have to force no dependencies
    --> We have to force non-Dask data structures

This approach has no advantage on simply using iqoqomp and it does not exploit any of the main features of DASK.

The dependencies wont work in this example on ANY (remote) cluster.
