FROM python:3.6

RUN apt-get update && apt-get install --quiet --yes git

RUN pip install pandas numpy scipy sklearn pysbol python-libsbml flask flask_restful

WORKDIR home

RUN git clone –branch v1.2 https://github.com/pablocarb/doebase.git

COPY rpTool.py /home/
COPY rpToolServe.py /home/

ENTRYPOINT ["python"]
CMD ["/home/rpToolServe.py"]

# Open server port
EXPOSE 8888
