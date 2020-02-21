FROM python:3.8.1-alpine3.11

# Install make with Alpine Linux package manager
RUN apk add make

COPY . /var/app/
WORKDIR /var/app/docs

RUN pip install -r requirements.txt

# Keep container running
CMD tail -f /dev/null
