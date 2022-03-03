FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /project
RUN mkdir /project/mystery
WORKDIR /project/mystery
COPY requirements.txt /project/mystery
#COPY . /project/mystery
RUN pip install -r requirements.txt
ADD . /project/mystery
