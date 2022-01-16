import ROOT


def setUpHistrogram(self,Name,ttreeName='',LineColor,LineWidth=2,Title='',XTitle,YTitle,Nbins=0,min=0,max=0):
	if ttreeName!='':
		Name = ROOT.gDirectory.Get(ttreeName).Clone()
	else:
		Name = ROOT.TH1F("Name", "Name",Nbins,min,max)
	Name.SetLineColor(LineColor)
	Name.SetLineWidth(LineWidth)
	Name.SetTitle(Title)
	Name.GetXaxis().SetTitle(XTitle)
	Name.GetYaxis().SetTiTle(YTitle)
	return Name
