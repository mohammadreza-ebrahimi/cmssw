#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os 
import sys
import argparse 

class SensorGroupInformation:
    def MakeHistoPerRho(self , hname , htitle ):
        a = ROOT.TH1F("h{0}_SG{1}".format( hname , self.SensorGroup ) , htitle , self.RhoNBins, self.RhoStart , self.RhoEnd )
        return a

    def Make2DHistoPerRho(self , hname , htitle , nbins , start , end ):
        a = ROOT.TH2F("h{0}_SG{1}".format( hname , self.SensorGroup ) , htitle , self.RhoNBins, self.RhoStart , self.RhoEnd , nbins , start , end )
        return a


    def __init__(self , sensorGroup , rhonBins = 30 , rhoStart = 0 , rhoEnd = 30):
        self.SensorGroup = sensorGroup
        self.RhoNBins = rhonBins
        self.RhoStart = rhoStart
        self.RhoEnd = rhoEnd

        self.nSensors = self.MakeHistoPerRho( 'nSensors' , 'number of sensors' )
        self.SensorsArea = self.MakeHistoPerRho("SensorsArea" , "Sensors area" )
        
        self.nSimHits = self.MakeHistoPerRho('nSimHits' , 'number of sim hits' )
        self.nDigiHits = self.MakeHistoPerRho('nDigiHits' , 'number of digi hits' )
        self.nDigiHitsV2 = self.MakeHistoPerRho('nDigiHitsV2' , 'number of digi hits when unknowns were ignored' )
        self.nOnes = self.MakeHistoPerRho( 'nOnes' , 'number of Ones' )
        self.nUnknowns = self.MakeHistoPerRho('nUnknowns' , 'number of unknowns')
        
        self.TofRho = self.Make2DHistoPerRho( 'TofRho' , ';Rho;ToF' , int(round(200./(25./32./7.))) , -100 , 100 )
        self.BxTofRho = self.Make2DHistoPerRho( 'BxTofRho' , ';Rho;ToF' , int(round(30./(25./32./7.))) , -15. , 15. )
        self.ToaRho = self.Make2DHistoPerRho( 'ToaRho' , ';Rho;ToA' , int(round(30./(25./32./7.))) , -15. , 15. )
        self.TotRho = self.Make2DHistoPerRho( 'TotRho' , ';Rho;ToT' , int(round(200./(25./32./7.))) , 0. , 200. )

    def FillGeometry(self , geoTree ):
        for entry in geoTree:
            if entry.SensorGroupIndex == self.SensorGroup:
                self.SensorGroupArea = entry.SensorX* entry.SensorY
                
                self.nSensors.Fill( entry.SensorRho  )
                self.SensorsArea.Fill( entry.SensorRho , self.SensorGroupArea )


    def FillHit( self , hit ):
        if hit.SensorGroupIndex != self.SensorGroup:
            return -1

        self.nSimHits.Fill( hit.SensorRho, hit.nSimParticles )
        self.nDigiHits.Fill( hit.SensorRho , hit.nValidDigiToAs )

        for spart in range( hit.nSimParticles ):
            self.TofRho.Fill( hit.SensorRho, hit.SimTof[spart] )
            self.BxTofRho.Fill( hit.SensorRho, hit.SimTof_perBx[spart] )

        for bx in range(3):
            if  hit.DigiHitStatus[bx]==-1:
                self.nUnknowns.Fill( hit.SensorRho )
            elif hit.DigiHitStatus[bx] == 1:
                self.nOnes.Fill( hit.SensorRho )
                self.nDigiHitsV2.Fill(hit.SensorRho, hit.nDigiHits[bx])
			

        for i in hit.DigiToA:
            self.ToaRho.Fill( hit.SensorRho , i )
        for j in hit.DigiToT:
            self.TotRho.Fill( hit.SensorRho , j )

    def Write(self , outdir , nevents ):
        outdir.mkdir( 'SensorGroup{0}'.format( self.SensorGroup ) ).cd()
        
        self.nSimHits.Write()
        self.nDigiHits.Write()
        self.nDigiHitsV2.Write()
        self.nOnes.Write()
        self.nUnknowns.Write()
        
        self.nTotals = self.MakeHistoPerRho('TotalNumbers' , 'number of total events*sensors' )
        self.nTotals.Add( self.nSensors , nevents )
        self.nTotals.Write()
        

        self.TotRho.Write()
        self.ToaRho.Write()
        self.TofRho.Write()
        self.BxTofRho.Write()

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '-i' , '--infile' , dest='infiles' , help='the name of the input files' , type=str , nargs="+" )
    parser.add_argument( '-p' , '--pu' , dest='PU' , default='auto' , help='the pu of the file' , type=str , choices=['auto' , '0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200'])
    parser.add_argument( '-o' , '--outfile' , dest='outfile' , default='auto' , help='the name of the output file' , type=str )

    opt = parser.parse_args()

    if not opt.infiles:
        print('please specify the input file name using -i option')
        return 1
    if opt.outfile == 'auto':
        opt.outfile = os.path.basename( opt.infiles[0] )
        print( 'output will be stored in ' + opt.outfile )
    if opt.PU == 'auto':
        for pu in ['0p5', '1' , '1p5' , '10' , '50' , '100' , '140' , '200']:
            if 'PU{0}/'.format( pu ) in opt.infiles[0]:
                opt.PU = pu
                print( 'pu set to ' + opt.PU)

    nEvents = 0
    allHits = ROOT.TChain("FbcmNtuple/PU{0}".format( opt.PU ) )
    for f in opt.infiles:
        fIn = ROOT.TFile.Open( f )
        nEvents += fIn.Get("FbcmNtuple/hNEvents").GetBinContent( 1 )
        fIn.Close()
        allHits.Add( f )

    allSensorGroups = { i:SensorGroupInformation( i ) for i in range(8) }
    fIn = ROOT.TFile.Open( opt.infiles[0] )
    for _,j in allSensorGroups.items():
        j.FillGeometry( fIn.Get('FbcmNtuple/GeometryInfo') )
    fIn.Close()

    for hit in allHits:
        for _,j in allSensorGroups.items():
            j.FillHit( hit )


	simhitsPerRho.Divide( totalAreaPerRho )
	digiHitsPerRho.Divide( totalAreaPerRho )
	
	fout = ROOT.TFile.Open( opt.outfile , "recreate")
	simhitsPerRho.Write()
	digiHitsPerRho.Write()
	#sensorsPerRho.Write()
	#totalAreaPerRho.Write()
        simhitsPerRho.Scale( 1.0/7.0 )
        digiHitsPerRho.Divide( totalAreaPerRho )
        digiHitsPerRho.Scale( 1.0/3.0 )
        fout.close()
        return 0


    fout = ROOT.TFile.Open( opt.outfile , "recreate")
    for _,j in allSensorGroups.items():
        j.Write( fout , nEvents )
    fout.Close()
    return 0

if __name__ == "__main__":
    sys.exit( main() )
