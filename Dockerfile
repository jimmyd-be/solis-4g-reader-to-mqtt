FROM python:3-alpine3.17
WORKDIR /usr/src/app

ADD solis.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD [“python”, “./solis.py”]