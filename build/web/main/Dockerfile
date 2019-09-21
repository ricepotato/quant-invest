FROM web-base:latest
ADD web.tar.gz /app
WORKDIR /app/web
RUN chmod 755 ./*
ENTRYPOINT [ "./docker-entrypoint.sh" ]
