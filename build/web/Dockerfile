FROM qi-base:latest
ADD common.tar.gz /app/qi
ADD web.tar.gz /app/qi
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/qi/web/qiweb/requirements.txt
WORKDIR /app/qi/web/qiweb
RUN chmod 755 ./*
#ENTRYPOINT [ "./docker-entrypoint.sh" ]
