FROM python:3.8

WORKDIR /app

COPY . /app/

RUN pip install psutil requests

EXPOSE 6432
CMD ["python3", "/app/cpu_mem_client_sunny.py"]

