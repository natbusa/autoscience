FROM python:latest

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

COPY app /srv
WORKDIR  /srv

ENTRYPOINT ["python"]
CMD ["app.py"]
