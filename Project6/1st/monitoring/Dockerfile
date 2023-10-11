FROM python:3.7

WORKDIR /app

RUN pip install requests psutil

COPY cpu_mem_test_client.py /app/cpu_mem_test_client.py

EXPOSE 5321
CMD ["python3", "/app/cpu_mem_test_client.py"]