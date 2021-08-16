#! /usr/bin/env python

# VERSION Track: this file is based on "ExtractPlots_v5", then were modified by H.Bakhshian,
# Root liear fit were added at the end. 
# Notice that "ExtractPlots_v5p2" is new than "ExtractPlots_v5" but no root liear fit. 
# If you look for the newes one You should look at ExtractPlots_v5p2

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from ROOT import TCanvas, TGraph
import time
import os 
import sys
import argparse 
import math
import copy
import array

# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.colors import BoundaryNorm
# from matplotlib.ticker import MaxNLocator
import numpy as np
import scipy.io as sio

def GetData1D(hst , rebinX): # rebinX : intiger
    hst.Rebin(rebinX) # def rebinX=1 for get the orginal hist, rebinX>1 combines the bins
    nBins = hst.GetNbinsX()
    xAxis = hst.GetXaxis()
    yVect = np.zeros(nBins)
    xVect = np.zeros(nBins)
    for b in range( nBins ) :
        val = hst.GetBinContent(b+1)
        p = xAxis.GetBinCenter(b+1)
        yVect[b] = val
        xVect[b] = p
    #Data = np.vstack((xVect_np2, yVect_np2))    
    Data={"xAxis":xVect.astype('double'),"data":yVect.astype('double')}
    return Data
    
def GetData2D(hst , rebinX, rebinY): # rebinX,Y : intiger
    hst.Rebin2D(rebinX,rebinY) # def rebinX=1 for get the orginal hist, rebinX>1 combines the bins
    nBinsX = hst.GetNbinsX()
    nBinsY = hst.GetNbinsY()
    xAxis = hst.GetXaxis()
    yAxis = hst.GetYaxis()
    xVect = np.zeros(nBinsX)
    yVect = np.zeros(nBinsY)
    zVect = np.zeros((nBinsX,nBinsY))
    
    for xi in range( nBinsX ) :
        for yi in range(nBinsY) :
            b = hst.GetBin (xi,yi) 
            val = hst.GetBinContent(b+1)
            px = xAxis.GetBinCenter(xi+1)
            py = yAxis.GetBinCenter(yi+1)
            xVect[xi] = px
            yVect[yi] = py
            zVect[xi][yi] = val
    Data={"xAxis":xVect.astype('double'),"yAxis":yVect.astype('double'),"data":zVect.astype('double')}
    return Data

