FROM alpine:3.9
RUN apk update
RUN apk add python3 python3-dev mariadb-dev build-base
RUN apk add linux-headers
RUN mkdir -p /app/qi
ADD requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
