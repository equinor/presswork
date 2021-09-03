FROM python:3

RUN python3 -m pip install JustifyText
RUN python3 -m pip install pyhyphen
RUN python3 -m pip install flask

ADD app /app
WORKDIR /app

RUN addgroup -S -g 1000 presswork
RUN adduser -S -u 1000 -G presswork presswork
USER 1000

ENTRYPOINT ["python3"]
CMD ["app.py"]
