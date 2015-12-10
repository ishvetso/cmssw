import ROOT
import math
from optparse import OptionParser
import copy

# python dumpScaleFactorTables.py --mc ../efficiency-mc-passingTrigWP80-LO.root --data ../efficiency-data-passingTrigWP80.root -b -n passingTrigWP80 --alternativeFitSig ../efficiency-data-passingTrigWP80-BreitWigner.root --alternativeFitBkg ../efficiency-data-passingTrigWP80-ExpBkg.root  --pileupUp ../efficiency-mc-passingTrigWP80-pileup-Up.root --pileupDown ../efficiency-mc-passingTrigWP80-pileup-Down.root --NLO ../efficiency-mc-passingTrigWP80-NLO-cutAndcount.root --selectionAlternativeMC ../efficiency-mc-passingTrigWP80-WP90Tag.root --selectionAlternativeData ../efficiency-data-passingTrigWP80-WP90Tag.root

def makeTable(hnum, hden, hAlternativeFitSig, hAlternativeFitBkg, hpileupUp, hpileupDown, hNLO, hMCSelectionAlternative, hDataSelectionAlternative, hMCFitRange, hDataFitRange, tablefilename):
    nX = hnum.GetNbinsX()
    nY = hnum.GetNbinsY()
    c = ROOT.TCanvas()
    c.SetLogx()
  
    f = open(tablefilename, "w+")
    
    
    f.write("minEta  maxEta minPt maxPt effData statError effMC statError systBkgShape systSigShape systFitRange systNLOvsLO systPU systTagSelection \n")
   
    hist = copy.copy(hnum)
    hist.Divide(hden)
    for i in xrange(1, nX+1):
        pT0 = hnum.GetXaxis().GetBinLowEdge(i)
        pT1 = hnum.GetXaxis().GetBinLowEdge(i+1)
    
        for j in xrange(1, nY+1):
            x = hnum.GetBinContent(i,j)/hden.GetBinContent(i,j)
            effData = hnum.GetBinContent(i,j)
            effMC = hden.GetBinContent(i,j)
            effDatastatError = hnum.GetBinError(i,j)
            effMcstatError = hden.GetBinError(i,j)
            dx1 = hnum.GetBinError(i,j)/hnum.GetBinContent(i,j)
            dx2 = hden.GetBinError(i,j)/hden.GetBinContent(i,j)
            dx = math.sqrt(dx1*dx1+dx2*dx2)*x
            eta0 = hnum.GetYaxis().GetBinLowEdge(j)
            eta1 = hnum.GetYaxis().GetBinLowEdge(j+1)
            #systematics
            SF_AlternativeFitSig = hAlternativeFitSig.GetBinContent(i,j)/hden.GetBinContent(i,j)
            SF_AlternativeFitBkg = hAlternativeFitBkg.GetBinContent(i,j)/hden.GetBinContent(i,j)
            FitSigAlternativeUnc = abs(SF_AlternativeFitSig - x)
            FitBkgAlternativeUnc = abs(SF_AlternativeFitBkg - x)
            pileupUncertainty = max ( abs((effData/hpileupUp.GetBinContent(i,j) )  - x), abs((effData/hpileupDown.GetBinContent(i,j) )  - x))
            SF_NLO = hnum.GetBinContent(i,j)/hNLO.GetBinContent(i,j)
            NLO_Unc = abs(SF_NLO -x)
            SF_SelectionAlternative = hDataSelectionAlternative.GetBinContent(i,j)/hMCSelectionAlternative.GetBinContent(i,j)
            SelectionUnc = abs(SF_SelectionAlternative -x)

            SF_FitRange = hDataFitRange.GetBinContent(i,j)/hMCFitRange.GetBinContent(i,j)
            totalUnc = math.sqrt(FitSigAlternativeUnc*FitSigAlternativeUnc + FitBkgAlternativeUnc*FitBkgAlternativeUnc  + pileupUncertainty*pileupUncertainty + NLO_Unc*NLO_Unc + SelectionUnc*SelectionUnc + dx*dx)
            hist.SetBinError(i,j,totalUnc)
            
            f.write("%+6.2f  %+6.2f %4.1f   %4.1f  %6.2f  %6.4f  %6.4f %6.4f %6.4f %6.4f %6.4f %6.4f %6.4f %6.4f \n"%(eta0, eta1, pT0, pT1, effData, effDatastatError, effMC, effMcstatError,   abs(SF_AlternativeFitBkg -x), abs(SF_AlternativeFitSig -x), abs(SF_FitRange - x), abs(SF_NLO - x), pileupUncertainty, abs(SF_SelectionAlternative - x)))            
    f.close()
    

    ROOT.gStyle.SetPaintTextFormat("4.2f")
    #histForDrawing = TH2F("drawing", "drawing", nX, hist.GetXaxis().GetBinLowEdge(nX), 65., hist.GetYaxis().GetBinLowEdge(1), hist.GetYaxis().GetBinLowEdge(nY + 1) )
    #print hist.GetYaxis().GetBinLowEdge(nY + 1)
    hist.Draw()
    c.SaveAs( options.name + ".png")

