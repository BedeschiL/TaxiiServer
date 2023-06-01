FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3-pip net-tools nano

COPY /app/requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY ./app/ /app

WORKDIR /app

CMD ["python3", "api.py"]


