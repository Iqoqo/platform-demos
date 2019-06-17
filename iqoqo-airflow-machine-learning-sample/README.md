# iqoqo-airflow-machine-learning-sample

Usage demos for integrating IQOQO platform into an Airflow installation

## Image classification 

The existing airflow code assumes a simple machine learning alghorithm.

Given an image, the algorithm will, in a large probabily, classify it as "food" or "not food".

The flow consists of -

* Downloading an existing set of already classified images (food or not food images).

* Resizing the images.

* Extract the images' features into compatible .csv files). 

* build a model that would be able to later classify unknown input as food or not.

* Feeding new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food).

## Compare Machine learning methods

Running the script via airflow without utilizing IQOQO takes ~40 minutes on a strong local machine.

For simplicity's sake, we've chosen to partially integrate IQOQO into the above mentioned flow.
It is available in the `iqoqo_bash_operator.py` file.

The new flow will look like this:

--> * Downloading an existing set of already classified images (food or not food images) (`build_dataset.py`)
+
--> * Resizing the images. (`build_dataset.py`)

--> * Extract the images' features into compatible .csv files). (`extract_features.py`)

So these stages will be performed simultanously by a few IQOQO agents.

* build a model. (`train.py`)

--> * Feeding new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food). (`predict.py`)

Naturally, each agent will report its results to a different text file.
