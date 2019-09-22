FROM qi-base:latest
RUN apk update
RUN apk add nginx
RUN apk add uwsgi
RUN apk add uwsgi-python3
RUN rm /etc/nginx/conf.d/default.conf
ADD qi_web.conf /etc/nginx/conf.d
ADD nginx.conf /etc/nginx
RUN adduser -D -g 'www' www
RUN mkdir /app
ADD requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
WORKDIR /app/server
