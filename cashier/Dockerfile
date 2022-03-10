FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /project
RUN mkdir /project/cashier
WORKDIR /project/cashier
COPY requirements.txt /project/cashier
RUN pip install -r requirements.txt
ADD . /project/cashier
