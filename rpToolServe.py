'''
#!/usr/bin/python2.7
'''

import sys
sys.path.insert(0, '/home/')

import tempfile
import shutil
import logging
import glob
import tarfile
import libsbml
import subprocess
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
    tmpOutputFolder = tempfile.mkdtemp()
    tmpInputFolder = tempfile.mkdtemp()
    #need to use 
    print('###### 1 ######')
    subprocess.call(['tar', 'xf', inputTar, '-C', tmpInputFolder])
    subprocess.call(['ls', tmpInputFolder])
    #tar = tarfile.open(inputTar, 'r:xz')
    #tar.extractall(path=tmpInputFolder)
    #tar.close()
    print('###### 2 ######')
    for sbml_path in glob.glob(tmpInputFolder+'/*'):
        print('------------ '+str(sbml_path)+' ------------')
        fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '')
        print('------------ '+str(fileName)+' ------------')
        selenzyme_info = rpTool.readRPpathway_selenzyme(libsbml.readSBMLFromFile(sbml_path), pathway_id)
        print(selenzyme_info)
        ##### PABLO ####
        # Prepare input files: geneparts.csv, refparts.csv
        genes = rpTool.selenzinfo2table(selenzyme_info, maxgenes)
        print(genes)
        gene_parts = os.path.join(tmpOutputFolder, 'GeneParts.csv')
        print(gene_parts)
        genes.to_csv(gene_parts, index=False)
        if file_parts is None:
            refs = rpTool.refparts_default()
            ref_parts = os.path.join(tmpOutputFolder, 'RefParts.csv')
            refs.to_csv(ref_parts,index=False)
        '''
        # Run DoE and retrieve SBOL and diagnostics
        try:
            diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, libsize)
        except:
           logging.error('Error detected error in rpTool.doeGetSBOL')
           continue
        '''
        print(ref_parts)
        print(gene_parts)
        print(libsize)
        diagnostics = rpTool.doeGetSBOL(ref_parts, gene_parts, libsize)
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
        #print(diagnostics)
        #print(diagnostics.keys())
        #dict_keys(['J', 'pow', 'rpv', 'X', 'M', 'factors', 'fact', 'M1', 'df', 'names', 'seed', 'libsize', 'sbol'])
        # Store results
        #open(outSBOL, 'w').write(res['data']['sbol'])
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
    print('###### 3 ######')
    with tarfile.open(outputTar, mode='w:gz') as ot:
        for sbol_path in glob.glob(tmpOutputFolder+'/*'):
            outFileName = fileName+'.sbol.xml'
            info = tarfile.TarInfo(outFileName)
            info.size = os.path.getsize(sbol_path)
            ot.addfile(tarinfo=info, fileobj=open(sbol_path, 'rb'))
    print('###### 4 ######')
    shutil.rmtree(tmpOutputFolder)
    shutil.rmtree(tmpInputFolder)
    print('###### 5 ######')
