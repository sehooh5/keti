FROM python:3.8

WORKDIR /app

RUN pip install psutil requests subprocess

ADD ./monitoring /app/

EXPOSE 6432
CMD ["python3", "/app/cpu_mem_test_client.py"]

