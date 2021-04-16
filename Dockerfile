# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /api
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 main:app