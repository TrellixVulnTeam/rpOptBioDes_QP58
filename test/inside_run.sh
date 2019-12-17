#!/bin/bash

python tool_rpOptBioDes.py -inputTar test_input.tar -outputTar test_output.tar -pathway_id rp_pathway -maxVariants 45 -libSize 48 -inputParts None

mv test_output.tar results/