class SensorGroupInformation:
    def CopyH1IToH1F(self , h ):
        hret = ROOT.TH1F()
        h.Copy( hret )
        return hret

    def __init__(self , sensorGroup , pu , fIn , destDirectory):
        self.SensorGroup = sensorGroup
        self.PU = pu
        self.destDir = destDirectory
                
        self.InDir = fIn.GetDirectory( 'SensorGroup{0}'.format( self.SensorGroup ) )
        self.nSimHits = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nSimHits' , self.SensorGroup ) ) )
        self.nDigiHits = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nDigiHits' , self.SensorGroup ) ) )
        self.nDigiHitsV2 = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nDigiHitsV2' , self.SensorGroup ) ) )
        self.nOnes = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nOnes' , self.SensorGroup ) ) )
        self.nUnknowns = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nUnknowns' , self.SensorGroup ) ) )
        self.nTotals = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'TotalNumbers' , self.SensorGroup ) ) ) 
        self.TotRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'TotRho' , self.SensorGroup ) )
        self.ToaRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'ToaRho' , self.SensorGroup ) )
        self.TofRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'TofRho' , self.SensorGroup ) )
        self.BxTofRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'BxTofRho' , self.SensorGroup ) ) 
        
        self.nSimHits.Divide( self.nTotals )
        self.nSimHits.Scale( 1.0/7.0 )
        
        self.nTotals.Scale( 3.0 )
        
        self.nUnknownsRatio = self.nUnknowns.Clone("nUnknownsRatio_SG{0}".format(self.SensorGroup))
        self.nUnknownsRatio.Divide( self.nTotals )
        
        self.nDigiHits.Divide( self.nTotals )
        self.nTotalsMinusUnknowns = self.nTotals.Clone("nTotalsMinusUnknowns_SG{0}".format(self.SensorGroup))
        self.nZeros = self.nTotals.Clone("nZeros_SG{0}".format(self.SensorGroup))
        self.nZeros.Add( self.nOnes , -1.0 )
        self.nZeros.Add( self.nUnknowns , -1.0 )
        self.nTotalsMinusUnknowns.Add( self.nUnknowns , -1.0 )
        self.nZeros.Divide( self.nTotalsMinusUnknowns )
        self.nDigiHitsV2.Divide(self.nTotalsMinusUnknowns)
        for b in range( self.nZeros.GetNbinsX() ) :
            bc = self.nZeros.GetBinContent(b+1)
            if bc > 0:
                self.nZeros.SetBinContent( b + 1 , -math.log( bc ) )



    def Write(self ):
        self.c1 = ROOT.TCanvas('cPU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )

        self.nZeros.SetLineColor( 3 )
        self.nZeros.SetTitle( '<Digi>-ZeroCounting' )
        self.nZeros.SetStats( False )
        self.nZeros.Draw(  )

        self.nDigiHits.SetLineColor( 2 )
        self.nDigiHits.SetTitle( '<Digi>-counting' )
        self.nDigiHits.SetStats(False)
        self.nDigiHits.Draw('same')

        self.nSimHits.SetLineColor( 4 )
        self.nSimHits.SetTitle('<sim-hits>')
        self.nSimHits.SetStats(False)
        self.nSimHits.Draw("SAME")

        self.c1.BuildLegend()
        self.c1.SaveAs( self.destDir + '{0}.png'.format( self.c1.GetName() ) )
        
    def hZeroCounting(self ):
        return self.nZeros
        
    def hCounting(self ):
        return self.nDigiHits
    
    def hCountingV2(self ):
        return self.nDigiHitsV2
        
    def hSimHits(self ):
        return self.nSimHits
    
    def hUnknownRatio(self ):
        return self.nUnknownsRatio
        
    def hOnes(self ):
        return self.nOnes

    def hUnknowns(self ):
        return self.nUnknowns

    def hNtotal(self ):
        return self.nTotals

    def hNTotalsMinusUnknowns(self ):
        return self.nTotalsMinusUnknowns        

    def hToaRho(self ):
        return self.ToaRho

    def hTotRho(self ):
        return self.TotRho

    def hTofRho(self ):
        return self.TofRho        
        
    def hBxTofRho(self ):
        return self.BxTofRho

        
        
    def WriteToA(self, Rho):
        self.c2 = ROOT.TCanvas('cPU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.ToaRho.ProjectionY("py",b)
        y_proj.SetName(self.ToaRho.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        ToA_1FH = ROOT.TH1F()
        y_proj.Copy(ToA_1FH)
        ToA_1FH.SetTitle( 'BIB_ToA' )
        ToA_1FH.SetStats( False )
        #ToA_1FH.GetXaxis().SetRangeUser(-15.,15.)
        ToA_1FH.Rebin(2)
        ToA_1FH.Draw()
        self.c2.BuildLegend()
        self.c2.SaveAs( self.destDir + '{0}.png'.format( self.c2.GetName() ) )
        
        
def puValue(x):
    return {
        '0' : 0.,
        '0p5': 0.5,
        '1': 1.,
        '1p5': 1.5,
        '10': 10.,
        '50': 50.,
        '100': 100.,
        '140': 140.,
        '200': 200.,
    }.get(x, -1.)  
          
            
def puCase(x):
    return {
        '0' : '/histBibSelfMixOut_pu',
        '0p5': '/outPU',
        '1': '/outPU',
        '1p5': '/outPU',
        '10': '/outPU',
        '50': '/outPU',
        '100': '/outPU',
        '140': '/outPU',
        '200': '/outPU',
    }.get(x, '/outPU')    
    
 
def getSrcDir(x):
    return {
        'no_aging' : './resultsAging/no_aging',
        'aging_1000': './resultsAging/aging_1000',
        'aging_3000': './resultsAging/aging_3000',
        'aging_4000': './resultsAging/aging_4000',
        'bib_selfMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_SelfMixed/nTuplizerOutput/histResults',
        'bib_noMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_NoMix/nTuplizerOutput/histResults' ,
        'bib_puMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_PileupBibMixed/nTuplizerOutput/histResults',
    }.get(x, '/outPU')  
    
def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument( '-i' , '--infile' , dest='infile' , help='the name of the input file' , type=str  )
    parser.add_argument( '-s' , '--src' , dest='srcDir' ,default='.', help='the name of the source base directory' , type=str  )
    parser.add_argument( '-p' , '--pu' , dest='PU' , default=None , help='the pu of the file' , type=str , choices=['0', '0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200', 'all'])
    parser.add_argument( '-t' , '--srcType' , dest='srcType' , default=None , help='the source type' , type=str , choices=['no_aging', 'aging_1000', 'aging_3000' , 'aging_4000' , 'bib_selfMix' , 'bib_noMix' , 'bib_puMix'])
    
    opt = parser.parse_args()
    
    if opt.srcType:
        opt.srcDir=getSrcDir(opt.srcType)
        print(opt.srcDir)
    else:
        opt.srcType = 'no_aging' 
        
    
    
    destDir=opt.srcDir +'/'
    # if not opt.infile:
        # print('please specify the input file name using -i option')
        # return 1
    
    if not opt.PU:
        print('please specify the pu using -p option')
        return 1
    
    if opt.PU=='all':
        opt.PU = ['0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200']
    else :
        opt.PU =[opt.PU]
    
    
    ROOT.gStyle.SetOptTitle(0)
    puDict = {}
    #puDict = dict.fromkeys(opt.PU, list())
    for pu in opt.PU:
        opt_infile = opt.srcDir + puCase(pu) + pu +".root"
        fIn = ROOT.TFile.Open( opt_infile ) 
        print(opt_infile)
        sg_list=list()
        for sg in range( 8 ):
            s = SensorGroupInformation(sg , pu , fIn , destDir)
            sg_list.append(copy.deepcopy(s))
            puDict[pu] = sg_list

    print("------------")

    pu_len = len(opt.PU)
    puVect=np.zeros(pu_len)
    
    #SenDict1Keys = ['puVect','rVect', 'nZeros', 'nDigiHits', 'nDigiHitsV2', 'nSimHits', 'nUnknownsRatio', 'nOnes' , 'nUnknowns', 'nTotals']
    AllResultsDict={}
    AllSensors=[]
    for sg in range( 8):
        #SensorDict = dict.fromkeys(SenDict1Keys, list())
        SensorDict={}
        nZerosList = []
        nDigiHitsList = []
        nDigiHitsV2List = []
        nSimHitsList = []
        nUnknownsRatioList = []
        nOnesList = []
        nUnknownsList = []
        nTotalsList = []
        nTotalsMinusUnknownsList = []
    
        ToaRhoList = []
        TotRhoList = []
        TofRhoList = []
        BxTofRhoList = [] 
        
        for pu in opt.PU:
            puVal=puValue(pu)
            puVect[opt.PU.index(pu)] = puVal
            
            nZeros_data = GetData1D( puDict[pu][sg].hZeroCounting() , 1 )
            nZerosList.append(nZeros_data["data"])
            
            nDigiHits_data = GetData1D( puDict[pu][sg].hCounting() , 1 )
            nDigiHitsList.append(nDigiHits_data["data"])
            
            nDigiHitsV2_data = GetData1D( puDict[pu][sg].hCountingV2() , 1 )
            nDigiHitsV2List.append(nDigiHitsV2_data["data"])
            
            nSimHits_data = GetData1D( puDict[pu][sg].hSimHits() , 1 )
            nSimHitsList.append(nSimHits_data["data"])
            
            nUnknownsRatio_data = GetData1D( puDict[pu][sg].hUnknownRatio() , 1 )
            nUnknownsRatioList.append(nUnknownsRatio_data["data"])
            
            nOnes_data = GetData1D( puDict[pu][sg].hOnes() , 1 )
            nOnesList.append(nOnes_data["data"])
            
            nUnknowns_data = GetData1D( puDict[pu][sg].hUnknowns() , 1 )
            nUnknownsList.append(nUnknowns_data["data"])
            
            
            nTotals_data = GetData1D( puDict[pu][sg].hNtotal() , 1 )
            nTotalsList.append(nTotals_data["data"])
            
            nTotalsMinusUnknowns_data = GetData1D( puDict[pu][sg].hNTotalsMinusUnknowns() , 1 )
            nTotalsMinusUnknownsList.append(nTotalsMinusUnknowns_data["data"])
            
            rhoVect = nTotals_data["xAxis"]
            
            ToaRho_data = GetData2D(puDict[pu][sg].hToaRho() , 1 , 7)
            #ToaRho_data.pop("xAxis")
            ToaRhoList.append(ToaRho_data)

            TotRho_data = GetData2D(puDict[pu][sg].hTotRho() , 1 , 7)
            #TotRho_data.pop("xAxis")
            TotRhoList.append(TotRho_data)

            TofRho_data = GetData2D(puDict[pu][sg].hTofRho() , 1 , 7)
            #TofRho_data.pop("xAxis")
            TofRhoList.append(TofRho_data)
            
            BxTofRho_data = GetData2D(puDict[pu][sg].hBxTofRho() , 1 , 7)
            #BxTofRho_data.pop("xAxis")
            BxTofRhoList.append(BxTofRho_data)
            
            
        SensorDict['puVect']= puVect
        SensorDict['rVect']= rhoVect
        SensorDict['nZeros']= np.array(nZerosList)
        SensorDict['nDigiHits']= np.array(nDigiHitsList)
        SensorDict['nDigiHitsV2']= np.array(nDigiHitsV2List)
        SensorDict['nSimHits']= np.array(nSimHitsList)
        SensorDict['nUnknownsRatio']= np.array(nUnknownsRatioList)
        SensorDict['nOnes']= np.array(nOnesList)
        SensorDict['nUnknowns']= np.array(nUnknownsList)
        SensorDict['nTotals']= np.array(nTotalsList)
        SensorDict['nTotalsMinusUnknownsList'] = np.array(nTotalsMinusUnknownsList)
        
        SensorDict["ToA"] = np.array(ToaRhoList)
        SensorDict["ToT"] = np.array(TotRhoList)
        SensorDict["ToF"] = np.array(TofRhoList)
        SensorDict["BxToF"] = np.array(BxTofRhoList)
                        
        AllSensors.append(SensorDict)

        
    AllResultsDict[opt.srcType] = {"SensorGroup":AllSensors}
    SensDict=AllResultsDict[opt.srcType]["SensorGroup"][7]
    x=SensDict['puVect']
    y=SensDict['nZeros'][0:8,14]
    # print(x) 
    # print(y)
    #sio.savemat("ResultsMat_{0}.mat".format(opt.srcType), AllResultsDict)
    ffit1 = ROOT.TF1("ffit1", "pol1", 0., 200.);
    ffit2 = ROOT.TF1 ("ffit2", " [0]+[1]*x", 0., 200. )
    ffit1.SetLineColor(3);
    ffit2.SetLineColor(2);
    myc = ROOT.TCanvas("myc", "Linear fit and data");
    #x = [0.5, 1 , 1.5, 10]
    #y = [1, 2, 3 , 4]
    #e = [.1, .1, .1, .1]
    #array.array('d' , self.pus) , array.array('d' , self.YVals )
    grr = ROOT.TGraph(8, array.array('d',x), array.array('d' , y));
    myc.SetGrid();
    
    grr.Fit(ffit1,"Q","+",0.5,200.);
#    grr.Fit(ffit2);
    grr.Fit(ffit2,"Q","+",0.5,50.);
    grr.Draw("AL*");
    #myc.BuildLegend()
    leg = ROOT.TLegend(0.2, 0.2); #, 0.4, 0.89
    leg.AddEntry(ffit1, "fit 1", "l");
    leg.AddEntry(ffit2, "fit 2", "l"); 
    leg.AddEntry(grr, "data", "l");
    #leg->AddEntry(ffit2, "LTS regression", "l");
    leg.Draw();
    myc.SaveAs( 'testGraph.png' )
    
    return 0

if __name__ == "__main__":
    sys.exit( main() )
