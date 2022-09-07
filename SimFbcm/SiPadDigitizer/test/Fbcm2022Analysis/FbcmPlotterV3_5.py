#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os 
import sys
import argparse 

import os
def getInputFileList(baseDirectory, beginsWithTheseChars, PFN_LFN ): # with "/" at the end
    # baseDir = "/".join(baseDirectory.split('/')[:-1]) + "/"
    baseDir = baseDirectory
    if PFN_LFN == "PFN":
        storeDir=baseDir
    elif PFN_LFN == "LFN":
        storeDir = "/" + "/".join(baseDir.split('/')[3:])
    else:
        print ('pls specify PFL or LFN')
        
    subDirs = os.listdir(baseDir)
    minBiasFiles = []
    for folder in subDirs:
        minBiasDirectory = baseDir + folder
        filesinDirectory = [storeDir + folder + "/" + f for f in os.listdir(minBiasDirectory) if f[:len(beginsWithTheseChars)] == beginsWithTheseChars]
        minBiasFiles = minBiasFiles + filesinDirectory
    return minBiasFiles



def WriteAtBase(outdir , numOfSensorGroups ):
        #outdir.mkdir( 'numOfSensorGroups' ).cd()
        outdir.cd()
        nSensorGroups = ROOT.TH1F("hnSensorGroups" , "number of Sensor groups" , 1, 0. , 1. )
        nSensorGroups.Fill( 0.5 , numOfSensorGroups )
        nSensorGroups.Write()

