import ROOT
import math
from optparse import OptionParser
import copy

# python dumpScaleFactorTables.py --mc ../efficiency-mc-passingTrigWP90-LO.root --data ../efficiency-data-passingTrigWP90.root -b -n passingTrigWP90 --alternativeFitSig ../efficiency-data-passingTrigWP90-BreitWigner.root --alternativeFitBkg ../efficiency-data-passingTrigWP90-ExpBkg.root  --pileupUp ../efficiency-mc-passingTrigWP90-pileup-Up.root --pileupDown ../efficiency-mc-passingTrigWP90-pileup-Down.root --NLO ../efficiency-mc-passingTrigWP90-NLO-cutAndcount.root --selectionAlternativeMC ../efficiency-mc-passingTrigWP90-WP90Tag.root --selectionAlternativeData ../efficiency-data-passingTrigWP90-WP90Tag.root --fitRangeMC ../efficiency-mc-passingTrigWP90-test-range-systematics.root --fitRangeData ../efficiency-data-passingTrigWP90-range-systematics.root 

def makeTable(hnum, hden, hAlternativeFitSig, hAlternativeFitBkg, hpileupUp, hpileupDown, hNLO, hMCSelectionAlternative, hDataSelectionAlternative, hMCFitRange, hDataFitRange, tablefilename, effDatafilename, effMCfilename, WP):
    nX = hnum.GetNbinsX()
    nY = hnum.GetNbinsY()
    c = ROOT.TCanvas("c", "c", 1400, 800)
    c.SetBottomMargin(0.15)
    #c.SetLogx()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
  
    f = open(tablefilename, "w+")
    fDataEff = open(effDatafilename, "w+")
    fMCEff = open(effMCfilename, "w+")
    f.write("\\begin{document} \n\\thispagestyle{empty} \n\\begin{landscape} \n\\begin{table}[ht] \n\caption*{Scale factors for triggering electron ID 25 ns data WP " + str(WP) +  "} \n\\resizebox{1.5\\textwidth}{!}{ \n\\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}\n")
    fDataEff.write("\\begin{tabular}{|c|c|c|c|c|}\n")
    fMCEff.write("\\begin{tabular}{|c|c|c|c|c|}\n")
    f.write("\\hline\n")
    fDataEff.write("\\hline\n")
    fMCEff.write("\\hline\n")
    f.write("$p_{T,min}$ & $p_{T,max}$ & $\\eta_{min}$ & $\\eta_{max}$ & Scale factor & signal shape unc. (\\%) & bkg. shape unc.(\\%) & pileup unc. (\\%)& NLOvsLO unc.(\\%) & tag selection unc.(\\%) & fit range unc.(\\%) & stat.unc.(\\%) & total unc. (\\%) & total unc. (abs.) \\\\ \n\\hline \n")
    fDataEff.write("$p_{T,min}$ & $p_{T,max}$  & $\\eta_{min}$ & $\\eta_{max}$ &  effData \\\\ \n\\hline \n")
    fMCEff.write("$p_{T,min}$ & $p_{T,max}$  & $\\eta_{min}$ & $\\eta_{max}$ &  effMC  \\\\ \n\\hline \n")
    hist = copy.copy(hnum)
    hist.Divide(hden)
    for i in xrange(1, nX+1):
        pT0 = hnum.GetXaxis().GetBinLowEdge(i)
        pT1 = hnum.GetXaxis().GetBinLowEdge(i+1)
    
        for j in xrange(1, nY+1):
            eta0 = hnum.GetYaxis().GetBinLowEdge(j)
            eta1 = hnum.GetYaxis().GetBinLowEdge(j+1)

            x = hnum.GetBinContent(i,j)/hden.GetBinContent(i,j)
            effData = hnum.GetBinContent(i,j)
            effMC = hden.GetBinContent(i,j)
            dx1 = hnum.GetBinError(i,j)/hnum.GetBinContent(i,j)
            dx2 = hden.GetBinError(i,j)/hden.GetBinContent(i,j)
            dx = math.sqrt(dx1*dx1+dx2*dx2)*x
            
            #systematics : signal shape
            SF_AlternativeFitSig = hAlternativeFitSig.GetBinContent(i,j)/hden.GetBinContent(i,j)
            FitSigAlternativeUnc = abs(SF_AlternativeFitSig - x)
            #systematics : bkg shape
            SF_AlternativeFitBkg = hAlternativeFitBkg.GetBinContent(i,j)/hden.GetBinContent(i,j)
            FitBkgAlternativeUnc = abs(SF_AlternativeFitBkg - x)
            #pileup uncertainty
            pileupUncertainty = max ( abs((effData/hpileupUp.GetBinContent(i,j) )  - x), abs((effData/hpileupDown.GetBinContent(i,j) )  - x))
            #NLOvsLO  uncertainty
            SF_NLO = hnum.GetBinContent(i,j)/hNLO.GetBinContent(i,j)
            NLO_Unc = abs(SF_NLO -x)
            #systematics: tag selection
            SF_SelectionAlternative = hDataSelectionAlternative.GetBinContent(i,j)/hMCSelectionAlternative.GetBinContent(i,j)
            SelectionUnc = abs(SF_SelectionAlternative -x)
            #fit range systematics
            SF_FitRange = hDataFitRange.GetBinContent(i,j)/hMCFitRange.GetBinContent(i,j)
            FitRangeUnc = abs(SF_FitRange - x)
            #total uncertainty
            totalUnc = math.sqrt(FitSigAlternativeUnc*FitSigAlternativeUnc + FitBkgAlternativeUnc*FitBkgAlternativeUnc  + pileupUncertainty*pileupUncertainty + NLO_Unc*NLO_Unc + SelectionUnc*SelectionUnc + FitRangeUnc*FitRangeUnc + dx*dx)
            hist.SetBinError(i,j,totalUnc)
            
            f.write("%4.1f &  %4.1f &  %+6.2f & %+6.2f  & %6.2f &  %6.2f  & %6.2f  &  %6.2f & %6.2f & %6.2f & %6.2f & %6.2f & %6.2f  & %6.2f  \\\\ \n"%(pT0, pT1, eta0, eta1 ,x, 100*abs(SF_AlternativeFitSig -x)/x, 100*abs(SF_AlternativeFitBkg -x)/x, 100*pileupUncertainty/x, 100*abs(SF_NLO - x)/x, 100*abs(SF_SelectionAlternative - x)/x, 100*abs(SF_FitRange -x)/x, 100.*dx/x, 100.*totalUnc/x, totalUnc))
            fDataEff.write("%4.1f &  %4.1f &  %+6.4f & %+6.4f  & %6.4f &   \\\\ \n"%(pT0, pT1, eta0, eta1, effData))
            fMCEff.write("%4.1f &  %4.1f &  %+6.4f & %+6.4f  & %6.4f &   \\\\ \n"%(pT0, pT1, eta0, eta1, effMC))
            f.write("\\hline\n")
            fMCEff.write("\\hline\n")
            fDataEff.write("\\hline\n")
    f.write("\\end{tabular} \n}\n\\end{table}\n\\end{landscape}\n\\end{document}\n")       
    fDataEff.write("\\end{tabular}\n")       
    fMCEff.write("\\end{tabular}\n")       
    f.close()
    fDataEff.close()
    fMCEff.close()

    ROOT.gStyle.SetPaintTextFormat("4.2f")
    histForDrawing = ROOT.TH2F("drawing", "drawing", nX, hist.GetXaxis().GetBinLowEdge(1), 65., nY, hist.GetYaxis().GetBinLowEdge(1), hist.GetYaxis().GetBinLowEdge(nY + 1) )
    for i in xrange(1, nX+1):
        for j in xrange(1, nY+1):
            histForDrawing.SetBinContent(i, j, hist.GetBinContent(i,j) )
            histForDrawing.SetBinError(i, j, hist.GetBinError(i,j) )

    for i in xrange(1, nX+1):
        histForDrawing.GetXaxis().SetBinLabel(i, "[" + str(hist.GetXaxis().GetBinLowEdge(i)) + "," + str(hist.GetXaxis().GetBinUpEdge(i)) + "]")
    histForDrawing.SetLabelSize(0.07)
    histForDrawing.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
    histForDrawing.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
    histForDrawing.GetXaxis().SetTitleOffset(2.)
    histForDrawing.Draw("COLZTEXTE")
    c.SaveAs( options.name + ".png")

