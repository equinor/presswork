FROM debian:latest

RUN apt update
RUN apt install -y python3 python3-pip
RUN python3 -m pip install JustifyText
RUN python3 -m pip install flask

VOLUME /app
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
