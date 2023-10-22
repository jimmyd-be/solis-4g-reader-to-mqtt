FROM python:3.9.18-alpine
WORKDIR /usr/src/app

ADD solis.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./solis.py"]