class SensorGroupInformation:
    def MakeHistoPerRho(self , hname , htitle ):
        a = ROOT.TH1F("h{0}_SG{1}".format( hname , self.SensorGroup ) , htitle , self.RhoNBins, self.RhoStart , self.RhoEnd )
        return a

    def Make2DHistoPerRho(self , hname , htitle , nbins , start , end ):
        a = ROOT.TH2F("h{0}_SG{1}".format( hname , self.SensorGroup ) , htitle , self.RhoNBins, self.RhoStart , self.RhoEnd , nbins , start , end )
        return a


    def __init__(self , sensorGroup , rhonBins = 25 , rhoStart = 8.75 , rhoEnd = 21.25):
        self.SensorGroup = sensorGroup
        self.RhoNBins = rhonBins
        self.RhoStart = rhoStart
        self.RhoEnd = rhoEnd
        
        #self.numOfBxSlots = self.MakeHistoPerRho('numOfBxSlots' , 'number of BX slots at digi' )
        self.numOfBxSlots  = ROOT.TH1F("h{0}_SG{1}".format( 'numOfBxSlots' , self.SensorGroup ) , "number of BX slots at digi" , 1, 0. , 1. )
        
        self.nSensors = self.MakeHistoPerRho( 'nSensors' , 'number of sensors' )
        self.SensorsArea = self.MakeHistoPerRho("SensorsArea" , "Sensors area" )
        
        self.nSimHits = self.MakeHistoPerRho('nSimHits' , 'number of sim hits' )
        self.nDigiHits = self.MakeHistoPerRho('nDigiHits' , 'number of digi hits' )
        self.nDigiHitsV2 = self.MakeHistoPerRho('nDigiHitsV2' , 'number of digi hits when unknowns were ignored' )
        self.nOnes = self.MakeHistoPerRho( 'nOnes' , 'number of Ones' ) # ones means non-zero
        self.nUnknowns = self.MakeHistoPerRho('nUnknowns' , 'number of unknowns')
        
        self.nInterstedBinRhuHits = self.MakeHistoPerRho('nInterstedBinRhuHits' , 'number of detected hits counted at the interested bin of RHU')
        self.nTotalRhuHitsPerBx = self.MakeHistoPerRho('nTotalRhuHitsPerBx' , 'Total number hits counted all RHU bins of a Bx')
        self.nOnesAtRhuBin = self.MakeHistoPerRho('nOnesAtRhuBin' , 'number of Ones (boolian: non-zero considered as one) in the interested RHU bin')
        
        # 1./1.28/n or (25./32./n) is the sampling period @1.28Gbps. note that n is an arbitray intiger to make a fine time-bin, near to the 1/FS
        # then if you rebin by n, this leads to the exact lpGBT sampling. 
        # orginal sampling in the Ferquecy domiain is 1/FS
        self.TofRho = self.Make2DHistoPerRho( 'TofRho' , ';Rho;ToF' , int(round(200./(1./1.28/7.))) , -100 , 100 )
        self.BxTofRho = self.Make2DHistoPerRho( 'BxTofRho' , ';Rho;ToF' , int(round(30./(1./1.28/7.))) , -15. , 15. )
        self.ToaRho = self.Make2DHistoPerRho( 'ToaRho' , ';Rho;ToA' , int(round(30./(1./1.28/7.))) , -15. , 15. )
        self.TotRho = self.Make2DHistoPerRho( 'TotRho' , ';Rho;ToT' , int(round(50./(1./1.28/7.))) , 0. , 50. )
        self.RHURho = self.Make2DHistoPerRho( 'RhuRho' , ';Rho;RHU' , 30 , -15.0 , 15.0 ) 
        self.PeakAmpl = self.Make2DHistoPerRho( 'PeakAmplitude' , ';Rho;Ampl' , 800 , 0.0 , 650. ) 
        self.SumChargeRho = self.Make2DHistoPerRho( 'SumCharge' , ';Rho;SumCharge' , 1000 , 0. , 130000. )
        
        
    def FillGeometry(self , geoTree ):
        for entry in geoTree:
            if entry.SiDieGroupIndex == self.SensorGroup:
                self.SensorGroupArea = entry.SensorX* entry.SensorY
                
                self.nSensors.Fill( entry.SensorRho  )
                self.SensorsArea.Fill( entry.SensorRho , self.SensorGroupArea )
                
    def SetNumOfBxSlots(self , nBxSlots ):
        self.numOfBxSlots.Fill(0.5, nBxSlots)


    def FillHit( self , hit ):
        if hit.SensorGroupIndex != self.SensorGroup:
            return -1

        self.nSimHits.Fill( hit.SensorRho, hit.nSimParticles )
        self.nDigiHits.Fill( hit.SensorRho , hit.nValidDigiToAs )
        
        self.nInterstedBinRhuHits.Fill(hit.SensorRho, hit.nInterstedRhuBins)
        self.nTotalRhuHitsPerBx.Fill(hit.SensorRho, hit.nTotalRhuDigi)
        self.nOnesAtRhuBin.Fill(hit.SensorRho, bool(hit.nInterstedRhuBins)) # may not differ from nInterstedRhuBins
        
        
        for spart in range( hit.nSimParticles ):
            self.TofRho.Fill( hit.SensorRho, hit.SimTof[spart] )
            self.BxTofRho.Fill( hit.SensorRho, hit.SimTof_perBx[spart] )
            self.SumChargeRho.Fill(hit.SensorRho, hit.SimCharge[spart])
            
        
        for bx in range(hit.BxSlotCnt): 
            if  hit.DigiHitStatus[bx]==-1:
                self.nUnknowns.Fill( hit.SensorRho )
            elif hit.DigiHitStatus[bx] == 1:
                self.nOnes.Fill( hit.SensorRho )
                self.nDigiHitsV2.Fill(hit.SensorRho, hit.nDigiHits[bx])
			

        for i in hit.DigiToA:
            self.ToaRho.Fill( hit.SensorRho , i )
        for j in hit.DigiToT:
            self.TotRho.Fill( hit.SensorRho , j )
        
        for j in hit.DigiRHU:
            self.RHURho.Fill( hit.SensorRho , j )
            
        for j in hit.PeakAmplitude:
            self.PeakAmpl.Fill( hit.SensorRho , j )

    # def WriteAtBase(self , numOfSensorGroups ):
        # self.nSensorGroups = ROOT.TH1F("hnSensorGroups" , "number of Sensor groups" , 1, 0. , 1. )
        # self.nSensorGroups.Fill( 0.5 , numOfSensorGroups )
        # self.nSensorGroups.Write()
        
    def Write(self , outdir , nevents ):
        outdir.mkdir( 'SensorGroup{0}'.format( self.SensorGroup ) ).cd()
        
        self.nSimHits.Write()
        self.nDigiHits.Write()
        self.nDigiHitsV2.Write()
        self.nOnes.Write()
        self.nUnknowns.Write()
        
        self.nInterstedBinRhuHits.Write()
        self.nTotalRhuHitsPerBx.Write()
        self.nOnesAtRhuBin.Write()
        
        
        self.numOfBxSlots.Write()
        
        self.nTotals = self.MakeHistoPerRho('TotalNumbers' , 'number of total events*sensors' )
        self.nTotals.Add( self.nSensors , nevents )
        self.nTotals.Write()
        

        self.TotRho.Write()
        self.ToaRho.Write()
        self.TofRho.Write()
        self.BxTofRho.Write()
        
        self.RHURho.Write()
        self.PeakAmpl.Write()
        self.SumChargeRho.Write()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '-i' , '--infile' , dest='infiles' , help='the name of the input files' , type=str , nargs="+" )
    parser.add_argument( '-p' , '--pu' , dest='PU' , default='auto' , help='the pu of the file' , type=str , choices=['auto' , '0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200'])
    parser.add_argument( '-o' , '--outfile' , dest='outfile' , default='auto' , help='the name of the output file' , type=str )
    parser.add_argument( '-d' , '--dir' , dest='inDir' , help='the directory of input files' , type=str )
    parser.add_argument( '-t' , '--tag' , dest='tag' , help='the instance name' , type=str )

    opt = parser.parse_args()
    
    if not opt.tag:
        print('please specify the the tag (instance Name) using -t option')
        return 1

    if not opt.infiles and not opt.inDir:
        print('please specify the input file name using -i option, OR \n specify the input directory using -d option')
        return 1
    if opt.infiles and  opt.inDir:
        print('please use only -i or -d options')
        return 1
    
    
    if opt.inDir:
        baseDirectory = opt.inDir
        opt.infiles = getInputFileList(baseDirectory, "outFbcm2022", 'PFN' )
        print(opt.infiles)
   
    # print(opt.infiles)
    if opt.PU == 'auto':
        for pu in ['0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200']:
            if 'pu{0}'.format( pu ) in opt.infiles[0]:
                opt.PU = pu
                print( 'pu set to ' + opt.PU)
    
    if opt.outfile == 'auto':
        #infileName = os.path.basename( opt.infiles[0] )
        #print(infileName)
        #instanceName= infileName.split('_')[1]
        instanceName = opt.tag
        outNameFile = "./output/results/"+"outPlotterMerged_"+instanceName+"_pu{}".format(opt.PU)+".root"
        opt.outfile = outNameFile
        print(outNameFile)
        
        
        
    

    print( 'output will be stored in ' + opt.outfile )
    
    fIn = ROOT.TFile.Open( opt.infiles[0] )
    nSensorGroups = int(fIn.Get("FbcmNtuple/"+opt.tag+"/hNSensorGroups").GetBinContent( 1 ))
    fIn.Close()
    #print(nSensorGroups)

    
    nEvents = 0
    allHits = ROOT.TChain("FbcmNtuple/{0}/PU{1}".format(opt.tag , opt.PU ) )
    for f in opt.infiles:
        fIn = ROOT.TFile.Open( f )
        nEvents += fIn.Get("FbcmNtuple/"+opt.tag+"/hNEvents").GetBinContent( 1 )
        fIn.Close()
        allHits.Add( f )

    
    sampleHit = next(iter(allHits))
    #print(sampleHit.BxSlotCnt)
    allSensorGroups = { i:SensorGroupInformation( i ) for i in range(nSensorGroups) }
    fIn = ROOT.TFile.Open( opt.infiles[0] )
    for _,j in allSensorGroups.items():
        j.FillGeometry( fIn.Get('FbcmNtuple/'+opt.tag+'/GeometryInfo') )
        j.SetNumOfBxSlots(sampleHit.BxSlotCnt)
    fIn.Close()

    for hit in allHits:
        for _,j in allSensorGroups.items():
            j.FillHit( hit )

    fout = ROOT.TFile.Open( opt.outfile , "recreate")
    for _,j in allSensorGroups.items():
        j.Write( fout , nEvents )
    
    WriteAtBase(fout, nSensorGroups)
    
    fout.Close()
    return 0

if __name__ == "__main__":
    sys.exit( main() )
