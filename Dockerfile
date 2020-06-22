FROM python:3.6

RUN apt-get update && apt-get install --quiet --yes git

RUN pip install pandas numpy scipy sklearn pysbol python-libsbml

WORKDIR home

RUN git clone -b v1.2 https://github.com/pablocarb/doebase.git

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY galaxy/code/tool_rpOptBioDes.py /home/