def main(options):
    fData = ROOT.TFile(options.data)
    fMC   = ROOT.TFile(options.mc)
    fAlternativeFitSig = ROOT.TFile(options.alternativeFitSig)
    fAlternativeFitBkg = ROOT.TFile(options.alternativeFitBkg)
    fpileupUp = ROOT.TFile(options.pileupUp)
    fpileupDown = ROOT.TFile(options.pileupDown)
    fNLO = ROOT.TFile(options.NLO)
    fDataSelectionAlternative = ROOT.TFile(options.selectionAlternativeData)
    fMCSelectionAlternative = ROOT.TFile(options.selectionAlternativeMC)
    fFitRangeMC = ROOT.TFile(options.fitRangeMC)
    fFitRangeData = ROOT.TFile(options.fitRangeData)

    hData = ""
    hMC = ""
    hAlternativeFitSig = ""
    hAlternativeFitBkg = ""
    hpileupUp = ""
    hpileupDown = ""
    hNLO = ""
    hDataSelectionAlternative = ""
    hMCSelectionAlternative = ""
    hDataFitRange = ""
    hMCFitRange = ""

    temp = "%s/%s/fit_eff_plots/" % (options.directory, options.name)
    #if("ToHLT" in temp):
    #    temp = "%s/%s/cnt_eff_plots/" %(options.directory, options.name)
    fData.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hData = p

    fAlternativeFitSig.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hAlternativeFitSig = p

    fAlternativeFitBkg.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hAlternativeFitBkg = p
                    
    fDataSelectionAlternative.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hDataSelectionAlternative = p

    fFitRangeData.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hDataFitRange = p

    temp = "%s/MCtruth_%s/fit_eff_plots/" % (options.directory, options.name)
    fMC.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hMC = p
    #pileup up
    fpileupUp.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hpileupUp = p

    fpileupDown.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hpileupDown = p

    fMCSelectionAlternative.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hMCSelectionAlternative = p

    fFitRangeMC.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hMCFitRange = p

    temp = "%s/MCtruth_%s/cnt_eff_plots/" % (options.directory, options.name)   
    fNLO.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hNLO = p                 
                    
    temp = "ScaleFactor_%s_%s.txt"%(options.directory, options.name)
    #hData.Divide(hMC)
    makeTable(hData, hMC, hAlternativeFitSig, hAlternativeFitBkg, hpileupUp, hpileupDown, hNLO, hMCSelectionAlternative, hDataSelectionAlternative, hMCFitRange, hDataFitRange, temp)
    
    fData.Close()
    fMC.Close()
    fAlternativeFitSig.Close()
    fAlternativeFitBkg.Close()
    fpileupUp.Close()
    fpileupDown.Close()
    fNLO.Close()

if (__name__ == "__main__"):
    parser = OptionParser()
    parser.add_option("", "--mc", default="efficiency-mc-GsfElectronToId.root", help="Input filename for MC")
    parser.add_option("", "--data", default="efficiency-data-GsfElectronToId.root", help="Input filename for data")
    parser.add_option("-d", "--directory", default="GsfElectronToRECO", help="Directory with workspace")
    parser.add_option("-n", "--name", default="Medium", help="Subdirectory with results")
    parser.add_option("-b", dest="batch", action="store_true", help="ROOT batch mode", default=False)
    parser.add_option("", "--alternativeFitSig", default="efficiency-data-passingTrigWP80-BreitWigner.root", help="file with alternative fit signal")
    parser.add_option("", "--alternativeFitBkg", default="efficiency-data-passingTrigWP80-BreitWigner.root", help="file with alternative fit bkg")
    parser.add_option("", "--pileupUp", default="efficiency-mc-passingTrigWP80-pileup-Up.root", help="pileup Up MC")
    parser.add_option("", "--pileupDown", default="efficiency-mc-passingTrigWP80-pileup-Down.root", help="pileup Down MC")
    parser.add_option("", "--NLO", default="efficiency-mc-passingTrigWP80-NLO.root", help="NLO")
    parser.add_option("", "--selectionAlternativeMC", default="efficiency-mc-passingTrigWP80-WP90Tag.root", help="selection alternative MC")
    parser.add_option("", "--selectionAlternativeData", default="efficiency-data-passingTrigWP80-WP90Tag.root", help="selection alternative data")
    parser.add_option("", "--fitRangeMC", default="efficiency-data-passingTrigWP80-WP90Tag.root", help="fit range MC")
    parser.add_option("", "--fitRangeData", default="efficiency-data-passingTrigWP80-WP90Tag.root", help="fit range data")
    
    (options, arg) = parser.parse_args()

    if (options.batch):
        ROOT.gROOT.SetBatch(True)

    main(options)