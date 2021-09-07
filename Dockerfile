FROM python:3

RUN python3 -m pip install JustifyText
RUN python3 -m pip install pyhyphen
RUN python3 -m pip install flask

ADD app /app
WORKDIR /app

RUN addgroup --gid 1000 presswork
RUN adduser --uid 1000 --group presswork presswork
USER 1000

ENTRYPOINT ["python3"]
CMD ["app.py"]
