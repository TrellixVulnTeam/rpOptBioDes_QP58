import sys
sys.path.insert(0, '/home/')

import re
import csv
import pandas as pd
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
