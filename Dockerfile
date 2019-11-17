FROM brsynth/rpbase

RUN conda install -y -c anaconda pandas
RUN conda install -y -c anaconda numpy
RUN conda install -y -c anaconda scipy
#RUN conda install -y -c sys-bio pysbol2

RUN git clone https://github.com/SynBioDex/pysbol.git
RUN python pysbol/setup.py install

#RUN pip install pysbol

RUN git clone https://github.com/pablocarb/doebase.git

#COPY rpOptBioDes.py /home/
