FROM python:3.9.18-alpine
WORKDIR /usr/src/app

RUN apk add libmodbus

ADD solis.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./solis.py"]