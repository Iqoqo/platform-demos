FROM python:3.7
RUN apt-get update && apt-get install -y \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*
ADD ./requirements.txt .
RUN pip install -r requirements.txt