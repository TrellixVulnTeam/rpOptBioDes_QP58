#!/usr/bin/env python3
"""
Created on March 17 2020

@author: Melchior du Lac
@description: rpOptBioDes

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(inputfile,
         input_format,
         input_sbol,
         output,
         pathway_id,
         max_variants,
         lib_size,
         input_parts)
    docker_client = docker.from_env()
    image_str = 'brsynth/rpoptbiodes-standalone:dev'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        shutil.copy(inputfile, tmpOutputFolder+'/input.dat')
        shutil.copy(input_sbol, tmpOutputFolder+'/input_sbol.dat')
        command = ['python /home/tool_rpOptBioDes.py',
                   '-input',
                   '/home/tmp_output/input.dat',
                   '-input_format',
                   str(input_format),
                   '-input_sbol',
                   '/home/tmp_output/input_sbol.dat',
                   '-output',
                   '/home/tmp_output/output.dat',
                   '-pathway_id',
                   str(pathway_id),
                   '-max_variants',
                   str(max_variants),
                   '-lib_size',
                   str(lib_size),
                   '-input_parts',
                   str(input_parts)]
        container = docker_client.containers.run(image_str,
												 command,
												 detach=True,
                                                 stderr=True,
                                                 remove=True,
												 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        print(err)
        shutil.copy(tmpOutputFolder+'/output.dat', outputTar)
        container.remove()



##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Convert the results of RP2 and rp2paths to SBML files')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-input_sbol', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-pathway_id', type=str, default='rp_pathway')
    parser.add_argument('-max_variants', type=int, default=5)
    parser.add_argument('-lib_size', type=int, default=102)
    parser.add_argument('-input_parts', type=str, default=None)
    params = parser.parse_args()
    main(params.input,
         params.input_format,
         params.input_sbol,
         params.output,
         params.pathway_id,
         params.max_variants,
         params.lib_size,
         params.input_parts)
