#FROM brsynth/rpbase
FROM ubuntu:19.10

#RUN conda install -y -c anaconda pandas
#RUN conda install -y -c anaconda numpy
#RUN conda install -y -c anaconda scipy
#RUN conda install -y -c sys-bio pysbol2

RUN apt-get update
RUN apt-get install -y python-pip
RUN apt-get install -y git

#RUN git clone https://github.com/SynBioDex/pysbol.git
#RUN python pysbol/setup.py install

RUN pip install pysbol numpy pandas scipy
RUN git clone https://github.com/pablocarb/doebase.git

#COPY rpOptBioDes.py /home/
