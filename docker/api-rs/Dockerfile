FROM python:latest

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY app /srv
WORKDIR  /srv

ENTRYPOINT ["python"]
CMD ["app.py"]
