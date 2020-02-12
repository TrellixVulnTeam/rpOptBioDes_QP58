import sys
sys.path.insert(0, '/home/')

import tempfile
import logging
import glob
import tarfile
import libsbml
#import subprocess
import os
import io

import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api

import rpTool

## run using HDD 3X less than the above function
#
#
#def runOptBioDes_hdd(input_tar, output_tar, pathway_id='rp_pathway', max_variants=5, lib_size=32, input_parts=None):
def runOptBioDes_hdd(input_tar, input_sbol, output_tar, pathway_id='rp_pathway', max_variants=5, lib_size=32, input_parts=None):
    """ - lib_size: desired size of the combinatorial library,
        - max_variants: maximum number of genes selected per step
        - input_parts: file with a URI list of sbol parts in Synbiohub
    """
    if input_parts=='None' or input_parts=='none' or input_parts=='N':
        input_parts = None
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            with tempfile.TemporaryDirectory() as tmpPartsFolder:
                #tar = tarfile.open(fileobj=input_tar, mode='r')
                tar = tarfile.open(fileobj=input_tar, mode='r')
                tar.extractall(path=tmpInputFolder)
                tar.close()
                for sbml_path in glob.glob(tmpInputFolder+'/*'):
                    fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '').replace('.rpsbml', '')
                    selenzyme_info = rpTool.readRPpathway_selenzyme(libsbml.readSBMLFromFile(sbml_path), pathway_id)
                    ##### PABLO ####
                    # Prepare input files: geneparts.csv, refparts.csv
                    genes = rpTool.selenzinfo2table(selenzyme_info, max_variants)
                    gene_parts = os.path.join(tmpPartsFolder, 'GeneParts.csv')
                    genes.to_csv(gene_parts, index=False)
                    if input_parts is None:
                        refs = rpTool.refparts_default()
                        ref_parts = os.path.join(tmpPartsFolder, 'RefParts.csv')
                        refs.to_csv(ref_parts,index=False)
                    # Run DoE and retrieve SBOL and diagnostics
                    try:
                        #diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, lib_size)
                        diagnostics = rpTool.doeGetSBOL(pfile=ref_parts, gfile=gene_parts, libsize=lib_size, gsbol=input_sbol)
                    except:
                        logging.error('Error detected error in rpTool.doeGetSBOL for '+str(sbml_path))
                        continue
                    #diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, lib_size)
                    #diagnostics = doeGetSBOL(ref_parts, gene_parts, size)
                    '''
                    data = {'M': diagnostics['M'].tolist(),
                            'J': diagnostics['J'],
                            'pow': diagnostics['J'],
                            'rpv': diagnostics['J'],
                            'names': diagnostics['names'],
                            'lib_size': diagnostics['lib_size'],
                            'seed': diagnostics['seed'],
                            'sbol': diagnostics['sbol']}
                    '''
                    open(tmpOutputFolder+'/'+fileName, 'w').write(diagnostics['sbol'])
                    #TODO: need to include the efeciecy information inside the SBOL directly
                    '''
                    with open(tmpOutputFolder+'_info.txt', 'w') as text_file:
                        text_file.write('Size: '+str(diagnostics['lib_size'])+'\n')
                        text_file.write('Efficiency:'+str(diagnostics['J'])+'\n')
                    '''
                    #Here you can insert what you need to do, or build a larger dictionnary for all the pathways. FileName
                    #is the name of the pathway ex: rp_1_1
                    #NOTE: this is retro so the first reaction is RP{highest} and the last reaction in the pathway is RP{lowest}
                    # the dictionnary should be like the following:
                    ################
                with tarfile.open(fileobj=output_tar, mode='w:xz') as ot:
                    for sbol_path in glob.glob(tmpOutputFolder+'/*'):
                        fileName = sbol_path.split('/')[-1].replace('.sbml','').replace('.xml','').replace('.sbol','')
                        outFileName = fileName+'.sbol.xml'
                        info = tarfile.TarInfo(outFileName)
                        info.size = os.path.getsize(sbol_path)
                        ot.addfile(tarinfo=info, fileobj=open(sbol_path, 'rb'))
                    for parts_path in glob.glob(tmpPartsFolder+'/*'):
                        info = tarfile.TarInfo(parts_path.split('/')[-1])
                        info.size = os.path.getsize(parts_path)
                        ot.addfile(tarinfo=info, fileobj=open(parts_path, 'rb'))


#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


def stamp(data, status=1):
    appinfo = {'app': 'rpOptBioDes', 'version': '1.0',
               'author': 'Melchior du Lac',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """ REST App."""
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


class RestQuery(Resource):
    """ REST interface that generates the Design.
        Avoid returning numpy or pandas object in
        order to keep the client lighter.
    """
    def post(self):
        input_tar = request.files['input_tar']
        input_sbol = request.files['input_sbol']
        params = json.load(request.files['data'])
        #pass the files to the rpReader
        output_tar = io.BytesIO()
        #### HDD ####
        runOptBioDes_hdd(input_tar,
                         input_sbol,
                         output_tar,
                         str(params['pathway_id']),
                         int(params['max_variants']),
                         int(params['lib_size']),
                         str(params['input_parts']))
        ###### IMPORTANT ######
        output_tar.seek(0)
        #######################
        return send_file(output_tar, as_attachment=True, attachment_filename='rpOptBioDes.tar', mimetype='application/x-tar')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
