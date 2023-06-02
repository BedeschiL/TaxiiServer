FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3-pip

COPY /src/requirements.txt /TaxiiServer/src/


RUN pip3 install -r /TaxiiServer/src/requirements.txt

COPY src/ /TaxiiServer/src

WORKDIR /TaxiiServer

ENV PYTHONPATH="${PYTHONPATH}:/TaxiiServer/src/"

CMD ["python3", "src/API/api.py"]



