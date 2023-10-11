FROM python:3.8

WORKDIR /app

RUN pip3 install psutil requests json

COPY cpu_mem_test_client.py /app/cpu_mem_test_client.py

EXPOSE 5321
CMD ["python3", "/app/cpu_mem_test_client.py"]