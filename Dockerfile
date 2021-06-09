FROM python:3

RUN python3 -m pip install JustifyText
RUN python3 -m pip install pyhyphen
RUN python3 -m pip install flask

ADD app /app
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
