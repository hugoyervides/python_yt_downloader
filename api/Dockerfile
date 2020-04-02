FROM tiangolo/meinheld-gunicorn-flask:python3.6-alpine3.8

#Enviroment Variables
ENV LISTEN_PORT 8080
ENV WORKERS_PER_CORE 3
ENV LOG_LEVEL debug

EXPOSE 8080

# Copy requirements file for PIP
COPY requirements.txt /tmp/

#Install FMPEG for mp3 convertion
RUN apk add --no-cache ffmpeg

# Upgrade pip and install the requirements file
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# Copy the app code and gunicorn config file
COPY ./app /app
