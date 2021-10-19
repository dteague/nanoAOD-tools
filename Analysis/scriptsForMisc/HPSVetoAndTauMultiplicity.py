from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
from particleClass import particle
import argparse
import traceback
import multiprocessing as  np
import os

#The objective of the code is to get the multiplicity of taus - applying a base selection of VLoose for all taus
#The double counting of the taus needs to be avoided by applying the veto < 0.02\
#Then make two addtional histogram with the leading tau with a tigher wp

ROOT.PyConfig.IgnoreCommandLineOptions = True

class HPSVetoandMultiplicty(Module):
    def __init__(self, filename):
        self.writeHistFile=True
        self.filename = filename #filename passed cause we needed to count the events with zero divide errors
	    #All these objects are common to all channels
        self.boostedTauVLoose = particle("boostedTau")
        self.HPSTauVloose = particle ("Tau")		
		
    def beginJob(self, histFile=None,histDirName=None):
        Module.beginJob(self,histFile,histDirName)
		#Now lets define the cutflow histograms
		#Starting to Di Tau channel selections
        self.totalMultiplicity =  ROOT.TH1F('totalMultiplicity', 'totalMultiplicity', 5, 0, 5)
        self.leadingLooseMultiplcity =  ROOT.TH1F('leadinLooseMultiplcity', 'leadinLooseMultiplcity', 5, 0, 5)
        self.leadingMediumMultiplicity = ROOT.TH1F('leadingMediumMultiplicity', 'leadingMediumMultiplicity', 5, 0, 5)
        self.leadingTightMultiplicity = ROOT.TH1F('leadingTightMultiplicity', 'leadingTightMultiplicity', 5, 0, 5)
        
        self.addObject(self.totalMultiplicity)
        self.addObject(self.leadingLooseMultiplcity)
        self.addObject(self.leadingMediumMultiplicity)
        self.addObject(self.leadingTightMultiplicity)

    def HPStauVeto(self,tauCollectionObject):
        isTau =""
        tau1 = ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        tau2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        tau1.SetPtEtaPhiM(tauCollectionObject.pt,tauCollectionObject.eta,tauCollectionObject.phi,tauCollectionObject.mass)
        for loosetau in self.boostedTauVLoose.collection:
            tau2.SetPtEtaPhiM(loosetau.pt,loosetau.eta,loosetau.phi,loosetau.mass)
            deltaR = tau1.DeltaR(tau2)
            if deltaR < 0.02:
                isTau = "bad"
                break
        if isTau != "bad":
            return True
        else:
            return False
        



    def analyze(self, event):
        #self.boostedTauLoose.setupCollection(event)
        #self.boostedTauLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 4 == 4))

        self.boostedTauVLoose.setupCollection(event)
        self.boostedTauVLoose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2))
        

        self.HPSTauVloose.setupCollection(event)
        self.HPSTauVloose.apply_cut(lambda x: (x.pt > 20) and (abs(x.eta) < 2.3) and (x.idMVAnewDM2017v2 & 2 == 2))

        HPSVetoCollection = filter(self.HPStauVeto,self.HPSTauVloose.collection)

        self.totalMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))

        if (len(self.boostedTauVLoose.collection)!=0 and len(HPSVetoCollection)!=0):
            if ((self.boostedTauVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 4 == 4)):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))

            if ((self.boostedTauVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 4 == 4)):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))

            if ((self.boostedTauVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 8 == 8)):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))

            if ((self.boostedTauVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 8 == 8)):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
            
            if ((self.boostedTauVLoose.collection[0].pt > HPSVetoCollection[0].pt) and (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 16 == 16)):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))

            if ((self.boostedTauVLoose.collection[0].pt < HPSVetoCollection[0].pt) and (HPSVetoCollection[0].idMVAnewDM2017v2 & 16 == 16)):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))


        if (len(self.boostedTauVLoose.collection)!=0 and len(HPSVetoCollection)==0):
            if (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 4 == 4):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
            if (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 8 == 8):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
            if (self.boostedTauVLoose.collection[0].idMVAnewDM2017v2 & 16 == 16):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
        
        if (len(self.boostedTauVLoose.collection)==0 and len(HPSVetoCollection)!=0):
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 4 == 4):
                self.leadingLooseMultiplcity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
            
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 8 == 8):
                self.leadingMediumMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
            
            if (HPSVetoCollection[0].idMVAnewDM2017v2 & 16 == 16):
                self.leadingTightMultiplicity.Fill(len(self.boostedTauVLoose.collection)+len(HPSVetoCollection))
	
        return True        


def call_postpoc(files):
		letsSortChannels = lambda: HPSVetoandMultiplicty(filename)
		nameStrip=files.strip()
		filename = (nameStrip.split('/')[-1]).split('.')[-2]
		p = PostProcessor(outputDir,[files], cut=cuts,branchsel=None,modules=[letsSortChannels()],noOut=True,outputbranchsel=outputbranches,histFileName="HPSVeto_"+filename+".root",histDirName="Plots")
		p.run()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	#parser.add_argument('--Channel',help="enter either tt or et or mut. For boostedTau test enter test",required=True)
	parser.add_argument('--inputFile',help="enter the path to the location of input file set",default="")
	parser.add_argument('--ncores',help ="number of cores for parallel processing", default=1)
	args = parser.parse_args()

	#Define Event Selection - all those to be connected by and
	eventSelectionAND = ["MET_pt>200",
						"PV_ndof > 4",
						"abs(PV_z) < 24",
						"sqrt(PV_x*PV_x+PV_y*PV_y) < 2",
						"Flag_goodVertices",
						"Flag_globalSuperTightHalo2016Filter", 
						"Flag_HBHENoiseIsoFilter",
						"Flag_HBHENoiseFilter",
						"Flag_EcalDeadCellTriggerPrimitiveFilter",
						"Flag_BadPFMuonFilter",
						"Flag_eeBadScFilter"]

	fnames =[args.inputFile]
	outputDir = "."
	outputbranches = "keep_and_drop.txt"
	cuts = "&&".join(eventSelectionAND)
	argList = list()
	filename =""
	for file in fnames:
		argList.append(file)

	if int(args.ncores) == 1:
		for arr in argList:
			call_postpoc(arr)
	
	else:
		pool = np.Pool(int(args.ncores))
		res=pool.map(call_postpoc, argList)

                













    

