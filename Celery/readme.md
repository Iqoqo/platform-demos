# Iqoqo Celery example
Usage demos for integrating IQOQO platform into a Celery runner

## Pre-requisites
In order to run this example you will need the following:
- RabbitMQ installed and running
- Celery installed and running 

You can use this [manual](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html) to help you with the installation

## The example
In this example we will show how to find the prime numbers in a given range 
by distributing the range between multiple workers. We will achieve that by using Celery as a job queue manager.
Later we will show how to run it using the Iqoqo platform and distribute the jobs to machines.

## Running the example on your local machine
- First start by running the Celery worker
  - open a terminal
  - Go to the Celery folder
  - Enter ```celery -A prime_finder_task worker -P eventlet --loglevel=info```
  - Your worker will start running, if you encounter any issues please refer to the Celery installation section
- Run prime_finder_parallel, this will use celery to split the task between multiple workers on your machine
 
 ## Running the example on the iqoqo platform
 - In the prime_finder_parallel.py file add your Iqoqo credentials
 - Start the Celery worker as described in the previous section (if it is already running restart it)
 - Uncomment the ```@iqoqo_job``` line
 - Run prime_finder_parallel.py. the tasks will now run on your Iqoqo account. 
 You can check their progress in your account dashboard
 
 ## Next steps
 - Unleash the full power of Celery and Iqoqo by running different celery [workflows](https://docs.celeryproject.org/en/latest/userguide/canvas.html) with Iqoqo
 - Try distributing over different machines to optimize your workflow
 
 ## Limitations
 - The script must be contained in a single file. Including other modules is not working currently.
 - Including global modules will work if running in venv only or providing a docker container
 
 