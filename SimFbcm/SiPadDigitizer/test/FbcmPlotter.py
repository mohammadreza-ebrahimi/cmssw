#! /usr/bin/env python

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import os 
import sys
import argparse 


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '-i' , '--infile' , dest='infile' , default=None , help='the name of the input file' , type=str )
    parser.add_argument( '-s' , '--SensorGroupIndex' , dest='SensorGroupIndex' , default=0 , help='the sensor group index' , type=int , choices=[i for i in range(8)])
    parser.add_argument( '-o' , '--outfile' , dest='outfile' , default='auto' , help='the name of the output file' , type=str )

    opt = parser.parse_args()

    if not opt.infile:
        print('please specify the input file name using -s option')
        return 1
    if opt.outfile == 'auto':
        opt.outfile = "{0}_{1}.root".format(opt.infile.split('.')[0] , opt.SensorGroupIndex)

        
    fIn = ROOT.TFile.Open( opt.infile )
    
    geometryInfo = fIn.Get('FbcmNtuple/GeometryInfo')

    sensorsPerRho = ROOT.TH1I("hSensorsPerRho" , "Sensors per row" , 30 , 0 , 30 )
    geometryInfo.Draw( "SensorRho >> hSensorsPerRho" , "SensorGroupIndex=={0}".format( opt.SensorGroupIndex ) )

    totalAreaPerRho = ROOT.TH1D("hTotalAreaPerRho" , "" , 30 , 0 , 30 )
    geometryInfo.Draw("SensorRho >> hTotalAreaPerRho" , "SensorX*SensorY*(SensorGroupIndex=={0})".format( opt.SensorGroupIndex ) )

    allHits = fIn.Get('FbcmNtuple/SensorSize_{0}'.format( opt.SensorGroupIndex ) )
    simhitsPerRho = ROOT.TH1D("hSimHitsPerRho" , "Sim Hits per rho" , 30 , 0 , 30 )
    digiHitsPerRho = ROOT.TH1D("hDigiHitsPerRho" , "Digi Hits per rho" , 30 , 0 , 30 )

    for hit in allHits:
        simhitsPerRho.Fill( hit.SensorRho, hit.nSimParticles )

        for bx in range(3):
            if  hit.DigiHitStatus[bx]==1:
                digiHitsPerRho.Fill(hit.SensorRho )
    
	simhitsPerRho.Divide( totalAreaPerRho )
	digiHitsPerRho.Divide( totalAreaPerRho )
	
	fout = ROOT.TFile.Open( opt.outfile , "recreate")
	simhitsPerRho.Write()
	digiHitsPerRho.Write()
	#sensorsPerRho.Write()
	#totalAreaPerRho.Write()
        simhitsPerRho.Scale( 1.0/7.0 )
        digiHitsPerRho.Scale( 1.0/3.0 )
        fout.Close()
        return 0

if __name__ == "__main__":
    sys.exit( main() )
