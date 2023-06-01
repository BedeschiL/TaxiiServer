FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3-pip net-tools nano

COPY /requirements.txt /app/
RUN pip3 install -r /src/requirements.txt

COPY src/ /app

WORKDIR /app

CMD ["python3", "api.py"]



