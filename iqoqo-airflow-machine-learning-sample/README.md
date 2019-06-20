# iqoqo-airflow-machine-learning-sample

Usage demos for integrating IQOQO platform into an Airflow DAG 

## Pre-requisites

- A previously installed running Airflow environment

## Image classification 

The existing airflow code assumes a simple machine learning alghorithm.

Given an image, the algorithm will, using a substancial probability factor, classify it as either "food" or "not food".

The flow consists of -

* (1) Downloading an existing set of already classified images (food or not food images).

* (2) (For each image set -) Resize the images so their features could be extracted.

* (3) Extract the images' features into compatible .csv files. 

* (4) Build a model that would be able to later classify unknown input as food or not.

* (5) Feed new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food, as mentioned above).

## Integrate IQOQO into the flow

Running the script via airflow without utilizing IQOQO takes ~40 minutes on a strong local machine.

For simplicity's sake, we've chosen to partially integrate IQOQO into the above mentioned flow.
It is available in the `iqoqo_bash_operator.py` file.

The steps which will newly implement IQOQO will have the `-->` prefix below.

The new flow will look like this:

--> * (1) Downloading an existing set of already classified images (food or not food images) (`build_dataset.py`)

--> * (2) Resizing the images. (`build_dataset.py`)

--> * (3) Extract the images' features into compatible .csv files). (`extract_features.py`)

So these stages will be performed simultanously by a few IQOQO agents.

* build a model. (`train.py`)

--> * Feeding new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food). (`predict.py`)

Naturally, each agent will report its results to a different text file.
