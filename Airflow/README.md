# Airflow

Usage demos for integrating IQOQO platform into an Airflow DAG.

## Pre-requisites

- A running Airflow [installation](https://airflow.apache.org/installation.html) (see `https://airflow.apache.org/installation.html`)
- An active, registered IQOQO account (sign up at `https://app.iqoqo.co/signup`)
- IQOQO's CLI installed (in your bash: `curl https://s3.us-east-2.amazonaws.com/iqoqo.cli/install.sh | sh`)

*****Note: if you're on a Mac, and you receive 
`ValueError: unknown locale: UTF-8 in Python`
When running the bash operator, add to your bash both where you run the scheduler and the airflow web server:

`export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8`

## Image classification 

The existing airflow code assumes a simple machine learning alghorithm.
(Images for this implementation sample are on a public S3 bucket)

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

Naturally, each agent working on a different set of images will report its results to a different text file.
