from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import glob
from particleClass import particle
import argparse
import traceback

ROOT.PyConfig.IgnoreCommandLineOptions = True  #Find out what does this do ?

class Channel(Module):
	def __init__(self, channel):
		self.channel = channel # Specify the channel
		#Need to add conditons for other channels
		if self.channel == "tt":
				self.boostedTau = particle("boostedTau")
				self.Tau = particle("Tau")
				self.FatJet = particle("FatJet")
		
		if self.channel == "test":
			self.boostedTau = particle("boostedTau")

    			
    			
				

	def beginJob(self):
        	pass
	
	def endJob(self):
		pass

	def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		self.out = wrappedOutputTree
		#self.Tau.setUpBranches(self.out) #creating the new branches
		#self.FatJet.setUpBranches(self.out)
		#self.boostedTau.setUpBranches(self.out)
		if self.channel == "tt":
			self.Tau.setUpBranches(self.out) #creating the new branches
			self.FatJet.setUpBranches(self.out)
			self.boostedTau.setUpBranches(self.out)
		
		if self.channel == "test":
			self.boostedTau.setUpBranches(self.out)
		


    		
    		
	def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
		pass
    	
	#event loop
	def analyze(self, event): 

		#Need to add more cchannels to this
		if self.channel == "test":
			self.boostedTau.setupCollection(event)
			self.boostedTau.apply_cut(lambda x: x.pt > 20 and (abs(x.eta) < 2.3) and (x.idMVAoldDM2017v2 & 1 == 1) )
			self.boostedTau.fillBranches(self.out)
			return True

		#Need to add other channels to this
		if self.channel == "tt":
			self.Tau.setupCollection(event)
			self.Tau.apply_cut(lambda x: x.pt > 20 and (abs(x.eta) < 2.4))

			self.FatJet.setupCollection(event)
			self.FatJet.apply_cut(lambda x: x.pt > 200 and (abs(x.eta) < 2.4))

			self.boostedTau.setupCollection(event)
			self.boostedTau.apply_cut(lambda x: x.pt > 20 and (abs(x.eta) < 2.3) and (x.idMVAoldDM2017v2 & 1 == 1) )


			if((len(self.Tau.collection)==2 or len(self.boostedTau.collection)==2) and len(self.FatJet.collection)==1): # condition for hadronic channel
				self.Tau.fillBranches(self.out) #Fill the branches
				self.FatJet.fillBranches(self.out)
				return True # Store event
			else:
				return False # Reject event

			
	

letsSortChannels = lambda: Channel(args.Channel)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Script to Handle root file preparation to split into channels. Input should be a singular files for each dataset or data already with some basic selections applied')
	parser.add_argument('--Channel',help="enter either tt or et or mut. For boostedTau test enter test",required=True)
	parser.add_argument('--inputLocation',help="enter the path to the location of input file set",default="")
	args = parser.parse_args()
	try:
		if args.Channel == "tt":
			#fnames = glob.glob(args.inputLocation + "/*.root")
			fnames = [str(args.inputLocation)] #for condor
 			#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/TestOutput"
			outputDir = "." #for condor
 			outputbranches = "keep_and_drop.txt"
 			cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2" # These wholesale cuts applied even before entering event loop
 			p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_ttChannel",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
			p.run()
		
		if args.Channel == "test":
			#fnames = glob.glob(args.inputLocation + "/*.root")
			fnames = [str(args.inputLocation)] #for condor
 			#outputDir = "/data/gparida/Background_Samples/bbtautauAnalysis/2016/TestOutput"
			outputDir = "." #for condor
 			outputbranches = "keep_and_drop.txt"
 			cuts = "MET_pt>200 && PV_ndof > 4 && abs(PV_z) < 24 && sqrt(PV_x*PV_x+PV_y*PV_y) < 2" # These wholesale cuts applied even before entering event loop
 			p = PostProcessor(outputDir, fnames, cut=cuts,branchsel=None,modules=[letsSortChannels()], postfix="_boostedTest",noOut=False,outputbranchsel=outputbranches) # running the post processor - output files will have the _ttChannels appended to their name 
			p.run()

		
	except Exception as error:
		print("Error:(")
		traceback.print_exc()