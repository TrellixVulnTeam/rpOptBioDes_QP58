#!/usr/bin/python

import argparse
import sys

sys.path.insert(0, '/home/')
import rpToolServe

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to call OptBioDes using rpSBML')
    parser.add_argument('-inputTar', type=str)
    parser.add_argument('-outputTar', type=str)
    parser.add_argument('-pathway_id', type=str)
    parser.add_argument('-maxVariants', type=int, default=5)
    parser.add_argument('-libSize', type=int, default=48)
    parser.add_argument('-inputParts', type=str)
    params = parser.parse_args()
    if params.inputParts=='None' or params.inputParts=='' or params.inputParts=='none':
        inputParts = None
    else:
        inputParts = params.inputParts
    rpToolServe.runOptBioDes_hdd(params.inputTar,
                                 params.outputTar,
                                 params.pathway_id,
                                 params.maxVariants,
                                 params.libSize,
                                 inputParts)
