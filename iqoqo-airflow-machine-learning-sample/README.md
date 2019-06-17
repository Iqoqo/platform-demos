# iqoqo-airflow-machine-learning-sample

Usage demos for integrating IQOQO platform into an Airflow installation

## Image classification 

The existing airflow code assumes a simple machine learning alghorithm.

Given an image, the algorithm will, in a large probabily, classify it as "food" or "not food".

The flow consists of -

* Downloading an existing set of already classified images (food or not food images).

* Resizing the images.

* Running them through a model (extracting their features into compatible .csv files).

* Feeding new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food).

## Compare Machine learning methods

Running the script via airflow without utilizing IQOQO takes ~40 minutes on a strong local machine.

For simplicity's sake, we've chosen to partially integrate IQOQO into the above mentioned flow.

The new flow will look like this:

--> * Downloading an existing set of already classified images (food or not food images)
+
--> * Resizing the images. 

So these stages will be performed simultanously by a few IQOQO agents.

* Running them through a model (extracting their features into compatible .csv files).

--> * Feeding new "unknown" input images to the built model in order to sort the input into one of the classes (food or not food).

Naturally, each agent will report its results to a different text file.
