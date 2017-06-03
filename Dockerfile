FROM ubuntu:latest

MAINTAINER Zach Loubier "zloubier1@gmail.com"

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev

RUN pip install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]