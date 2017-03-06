FROM python:latest

COPY requirements.yml /
RUN pip install -r requirements.yml

COPY app /app
WORKDIR  /app

ENTRYPOINT ["python"]
CMD ["app.py"]