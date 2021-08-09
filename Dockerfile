FROM python:3.7-slim

RUN apt update
RUN apt-get install libgomp1 -y

RUN pip install --upgrade pip
RUN python3 --version

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
COPY app.py /app/
COPY src/ /app/src/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

CMD exec gunicorn -b :$PORT -w 4 app:app