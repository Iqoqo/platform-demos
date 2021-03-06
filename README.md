# Platform-demos

Usage demos for the dis.co platform

## Gender in news

An NLP research of gender appearnces gap in 150,000 publication from 15 different news websites usign the IQOQO distribution framework.
Code is based on an [article by Neal Caren](http://nbviewer.jupyter.org/gist/nealcaren/5105037) and evaluates [all the news](https://www.kaggle.com/snapcrack/all-the-news) dataset

## Compare Machine learning methods

An analysis comparing different Machine learning methods (using the sklearn package).
You can find the original script in the following article: https://pythondata.com/.

The original data from the article is data set contains 416 liver patient records and 167 non liver patient records collected from North East of Andhra Pradesh, India. The “Dataset” column is a class label used to divide groups into liver patient (liver disease) or not (no disease).

In our script the data was replaced with much larger dataset:
http://archive.ics.uci.edu/ml/datasets/hepmass
This data was taken from high-energy physics research.
The search for exotic particles requires sorting through a large number of collisions to find the events of interest. This data set challenges one to detect a new particle of unknown mass.
Machine learning is used in high-energy physics experiments to search for the signatures of exotic particles. These signatures are learned from Monte Carlo simulations of the collisions that produce these particles and the resulting decay products. In each of the three data sets here, the goal is to separate particle-producing collisions from a background source.

## Airflow
A machine learning example using Airflow with Iqoqo. The provided iqoqo bash operator takes an existing public bucket
which contains 5k images, resizes them in a parallel way using Iqoqo, trains a model to distinguish "food" images from
"not food" ones and then proves its abilities by allowing the produced model to runn on an unknown set of images, 
showing which ones are food or not in a high probability factor.

## Celery
A simple example of running a prime number finder in a distributed way using the Celery platform and Iqoqo. The prime finder module splits a range of numbers into sub ranges and runs a prime finder function on them in parallel using Celery. by adding a single line of code the module runs the prime finder function on the sub ranges in parallel using the Iqoqo platform on several machines. This demonstrates the ease, in which users already using Celery to run jobs in parallel, can use the iqoqo platform to run their jobs. 

## DASK

Dask is a library for parallel computing in Python.

Dask is composed of two parts:

    1. Dynamic task scheduling optimized for computation. This is similar to Airflow, Luigi, Celery, 
    or Make, but optimized for interactive computational workloads.
    2. “Big Data” collections like parallel arrays, dataframes, and lists that extend common interfaces 
    like NumPy, Pandas, or Python iterators to larger-than-memory or distributed environments. 
    These parallel collections run on top of dynamic task schedulers.

Research about the options to integrate iqoqo with DASK was done and the summary is detailed in the DASK directory of platform-demos.
There is a working example of a simple use case using DASK with iqoqo.
