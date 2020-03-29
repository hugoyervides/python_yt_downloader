FROM tiangolo/meinheld-gunicorn-flask:python3.7

ENV LISTEN_PORT 8080

EXPOSE 8080

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy over our app code
COPY ./app /app

# set an environmental variable, MESSAGE,
# which the app will use and display
ENV MESSAGE "Youtube Downloader API Started"
