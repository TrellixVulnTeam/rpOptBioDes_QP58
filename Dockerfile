FROM python:3.6

RUN apt-get update && apt-get install --quiet --yes git

RUN pip install pandas numpy scipy sklearn pysbol python-libsbml

WORKDIR home

RUN git clone https://github.com/pablocarb/doebase.git

COPY rpTool.py /home/
COPY rpToolServe.py /home/

ONBUILD ENTRYPOINT ["python"]
ONBUILD CMD ["/home/rpToolServe.py"]

# Open server port
ONBUILD EXPOSE 8888
