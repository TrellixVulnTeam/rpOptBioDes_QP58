FROM brsynth/rpbase

RUN conda install -y -c anaconda pandas
RUN conda install -y -c anaconda numpy
RUN conda install -y -c anaconda scipy
#RUN conda install -y -c sys-bio pysbol2

RUN git clone https://github.com/SynBioDex/libSBOL.git --recursive
WORKDIR /home/libsbol/
RUN make install
RUN /home/
RUN export PYTHONPATH=$PYTHONPATH:/path-to-your-Python-bindings

RUN git clone https://github.com/SynBioDex/pysbol.git
RUN python pysbol/setup.py install

#RUN pip install pySBOL
#RUN apt install -y python-pip
#RUN pip install pysbol

RUN git clone https://github.com/pablocarb/doebase.git

#COPY rpOptBioDes.py /home/

COPY rpOptBioDes.py /home/


#RUN git clone https://github.com/SynBioDex/libSBOL.git --recursive
