FROM python:3.8.1-alpine3.11

# Install make with Alpine Linux package manager
RUN apk add make

RUN pip install -U sphinx==2.4.1 sphinx-rtd-theme

COPY . /var/app/
WORKDIR /var/app/docs

# Keep container running
CMD tail -f /dev/null
