#! /usr/bin/env python

# VERSION Track: 
# this is _v8 which is prepared to save for Matlab, based on the new BCM1F Gemetry and the New FBCM2022
# _v7 which was prepared to save for Matlab, based on the new Gemetry and the last run for TDR 
# _7 was based on "ExtractPlots_v5", and "nZerosV0" was added to this version.
# this file is newer than "ExtractPlots_v5", but lacks the Root fitting in _v6 (which is based on root fitting)
# one should merge the changes of _v6 (modified by H.Bakhshian) to this file. 

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


# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.colors import BoundaryNorm
# from matplotlib.ticker import MaxNLocator
import numpy as np
import scipy.io as sio

NumOfBxInMixing = 7.0 # -3:3, i.e. 

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
        
        self.hnDigiBxSlots = self.InDir.Get("h{0}_SG{1}".format( 'numOfBxSlots' , self.SensorGroup ) )
        self.nBxSlotsInDigi = (self.hnDigiBxSlots.GetBinContent(1)) # GetData1D(self.hnDigiBxSlots , 1)
        #print("NumofBx slots is {0}".format(self.nBxSlotsInDigi))
        
        self.nSimHits = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nSimHits' , self.SensorGroup ) ) )
        self.nDigiHits = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nDigiHits' , self.SensorGroup ) ) )
        self.nDigiHitsV2 = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nDigiHitsV2' , self.SensorGroup ) ) )
        self.nOnes = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nOnes' , self.SensorGroup ) ) )
        self.nUnknowns = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nUnknowns' , self.SensorGroup ) ) )
        self.nTotals = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'TotalNumbers' , self.SensorGroup ) ) ) 
        
        self.nTotalRhuHitsPerBx = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nTotalRhuHitsPerBx' , self.SensorGroup ) ) ) 
        self.nInterstedBinRhuHits = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nInterstedBinRhuHits' , self.SensorGroup ) ) ) 
        self.nOnesAtRhuBin = self.CopyH1IToH1F( self.InDir.Get( 'h{0}_SG{1}'.format( 'nOnesAtRhuBin' , self.SensorGroup ) ) ) 
        
        
        
        self.TotRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'TotRho' , self.SensorGroup ) )
        self.ToaRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'ToaRho' , self.SensorGroup ) )
        self.TofRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'TofRho' , self.SensorGroup ) )
        self.BxTofRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'BxTofRho' , self.SensorGroup ) ) 
        
        self.RhuRho = self.InDir.Get( 'h{0}_SG{1}'.format( 'RhuRho' , self.SensorGroup ) )
        self.PeakAmpl = self.InDir.Get( 'h{0}_SG{1}'.format( 'PeakAmplitude' , self.SensorGroup ) )
        
        self.nSimHits.Divide( self.nTotals )
        self.nSimHits.Scale( 1.0/NumOfBxInMixing )
        
        self.nTotals.Scale( self.nBxSlotsInDigi ) # x3 in early version 
        
        self.nUnknownsRatio = self.nUnknowns.Clone("nUnknownsRatio_SG{0}".format(self.SensorGroup))
        self.nUnknownsRatio.Divide( self.nTotals )
        
        self.nDigiHits.Divide( self.nTotals )
        self.nTotalsMinusUnknowns = self.nTotals.Clone("nTotalsMinusUnknowns_SG{0}".format(self.SensorGroup))
        self.nZeros = self.nTotals.Clone("nZeros_SG{0}".format(self.SensorGroup)) 
        self.nZeros.Add( self.nOnes , -1.0 ) 
        
        self.nZerosV0 = self.nZeros.Clone("nZerosV0_SG{0}".format(self.SensorGroup)) 
        
        self.nZeros.Add( self.nUnknowns , -1.0 )
        self.nTotalsMinusUnknowns.Add( self.nUnknowns , -1.0 )
        self.nZeros.Divide( self.nTotalsMinusUnknowns )
        self.nDigiHitsV2.Divide(self.nTotalsMinusUnknowns)
        for b in range( self.nZeros.GetNbinsX() ) :
            bc = self.nZeros.GetBinContent(b+1)
            if bc > 0:
                self.nZeros.SetBinContent( b + 1 , -math.log( bc ) )

        self.nZerosV0.Divide( self.nTotals )
        for b in range( self.nZerosV0.GetNbinsX() ) :
            bc = self.nZerosV0.GetBinContent(b+1)
            if bc > 0:
                self.nZerosV0.SetBinContent( b + 1 , -math.log( bc ) )
                
        self.rhuTimingEfficiency = self.nInterstedBinRhuHits.Clone("rhuTimingEfficiency_SG{0}".format(self.SensorGroup))
        self.rhuTimingEfficiency.Divide( self.nTotalRhuHitsPerBx )
        
        #self.nTotalRhuHitsPerBx.Scale( self.nBxSlotsInDigi )
        
        self.nRhuZeors = self.nTotals.Clone("nRhuZeors_SG{0}".format(self.SensorGroup)) 
        self.nRhuZeors.Add( self.nOnesAtRhuBin , -1.0 ) 
        
        self.lambdaDigiZC_Rhu = self.nRhuZeors.Clone("lambdaDigiZCntRhu_SG{0}".format(self.SensorGroup)) 
        self.lambdaDigiZC_Rhu.Divide( self.nTotals )
        for b in range( self.lambdaDigiZC_Rhu.GetNbinsX() ) :
            bc = self.lambdaDigiZC_Rhu.GetBinContent(b+1)
            if bc > 0:
                self.lambdaDigiZC_Rhu.SetBinContent( b + 1 , -math.log( bc ) )
        
        
        self.lambdaDigiC_Rhu  =  self.nInterstedBinRhuHits.Clone("lambdaDigiCntRhu_SG{0}".format(self.SensorGroup))
        self.lambdaDigiC_Rhu.Divide( self.nTotals ) 



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
        
    def hZeroV0Counting(self ):
        return self.nZerosV0 

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

    #
    def hPeakAmpl(self ):
        return self.PeakAmpl     
    
    def hRhuRho(self ):
        return self.RhuRho        
        
    def hNTotalRhuHitsPerBx(self ):
        return self.nTotalRhuHitsPerBx        

    def hNInterstedBinRhuHits(self ):
        return self.nInterstedBinRhuHits        
            
    def hRhuTimingEfficiency(self ):
        return self.rhuTimingEfficiency        
            
    def hNrhuZeors(self ):
        return self.nRhuZeors        

    def hLambdaDigiZCntRhu(self ):
        return self.lambdaDigiZC_Rhu        

    def hLambdaDigiCntRhu(self ):
        return self.lambdaDigiC_Rhu        
    #
    
    def WriteBxTof(self, Rho):
        self.c2 = ROOT.TCanvas('Tof_PU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.BxTofRho.ProjectionY("py",b)
        y_proj.SetName(self.BxTofRho.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        BxTof_1FH = ROOT.TH1F()
        y_proj.Copy(BxTof_1FH)
        BxTof_1FH.SetTitle( 'Tof' )
        BxTof_1FH.SetStats( False )
        BxTof_1FH.Rebin(2)
        BxTof_1FH.GetXaxis().SetRangeUser(-0.,25.0)
        BxTof_1FH.Draw()
        self.c2.BuildLegend()
        self.c2.SaveAs( self.destDir + '{0}.png'.format( self.c2.GetName() ) )
        
    def WriteToA(self, Rho):
        self.c2 = ROOT.TCanvas('ToA_PU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.ToaRho.ProjectionY("py",b)
        y_proj.SetName(self.ToaRho.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        ToA_1FH = ROOT.TH1F()
        y_proj.Copy(ToA_1FH)
        ToA_1FH.SetTitle( 'ToA' )
        ToA_1FH.SetStats( False )
        ToA_1FH.Rebin(2)
        ToA_1FH.GetXaxis().SetRangeUser(-15.,15.)
        ToA_1FH.Draw()
        self.c2.BuildLegend()
        self.c2.SaveAs( self.destDir + '{0}.png'.format( self.c2.GetName() ) )
        
    def WriteToT(self, Rho):
        self.c2 = ROOT.TCanvas('ToT_PU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.TotRho.ProjectionY("py",b)
        y_proj.SetName(self.TotRho.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        ToT_1FH = ROOT.TH1F()
        y_proj.Copy(ToT_1FH)
        ToT_1FH.SetTitle( 'ToT' )
        ToT_1FH.SetStats( False )
        ToT_1FH.Rebin(7)
        ToT_1FH.GetXaxis().SetRangeUser(-5.,35.)
        ToT_1FH.Draw()
        self.c2.BuildLegend()
        self.c2.SaveAs( self.destDir + '{0}.png'.format( self.c2.GetName() ) )
        
    def WriteAmpl(self, Rho):
        self.c2 = ROOT.TCanvas('Amplitude_mV_PU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.PeakAmpl.ProjectionY("py",b)
        y_proj.SetName(self.PeakAmpl.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        Ampl_1FH = ROOT.TH1F()
        y_proj.Copy(Ampl_1FH)
        Ampl_1FH.SetTitle( 'Ampl(mV)' )
        Ampl_1FH.SetStats( False )
        Ampl_1FH.Rebin(4)
        Ampl_1FH.GetXaxis().SetRangeUser(0.0,400.0)
        Ampl_1FH.Draw()
        self.c2.BuildLegend()
        self.c2.SaveAs( self.destDir + '{0}.png'.format( self.c2.GetName() ) )
        
    def WriteRhu(self, Rho):
        self.c2 = ROOT.TCanvas('Rhu_PU{0}SG{1}'.format( self.PU , self.SensorGroup ), 'PU{0}SG{1}'.format( self.PU , self.SensorGroup ) )
        #Tpadd=ROOT.TPad("H1","H2",)
        b = self.nSimHits.FindBin(Rho)
        y_proj = self.RhuRho.ProjectionY("py",b)
        y_proj.SetName(self.RhuRho.GetName()+"_projY{0}".format(self.SensorGroup))
        y_proj.Draw("same, hist")
        Rhu_1FH = ROOT.TH1F()
        y_proj.Copy(Rhu_1FH)
        Rhu_1FH.SetTitle( 'Rhu' )
        Rhu_1FH.SetStats( False )
        Rhu_1FH.Rebin(1)
        Rhu_1FH.GetXaxis().SetRangeUser(-6,6)
        Rhu_1FH.Draw()
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
    
 
def getSrcDir(x,ver):
    return {
        'no_aging' : './resultsFbcm'+ver+'/no_aging/aging0_pu',
        'aging_1000': './resultsFbcm'+ver+'/aging_1000/aging1k_pu',
        'aging_3000': './resultsFbcm'+ver+'/aging_3000/aging3k_pu',
        'aging_4000': './resultsFbcm'+ver+'/aging_4000/aging4k_pu',
        'bib_selfMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_SelfMixed/nTuplizerOutput/histResults',
        'bib_noMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_NoMix/nTuplizerOutput/histResults' ,
        'bib_puMix': '/afs/cern.ch/work/m/msedghi/public/BeamInducedBackgrdFbcm/bibDIGI_PileupBibMixed/nTuplizerOutput/histResults',
    }.get(x, '/outPU')  
    
def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '-i' , '--infile' , dest='infile' , help='the name of the input file' , type=str  )
    #parser.add_argument( '-s' , '--src' , dest='srcDir' ,default='.', help='the name of the source base directory' , type=str  )
    parser.add_argument( '-p' , '--pu' , dest='PU' , default=None , help='the pu of the file' , type=str , choices=['0', '0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200', 'all'])
    parser.add_argument( '-t' , '--srcType' , dest='srcType' , default=None , help='the source type' , type=str , choices=['no_aging', 'aging_1000', 'aging_3000' , 'aging_4000' , 'bib_selfMix' , 'bib_noMix' , 'bib_puMix'])
    parser.add_argument( '-v' , '--ver' , dest='srcVer' , default='V2' , help='the source Version directory' , type=str , choices=['V1', 'V2'])
    
    opt = parser.parse_args()
    
    ExplicitInputfile = False
    
    if opt.infile:
        ExplicitInputfile = True
        if opt.infile[0]=='.' :
            destDir="."+"/".join(opt.infile.split(os.sep)[0:-2])+'/'
            opt.srcType = (opt.infile.split(os.sep)[-1]).split('.')[0]
            
        elif opt.infile[0]!='/':
            destDir="."+"/".join(opt.infile.split(os.sep)[0:-2])+'/'
            opt.srcType = opt.infile.split('.')[0]
        else:
            destDir="/".join(opt.infile.split(os.sep)[0:-2])+'/'
            opt.srcType=(opt.infile.split(os.sep)[-1]).split('.')[0]
        
        print(opt.srcType)
        
        print("dest Dir is {0}".format(destDir))
        
        #return
    else:
        if opt.srcType:
            opt_srcDir=getSrcDir(opt.srcType,opt.srcVer)
            print(opt_srcDir)
        #else:
            #opt.srcType = 'no_aging' 
            #opt_srcDir=getSrcDir(opt.srcType)
            
        destDir="/".join(opt_srcDir.split(os.sep)[0:-2])+'/'
        print("dest Dir is")
        print(destDir)
        
    

    
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
        if ExplicitInputfile:
            opt_infile = opt.infile
        else:
            opt_infile = opt_srcDir + pu +".root"
            
        fIn = ROOT.TFile.Open( opt_infile ) 
        hnSensorGroups = fIn.Get("hnSensorGroups")
        nSensorGroups = int(hnSensorGroups.GetBinContent(1))
        #print("number of Sensor groups is {0}".format(nSensorGroups))
        print(opt_infile)
        #sg_list=list()
        sg_list = {}
        for sg in range( nSensorGroups ):
            s = SensorGroupInformation(sg , pu , fIn , destDir)
            #sg_list.append(copy.deepcopy(s))
            s.WriteAmpl(14.5)
            s.WriteRhu(14.5)
            s.WriteToA(14.5)
            s.WriteBxTof(14.5)
            s.WriteToT(14.5)
            
            sg_list[sg]=s
            puDict[pu] = sg_list

    print("------------")

    pu_len = len(opt.PU)
    puVect=np.zeros(pu_len)
    
    #SenDict1Keys = ['puVect','rVect', 'nZeros', 'nDigiHits', 'nDigiHitsV2', 'nSimHits', 'nUnknownsRatio', 'nOnes' , 'nUnknowns', 'nTotals']
    AllResultsDict={}
    AllSensors=[]
    for sg in range( nSensorGroups ):
        #SensorDict = dict.fromkeys(SenDict1Keys, list())
        SensorDict={}
        nZerosList = []
        nZerosV0List = []
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
        #
        nTotalRhuHitsPerBxList = []
        nInterstedBinRhuHitsList = []
        nRhuZeorsList = []
        rhuTimingEfficiencyList = []
        lambdaDigiZCntRhuList = []
        lambdaDigiCntRhuList = []
        
        PeakAmplList = []
        RhuRhoList = []
        #
        
        for pu in opt.PU:
            puVal=puValue(pu)
            puVect[opt.PU.index(pu)] = puVal
            
            nZeros_data = GetData1D( puDict[pu][sg].hZeroCounting() , 1 )
            nZerosList.append(nZeros_data["data"])
            
            nZerosV0_data = GetData1D( puDict[pu][sg].hZeroV0Counting() , 1 )
            nZerosV0List.append(nZerosV0_data["data"])
            
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
            
            ##----------
            tempData = GetData1D( puDict[pu][sg].hNTotalRhuHitsPerBx() , 1 )
            nTotalRhuHitsPerBxList.append(tempData["data"])
            
            tempData = GetData1D( puDict[pu][sg].hNInterstedBinRhuHits() , 1 )
            nInterstedBinRhuHitsList.append(tempData["data"])
            
            tempData = GetData1D( puDict[pu][sg].hNrhuZeors() , 1 )
            nRhuZeorsList.append(tempData["data"])
            
            tempData = GetData1D( puDict[pu][sg].hRhuTimingEfficiency() , 1 )
            rhuTimingEfficiencyList.append(tempData["data"])
            
            tempData = GetData1D( puDict[pu][sg].hLambdaDigiZCntRhu() , 1 )
            lambdaDigiZCntRhuList.append(tempData["data"])            

            tempData = GetData1D( puDict[pu][sg].hLambdaDigiCntRhu() , 1 )
            lambdaDigiCntRhuList.append(tempData["data"])  

            
            tempData = GetData2D(puDict[pu][sg].hPeakAmpl() , 1 , 1)
            PeakAmplList.append(tempData)
            
            tempData = GetData2D(puDict[pu][sg].hRhuRho() , 1 , 1)
            RhuRhoList.append(tempData)            
            
            ##----------
            
            
        SensorDict['puVect']= puVect
        SensorDict['rVect']= rhoVect
        SensorDict['nZeros']= np.array(nZerosList)
        SensorDict['nZerosV0']= np.array(nZerosV0List)
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
        
        #
        
        SensorDict["PeakAmpl"] = np.array(PeakAmplList)
        SensorDict["Rhu"] = np.array(RhuRhoList)
        SensorDict["TotalRhuHitsPerBx"] = np.array(nTotalRhuHitsPerBxList)
        SensorDict["InterstedBinRhuHits"] = np.array(nInterstedBinRhuHitsList)
        SensorDict["RhuZeors"] = np.array(nRhuZeorsList)
        SensorDict["rhuTimingEff"] = np.array(rhuTimingEfficiencyList)
        SensorDict["lambdaDigiZCntRhu"] = np.array(lambdaDigiZCntRhuList)
        SensorDict["lambdaDigiCntRhu"] = np.array(lambdaDigiCntRhuList)
        #
                        
        AllSensors.append(SensorDict)

        
    AllResultsDict[opt.srcType] = {"SensorGroup":AllSensors}
    sio.savemat(destDir+"ResultsMat_{0}.mat".format(opt.srcType), AllResultsDict)
    
    
    return 0

if __name__ == "__main__":
    sys.exit( main() )
