# Grab the python-3.7 image
FROM python:3.7

# maintainer stuff
LABEL maintainer='emilianomarcheserc@gmail.com'

# Add requirements and install dependencies
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/app/
WORKDIR /opt/app

CMD python ingest.py