import ROOT
import os
import json
from weightList import *

from Configurations.ConfigDefinition import ReweightConfiguration
from Configurations.Weights.CrossSectionWeightingModule.CrossSectionWeight import crossSectionWeight as crossSectionWeight
from Configurations.Weights.pileupWeightingModule.pileupWeight import pileupWeight_2016

Radion_M1200Config = ReweightConfiguration()
Radion_M1200Config.name = 'Radion_M1200'
#Radion_M1200Config.jsonSampleFile = os.environ['CMSSW_BASE']+'/src/bbtautauAnalysisScripts/analysisCore/config/samples/2016_Samples.json'
Radion_M1200Config.jsonSampleFile =  os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/Samples/2016_Samples.json'

with open(Radion_M1200Config.jsonSampleFile,'r') as jsonFile:
    jsonInfo = json.load(jsonFile)
theFile = ROOT.TFile(jsonInfo[Radion_M1200Config.name]['file'])
totalNumberOfEvents = theFile.cutflow.GetBinContent(1)
theFile.Close()

Radion_M1200Config.inputFile = jsonInfo[Radion_M1200Config.name]['file']
Radion_M1200Config.inputFile_tt = jsonInfo[Radion_M1200Config.name]['file_tt']
Radion_M1200Config.inputFile_et = jsonInfo[Radion_M1200Config.name]['file_et']
Radion_M1200Config.inputFile_mt = jsonInfo[Radion_M1200Config.name]['file_mt']

crossSectionWeight.XS = jsonInfo[Radion_M1200Config.name]['XS'] * 1e-12 #XS in pb
crossSectionWeight.timePeriod = '2016'
crossSectionWeight.totalNumberOfEvents = totalNumberOfEvents
try:
    crossSectionWeight.forcedGenWeight = jsonInfo[Radion_M1200Config.name]['forcedGenWeight']
except KeyError:
    crossSectionWeight.forcedGenWeight = None


Radion_M1200Config.listOfWeights = list