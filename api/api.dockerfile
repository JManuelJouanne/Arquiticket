FROM python:3.11.1

WORKDIR /api/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .