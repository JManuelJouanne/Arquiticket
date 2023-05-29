FROM python:3.11.1

WORKDIR /worker/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .