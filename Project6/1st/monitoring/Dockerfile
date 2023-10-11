FROM python:3.8

WORKDIR /app

# RUN pip install psutil requests

COPY cpu_mem_test_client.py /app/cpu_mem_test_client.py

EXPOSE 5321
CMD ["python3", "/app/cpu_mem_test_client.py"]

