FROM alpine:3.9
RUN apk add uwsgi
RUN apk add python3
RUN mkdir /app/qi
ADD server.tar.gz /app/qi
RUN pip install -r /app/qi/server/requirements.txt
WORKDIR /app/qi/server
ENTRYPOINT ["./docker-entrypoint.sh"]