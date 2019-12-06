FROM ubuntu:19.10

RUN apt-get update
#RUN apt-get install -y python3
#RUN apt-get install -y python3-pip
RUN apt-get install -y python-pip
RUN apt-get install -y git
RUN apt-get install -y liblzma-dev

#RUN pip3 install pysbol numpy pandas scipy python-libsbml
RUN pip install pysbol numpy pandas scipy python-libsbml
RUN pip install backports.tempfile
#RUN pip install pylzma
RUN pip install backports.lzma

WORKDIR /home/

COPY rpOptBioDes.py /home/
RUN git clone https://github.com/pablocarb/doebase.git
