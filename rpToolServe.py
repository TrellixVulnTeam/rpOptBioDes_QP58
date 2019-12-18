import sys
sys.path.insert(0, '/home/')

import tempfile
import logging
import glob
import tarfile
import libsbml
#import subprocess
import os

import rpTool

## run using HDD 3X less than the above function
#
#
def runOptBioDes_hdd(inputTar, outputTar, pathway_id='rp_pathway', maxgenes=5, libsize=32, file_parts=None):
    """ - libsize: desired size of the combinatorial library,
        - maxgenes: maximum number of genes selected per step
        - file_parts: file with a URI list of sbol parts in Synbiohub
    """
    if file_parts=='None' or file_parts=='none' or file_parts=='N':
        file_parts = None
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            with tempfile.TemporaryDirectory() as tmpPartsFolder:
                #tar = tarfile.open(fileobj=inputTar, mode='r')
                tar = tarfile.open(inputTar, mode='r')
                tar.extractall(path=tmpInputFolder)
                tar.close()
                for sbml_path in glob.glob(tmpInputFolder+'/*'):
                    fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '')
                    selenzyme_info = rpTool.readRPpathway_selenzyme(libsbml.readSBMLFromFile(sbml_path), pathway_id)
                    ##### PABLO ####
                    # Prepare input files: geneparts.csv, refparts.csv
                    genes = rpTool.selenzinfo2table(selenzyme_info, maxgenes)
                    gene_parts = os.path.join(tmpPartsFolder, 'GeneParts.csv')
                    genes.to_csv(gene_parts, index=False)
                    if file_parts is None:
                        refs = rpTool.refparts_default()
                        ref_parts = os.path.join(tmpPartsFolder, 'RefParts.csv')
                        refs.to_csv(ref_parts,index=False)
                    # Run DoE and retrieve SBOL and diagnostics
                    try:
                        diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, libsize)
                    except:
                        logging.error('Error detected error in rpTool.doeGetSBOL for '+str(sbml_path))
                        continue
                    #diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, libsize)
                    #diagnostics = doeGetSBOL(ref_parts, gene_parts, size)
                    '''
                    data = {'M': diagnostics['M'].tolist(),
                            'J': diagnostics['J'],
                            'pow': diagnostics['J'],
                            'rpv': diagnostics['J'],
                            'names': diagnostics['names'],
                            'libsize': diagnostics['libsize'],
                            'seed': diagnostics['seed'],
                            'sbol': diagnostics['sbol']}
                    '''
                    open(tmpOutputFolder+'/'+fileName, 'w').write(diagnostics['sbol'])
                    #TODO: need to include the efeciecy information inside the SBOL directly
                    '''
                    with open(tmpOutputFolder+'_info.txt', 'w') as text_file:
                        text_file.write('Size: '+str(diagnostics['libsize'])+'\n')
                        text_file.write('Efficiency:'+str(diagnostics['J'])+'\n')
                    '''
                    #Here you can insert what you need to do, or build a larger dictionnary for all the pathways. FileName 
                    #is the name of the pathway ex: rp_1_1
                    #NOTE: this is retro so the first reaction is RP{highest} and the last reaction in the pathway is RP{lowest}
                    # the dictionnary should be like the following:
                    ################
                with tarfile.open(outputTar, mode='w:xz') as ot:
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