def main(options):
    fData = ROOT.TFile(options.data)
    fMC   = ROOT.TFile(options.mc)
    #get files for systematics
    #signal shape
    fAlternativeFitSig = ROOT.TFile(options.alternativeFitSig)
    #background shape
    fAlternativeFitBkg = ROOT.TFile(options.alternativeFitBkg)
    #pileup Up
    fpileupUp = ROOT.TFile(options.pileupUp)
    #pileup Down
    fpileupDown = ROOT.TFile(options.pileupDown)
    #NLO uncertainty
    fNLO = ROOT.TFile(options.NLO)
    #data: tag selection systematics
    fDataSelectionAlternative = ROOT.TFile(options.selectionAlternativeData)
    #MC: tag selection systematics
    fMCSelectionAlternative = ROOT.TFile(options.selectionAlternativeMC)
    #MC: fit range systematics
    fFitRangeMC = ROOT.TFile(options.fitRangeMC)
    #data: fit range systematics
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

    #getting histograms from files: data
    temp = "%s/%s/fit_eff_plots/" % (options.directory, options.name)
    #if("ToHLT" in temp):
    #    temp = "%s/%s/cnt_eff_plots/" %(options.directory, options.name)
    #nominal data
    fData.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hData = p

    #data alternative signal shape
    fAlternativeFitSig.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hAlternativeFitSig = p

    # data alternative background shape
    fAlternativeFitBkg.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hAlternativeFitBkg = p
                    
    #data tag selection systematics
    fDataSelectionAlternative.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hDataSelectionAlternative = p

    #fit range systematics
    fFitRangeData.cd(temp)

    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hDataFitRange = p

    #getting histograms from files: MC
    #nominal MC
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

    #pileup down
    fpileupDown.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hpileupDown = p

    #tag selection systematics
    fMCSelectionAlternative.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hMCSelectionAlternative = p

    # fit range systematics
    fFitRangeMC.cd(temp)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
    for k in  keyList:
        obj = ROOT.gDirectory.GetKey(k).ReadObj();
        innername = obj.GetName()
        if (obj.ClassName() == "TCanvas"):
            for p in obj.GetListOfPrimitives():
                if (p.ClassName() == "TH2F"):
                    hMCFitRange = p

    #getting histograms from files with cut and count: this we do only for NLO vs LO uncertainty
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
    tempEffData =  "EffData_%s_%s.txt"%(options.directory, options.name)
    tempEffMC =  "EffMC_%s_%s.txt"%(options.directory, options.name)
    #hData.Divide(hMC)
    if options.name == "passingTrigWP80" :
        WP = 80
    elif options.name == "passingTrigWP90":
        WP = 90
    else :
        WP =-1

    makeTable(hData, hMC, hAlternativeFitSig, hAlternativeFitBkg, hpileupUp, hpileupDown, hNLO, hMCSelectionAlternative, hDataSelectionAlternative,hMCFitRange, hDataFitRange, temp, tempEffData, tempEffMC, WP)
    
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