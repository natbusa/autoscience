FROM python:latest

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

ADD .hdfscli.cfg /root/
ADD data /data

COPY app /srv
WORKDIR  /srv

ENTRYPOINT ["python"]
CMD ["app.py"]
