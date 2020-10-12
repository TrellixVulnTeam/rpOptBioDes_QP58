#!/usr/bin/env python3
'''
#!/usr/bin/python
'''
import sys
sys.path.insert(0, '/home/')

import argparse
import sys
import tempfile

import rpToolServe

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Python wrapper to call OptBioDes using rpSBML')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-input_sbol', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-pathway_id', type=str, default='rp_pathway')
    parser.add_argument('-max_variants', type=int, default=5)
    parser.add_argument('-lib_size', type=int, default=102)
    parser.add_argument('-input_parts', type=str, default=None)
    params = parser.parse_args()
    if params.input_parts=='None' or params.input_parts=='' or params.input_parts=='none' or params.input_parts==None:
        input_parts = None
    else:
        input_parts = params.input_parts
    if params.input_format=='tar':
        rpToolServe.runOptBioDes_hdd(params.input,
                                     params.input_sbol,
                                     params.output,
                                     params.pathway_id,
                                     params.max_variants,
                                     params.lib_size,
                                     input_parts)
    elif params.input_format=='sbml':
        #make the tar.xz 
        with tempfile.temporarydirectory() as tmpoutputfolder:
            input_tar = tmpoutputfolder+'/tmp_input.tar.xz'
            output_tar = tmpoutputfolder+'/tmp_output.tar.xz'
            with tarfile.open(input_tar, mode='w:xz') as tf:
                #tf.add(params.input)
                info = tarfile.tarinfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                info.size = os.path.getsize(params.input)
                tf.addfile(tarinfo=info, fileobj=open(params.input, 'rb')) 
            rpToolServe.runOptBioDes_hdd(input_tar,
                                         params.input_sbol,
                                         output_tar,
                                         params.pathway_id,
                                         params.max_variants,
                                         params.lib_size,
                                         input_parts)
            with tarfile.open(output_tar) as outtar:
                outtar.extractall(tmpoutputfolder)
            out_file = glob.glob(tmpoutputfolder+'/*.xml')
            if len(out_file)>1:
                logging.warning('there are more than one output file...')
            shutil.copy(out_file[0], params.output)
    else:
        logging.error('Cannot interpret the format input: '+str(params.input_format))
