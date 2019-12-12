#FROM brsynth/rpbase
FROM conda/miniconda2

RUN conda install -y -c anaconda pandas
RUN conda install -y -c anaconda numpy
RUN conda install -y -c anaconda scipy
#RUN conda install -y -c sys-bio pysbol2

RUN apt-get update && apt-get install -y git
RUN pip install pysbol numpy pandas scipy python-libsbml

RUN conda install -c conda-forge backports.tempfile
RUN conda install -c conda-forge backports.lzma
#RUN conda install -c auto pylzma
#RUN pip install pylzma tempfile
#RUN apt-get install -y liblzma-dev
#RUN pip install backports.tempfile
#RUN pip install pylzma
#RUN pip install backports.lzma


#RUN git clone https://github.com/SynBioDex/pysbol.git
#RUN python pysbol/setup.py install

#RUN pip install pysbol

WORKDIR /home/
COPY rpOptBioDes.py /home/

RUN git clone https://github.com/pablocarb/doebase.git

#COPY rpOptBioDes.py /home/
