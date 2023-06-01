FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3-pip net-tools nano

COPY /src/requirements.txt /src/
RUN pip3 install -r /src/requirements.txt

COPY src/ /src

WORKDIR /src

CMD ["python3", "api.py"]



