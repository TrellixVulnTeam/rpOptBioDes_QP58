#!/bin/sh

docker run -d -p 8888:8888 --name test_rpOptBioDes brsynth/rpoptbiodes
python tool_rpOptBioDes.py -inputTar test_input.tar -outputTar test_output.tar -pathway_id rp_pathway -maxVariants 45 -libSize 102 -inputParts None -server_url http://0.0.0.0:8888/REST
docker kill test_rpOptBioDes
docker rm test_rpOptBioDes
