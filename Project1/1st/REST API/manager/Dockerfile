FROM python:3.7

RUN pip install Flask 
RUN mkdir /app
WORKDIR /app
ADD . /app/

EXPOSE 5000
CMD ["python", "/app/app.py"]

