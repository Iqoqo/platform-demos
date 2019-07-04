# Simple Iqoqo Airflow integration example
Demo for integrating IQOQO platform into a Airflow installation

## Pre-requisites
- A running Airflow [installation](https://airflow.apache.org/installation.html) (see `https://airflow.apache.org/installation.html`)
- An active, registered IQOQO account (sign up at `https://app.iqoqo.co/signup`)

- In your bash:
`export IQOQO_EMAIL=<Your IQOQO Email credentials>`
`export IQOQO_PASSWORD= <Your IQOQO Password credentials>`

*****Note: if you're on a Mac, and you receive 
`ValueError: unknown locale: UTF-8 in Python`
When running the operator via operator, add to your bash:

`export LC_ALL=en_US.UTF-8`

and

`export LANG=en_US.UTF-8`

## The example
The example finds and prints prime numbers inside a given range.
The sample airflow DAG file (`iqoqo_python_operator`) distributes the range between multiple IQOQO workers.

## Running the example on your local machine
- Add both python files to your Airflow's installation DAGS folders. (`~/airflow/dags/`)
- Trigger `iqoqo_python_operator` from the UI or from the bash.
 
 
 