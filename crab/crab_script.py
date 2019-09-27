#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

##soon to be deprecated
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
##new way of using jme uncertainty
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

jmeCorrections = createJMECorrector(True, "2016", "B", "Total", True, "AK4PFchs", False)
cuts="nMuon+nElectron>=2&&MET_pt>40"


p=PostProcessor(".",inputFiles=inputFiles(),cut=cuts,modules=[jmeCorrections()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"

