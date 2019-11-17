FROM brsynth/rpbase

RUN pip install -y numpy pandas scipy pysbol

RUN git clone https://github.com/pablocarb/doebase.git

#COPY rpOptBioDes.py /home/
