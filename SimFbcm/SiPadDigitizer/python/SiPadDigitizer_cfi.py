import FWCore.ParameterSet.Config as cms

from SimFbcm.SiPadDigitizer.SiPadSimParameters_cfi import SiPadSimBlock
from SimFbcm.SiPadDigitizer.SiPadFrontEndParameters_cfi import *


SiPadDigitizer = cms.PSet(
    accumulatorType = cms.string("SiPadDigitizer"), 
    hitsProducer = cms.string('g4SimHits'), 
	SubdetName=cms.string('FBCMHits'), 
	GeometryType = cms.string('idealForDigi'), 
	InstanceName = cms.string('SiPad'), 
	SiPadSimParam = cms.PSet(SiPadSimBlock),
	FFT_SimParam = cms.PSet(fftSimParam),
	SiPadFrontEndParam = cms.VPSet( SiPadFrontEndBlock0,
									SiPadFrontEndBlock1,
									SiPadFrontEndBlock2,
									SiPadFrontEndBlock3,
									SiPadFrontEndBlock4,
									SiPadFrontEndBlock5,
									SiPadFrontEndBlock6,
									SiPadFrontEndBlock7,
									SiPadFrontEndBlock8 ), 
    FE_SelectionType = cms.int32(2), # 0: automatic selection by sensor size; similar to TDR
                                     # 1: automatic selection by SiDie group Index (copyNo); 
                                     #    good for similar sensor sizes, but various FE parameters (blocks). 
                                     # 2: only an unique SiPadFrontEnd configuration for all the sensors,
                                     #    regardless of the sizes or different SiDes. with case 2, only
                                     #    the first element of the SiPadFrontEndParam PSet is used. 
                                     #    case 2 also considers size-dependent parameters such as detector capacitance.
                                     
                                     
	TofCharge_Test = cms.PSet(TofCharge_Test),
	SiHitPulseShapeParam = cms.PSet(SiHitPulseShapeParam)
	
)

