FROM python:3.11.1

WORKDIR /api/

COPY api_requirements.txt .
RUN pip3 install -r api_requirements.txt

COPY . .