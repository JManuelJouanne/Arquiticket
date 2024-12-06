FROM python:3.11.1

WORKDIR /job_master/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .