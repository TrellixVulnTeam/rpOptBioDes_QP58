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


def main(inputfile,
         input_format,
         input_sbol,
         output,
         pathway_id,
         max_variants,
         lib_size,
         input_parts):
    """The docker call to calculate the design of experiment combination of genetic parts

    :param inputfile: The path to the input file
    :param input_format: The input type of the gile. Suported input: tar, sbml
    :param input_sbol: The path to the input SBOL file
    :param output: The path to the output file
    :param pathway_id: The Groups id of the heterologous pathway (Default: rp_pathway)
    :param max_variants: Maximum number of genes selected per step (Default: 5)
    :param lib_size: Desired size of the combinatorial library (Default: 32)
    :param input_parts: The file with a URI list of sbol parts in Synbiohub (Default: None)

    :type inputfile: str
    :type input_sbol: str
    :type output: str
    :type pathway_id: str
    :type max_variants: int
    :type lib_size: int 
    :type input_parts: str

    :rtype: bool
    :return: The success or failure of the function
    """
    docker_client = docker.from_env()
    image_str = 'brsynth/rpoptbiodes-standalone'
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
        if os.path.exists(inputfile) and os.path.exists(input_sbol):
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
            err_str = err.decode('utf-8')
            if 'ERROR' in err_str:
                print(err_str)
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output.dat'):
                print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
            else:
                shutil.copy(tmpOutputFolder+'/output.dat', output)
            container.remove()
        else:
            logging.error('Cannot find one or more of the input file: '+str(inputfile))
            logging.error('Cannot find one or more of the input file: '+str(input_sbol))
            exit(1)


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
