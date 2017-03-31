FROM python:latest

COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt

COPY .hdfscli.cfg /root/

COPY app /srv
WORKDIR  /srv

ENTRYPOINT ["python"]
CMD ["init.py"]
