#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Galaxy script to query rpOptBioDes REST service

"""

import requests
import argparse
import json
import logging


##
#
#
def rpOptBioDesUpload(inputTar,
                      outputTar,
                      pathway_id,
                      maxVariants,
                      libSize,
                      inputParts,
                      server_url):
    if inputParts=='None' or inputParts=='' or inputParts=='none':
        inputParts = None
    # Post request
    data = {'pathway_id': pathway_id,
            'maxVariants': maxVariants,
            'libSize': libSize,
            'inputParts': inputParts}
    files = {'inputTar': open(inputTar, 'rb'),
             'data': ('data.json', json.dumps(data))}
    r = requests.post(server_url+'/Query', files=files)
    r.raise_for_status()
    with open(outputTar, 'wb') as ot:
        ot.write(r.content)


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to call OptBioDes using rpSBML')
    parser.add_argument('-inputTar', type=str)
    parser.add_argument('-outputTar', type=str)
    parser.add_argument('-pathway_id', type=str)
    parser.add_argument('-maxVariants', type=int, default=5)
    parser.add_argument('-libSize', type=int, default=102)
    parser.add_argument('-inputParts', type=str)
    parser.add_argument('-server_url', type=str)
    params = parser.parse_args()
    rpOptBioDesUpload(params.inputTar,
                      params.outputTar,
                      params.pathway_id,
                      params.maxVariants,
                      params.libSize,
                      params.inputParts,
                      params.server_url)
