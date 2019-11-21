#!/usr/bin/python3

import sys
sys.path.insert(0, '/home/')

import argparse
import libsbml
import tarfile
import logging
import tempfile
import os
import re
import requests
import csv
import pandas as pd
import glob
from doebase.synbioParts import doeGetSBOL

#TODO: consider replacing this function with directly rpSBML functions from an import 

#TODO: consider replacing this function with directly rpSBML functions from an import 

## Function that reads returns the list of rea
#
#
def readRPpathway_selenzyme(sbml, pathway_id='rp_pathway'):
    # loop through all the members of RP heterologous reactions
    groups = sbml.model.getPlugin('groups')
    rp_pathway = groups.getGroup(pathway_id)
    toRet = {}
    for member in rp_pathway.getListOfMembers():
        if not member.getIdRef()=='targetSink':
            toRet[member.getIdRef()] = {}
            #extract the annotatio from the reaction and extract selenzyme information
            annot = sbml.model.getReaction(member.getIdRef()).getAnnotation()
            #bag = annot.getChild('RDF').getChild('Ibisba').getChild('ibisba')
            bag = annot.getChild('RDF').getChild('BRSynth').getChild('brsynth')
            for i in range(bag.getNumChildren()):
                ann = bag.getChild(i)
                if ann=='':
                    logging.warning('This contains no attributes: '+str(ann.toXMLString()))
                    continue
                elif ann.getName()=='selenzyme':
                    for y in range(ann.getNumChildren()):
                        selAnn = ann.getChild(y)
                        try:
                            toRet[member.getIdRef()][selAnn.getName()] = float(selAnn.getAttrValue('value'))
                        except ValueError:
                            toRet[member.getIdRef()][selAnn.getName()] = None
                else:
                    #logging.warning('The reaction '+str(member.getIdRef())+' does not contain selenzyme information but is alos non-empty')
                    pass
    return toRet


def selenzinfo2table(si, maxgenes=5):
    """ Convert the selenzyme_info dictionary into the input table: Name, Type, Part, Step
        It assumes that pathway steps are in reverse direction and are called as RP1, RP2, etc.
    """
    genes = pd.DataFrame(columns=['Name','Type', 'Part', 'Step'])
    s = 1
    i = 1
    for step in sorted(si.keys(), key=lambda x:-int(re.sub('RP','',x))):
        j = 1
        for g in sorted(si[step], key=lambda x: -float(si[step][x])):
            genes.loc[i] = [g,'gene',g,s]
            if j > maxgenes:
                break
            i += 1
            j += 1
        s += 1
    return genes


def refparts_default():
    """ Default set of gene regulatory parts in E. coli
    """
    refs = pd.DataFrame([
        ['PlacUV5','promoter','https://synbiohub.org/public/igem/BBa_K1847014/1'],
        ['Ptrc','promoter','https://synbiohub.org/public/igem/BBa_J56012/1'],
        ['BBR1','origin','https://synbiohub.org/public/igem/BBa_I50041/1'],
        ['p15A','origin','https://synbiohub.org/public/igem/BBa_I50032/1'],
        ['ColE1','origin','https://synbiohub.org/public/igem/BBa_J64101/1'],
        ['res1','resistance','https://synbiohub.org/public/igem/BBa_I13800/1']
    ], columns=['Name','Type','Part'])
    return refs


## run using HDD 3X less than the above function
#
#
def runOptBioDes_hdd(inputTar, outputTar, pathway_id='rp_pathway', maxgenes=5, libsize=32, file_parts=None):
    """ - libsize: desired size of the combinatorial library,
        - maxgenes: maximum number of genes selected per step
        - file_parts: file with a URI list of sbol parts in Synbiohub
    """
    #rpcofactors = rpCofactors.rpCofactors()
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            tar = tarfile.open(inputTar, 'r:xz')
            tar.extractall(path=tmpInputFolder)
            tar.close()
            for sbml_path in glob.glob(tmpInputFolder+'/*'):
                fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '')
                selenzyme_info = readRPpathway_selenzyme(libsbml.readSBMLFromFile(sbml_path), pathway_id)
                ##### PABLO ####
                # Prepare input files: geneparts.csv, refparts.csv
                genes = selenzinfo2table(selenzyme_info,maxgenes)
                gene_parts = os.path.join(tmpOutputFolder, 'GeneParts.csv')
                genes.to_csv(gene_parts, index=False)
                if file_parts is None:
                    refs = refparts_default()
                    ref_parts = os.path.join(tmpOutputFolder, 'RefParts.csv')
                    refs.to_csv(ref_parts,index=False)
                # Run DoE and retrieve SBOL and diagnostics
                diagnostics = doeGetSBOL(ref_parts, gene_parts, libsize)
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
            with tarfile.open(outputTar, mode='w:xz') as ot:
                for sbol_path in glob.glob(tmpOutputFolder+'/*'):
                    outFileName = str(sbml_path.split('/')[-1])+'.sbol.xml'
                    info = tarfile.TarInfo(outFileName)
                    info.size = os.path.getsize(sbol_path)
                    ot.addfile(tarinfo=info, fileobj=open(sbol_path, 'rb'))
