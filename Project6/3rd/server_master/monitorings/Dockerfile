FROM python:3.8

RUN pip install psutil requests

ADD .

EXPOSE 6432
CMD ["python3", "cpu_mem_client_sunny.py"]

