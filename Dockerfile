FROM ubuntu:19.10

RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y git

RUN pip install pysbol numpy pandas scipy
RUN git clone https://github.com/pablocarb/doebase.git

WORKDIR /home/

COPY rpOptBioDes.py /home/
