FROM python:3.11.1

WORKDIR /subscriber/

ENV HOST passline.iic2173.net
ENV PORT 9000
ENV USER_MQTT students
ENV PASSWORD iic2173-2023-1-students
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .