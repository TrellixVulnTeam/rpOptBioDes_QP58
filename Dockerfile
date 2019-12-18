FROM brsynth/rpbase
#FROM conda/miniconda2

RUN conda install -y -c anaconda pandas
RUN conda install -y -c anaconda numpy
RUN conda install -y -c anaconda scipy
#RUN conda install -y -c sys-bio pysbol2

RUN pip install pysbol python-libsbml sklearn

RUN apt-get update && apt-get install -y git
#RUN conda install -c conda-forge backports.tempfile
#RUN conda install -c conda-forge backports.lzma
#RUN pip install pylzma tempfile
#RUN apt-get install -y liblzma-dev
#RUN pip install backports.tempfile
#RUN pip install pylzma
#RUN pip install backports.lzma


#RUN git clone https://github.com/SynBioDex/pysbol.git
#RUN python pysbol/setup.py install

#RUN pip install pysbol
#RUN pip install pylzma
#RUN pip install backports.tempfile
#RUN conda install -c auto pylzma
#RUN apt-get install -y liblzma-dev
#RUN pip install pylzma
#RUN pip install backports.lzma

RUN git clone https://github.com/pablocarb/doebase.git

COPY rpTool.py /home/
COPY rpToolServe.py /home/
#COPY /test/test_input.tar /home/


#COPY rpOptBioDes.py /home/
