FROM qi-base:latest
ADD common.tar.gz /app/qi
ADD server.tar.gz /app/qi
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/qi/server/requirements.txt
WORKDIR /app/qi/server
RUN chmod 755 ./*
ENTRYPOINT [ "./docker-entrypoint.sh" ]
