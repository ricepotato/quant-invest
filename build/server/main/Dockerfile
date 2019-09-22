FROM server-base:latest
ADD server.tar.gz /app
ADD common.tar.gz /app/server
ADD data.tar.gz /app/server
RUN chmod 755 ./*
ENTRYPOINT [ "./docker-entrypoint.sh" ]

