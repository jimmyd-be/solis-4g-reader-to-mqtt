FROM python:alpine3.17
ADD solis.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD [“python”, “./solis.py”]