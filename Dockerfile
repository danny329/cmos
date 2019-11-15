FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /cmos
WORKDIR /cmos

RUN apt-get update &&  apt-get install -y

COPY requirements.txt /cmos/

RUN pip3 install -r requirements.txt

COPY . /cmos/
