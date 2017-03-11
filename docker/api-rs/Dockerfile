FROM python:latest

COPY requirements.yml /
RUN pip install -r requirements.yml

COPY app /application
WORKDIR  /application

ENTRYPOINT ["python"]
CMD ["app.py"]
