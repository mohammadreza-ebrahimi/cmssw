import FWCore.ParameterSet.Config as cms


fftSimParam = cms.PSet(
	NumOfFFT_Points = cms.int32(2048), # Length of signal, This should be an integer number with power of 2
	SamplingRepetition = cms.int32(10) # FS: Sampling repetition per ns [1/ns]
)
TofCharge_Test = cms.PSet(
	TofVector =  cms.vdouble(0.0), 
	ChargeVect = cms.vdouble(4.0*6242),
	TestSensorSize= cms.double(0.0289) # cm2 
    # 0.0225	0.0289	0.0335	0.0385	0.0462	0.0537	0.0658	0.0802	0.1327
)

SiHitPulseShapeParam =cms.PSet(
	HitPulseParam =  cms.vdouble(0.6294422, 99.999855, 40.371655, 1.0, 3.5/2.2) # 0.6294422, 99.999855, 40.371655, 1.0, 3.5/2.2
) 

SiPadFrontEndBlock0 = cms.PSet(
	GoodForSizeRange = cms.vdouble(0.0,0.0255), # cm2, range from minimum size through maximum size
	
	MaxFEOutputVoltage = cms.double(700.0), # mV
	#LimmiterEdgeCorrFactor = cms.double(1.5), # unitless, by default should be 1.5 
	
	ZCComp_LowerTsh = cms.double(-43.0), # mV, 
	ZCComp_UpperTsh = cms.double(0.0), # mV
	ArmingComp_LowerTsh = cms.double(25.0), # mV , 3*5
	ArmingComp_UpperTsh = cms.double(60.0), # mV, 3*30
	
	TIA_Shaper_Gain = cms.double(120.0), # V/V (the amplifier gain after TIA and Shaper1), to keep the linearity at least to 6MIPs
	Tia_Rf = cms.double(5.0), # kOhm
	Tia_Cf = cms.double(0.25), # pF
	Tia_Cin_gs = cms.double(0.4), # pf (just the TIA input Capacitance), the SiPad Capacitance will be added to this
	Tia_Co = cms.double(0.4), # pf
	Tia_gin = cms.double(3.0), # mS
	SensorCouplingCapacitance = cms.double(315.0), # pF
	SensorCapPerCm2 = cms.double(86.207), # pF/cm2
	Shaper1_Tau = cms.double(0.9), # ns
	CFD_Delay  = cms.double(2.0), # ns
	CfdShaper_Gain = cms.double(1.5), # V/V
	CfdShaper_Tau = cms.double(0.25), # ns
	DelayModel = cms.string('FirstOrderPadeDelay'), # 'IdealDelay' or 'FirstOrderPadeDelay'
	CFD_Fraction = cms.double(0.5), # between 0-1, typically around 0.5
	
	lpGBT_AlignerDelay = cms.double(5.2), # ns
	Bx_Duration = cms.double(25.0), # ns
	
    ToAUpperCut = cms.double(30.0), # ns // for BIB study, more than one BX should be investigated
	ToALowerCut = cms.double(-30.0), # ns // for BIB study, more than one BX should be investigated
	BinLength = cms.double(6.26), # ns
	BinOffset = cms.double(0.0), # ns
	
)

SiPadFrontEndBlock1 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock2 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock3 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock4 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock5 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock6 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock7 = SiPadFrontEndBlock0.clone();
SiPadFrontEndBlock8 = SiPadFrontEndBlock0.clone();

#----------------------------

SiPadFrontEndBlock0.GoodForSizeRange = cms.vdouble(0.0   , 0.0257) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock1.GoodForSizeRange = cms.vdouble(0.0257, 0.0312) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock2.GoodForSizeRange = cms.vdouble(0.0312, 0.036) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock3.GoodForSizeRange = cms.vdouble(0.036 , 0.0423) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock4.GoodForSizeRange = cms.vdouble(0.0423 , 0.05) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock5.GoodForSizeRange = cms.vdouble(0.05, 0.0598) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock6.GoodForSizeRange = cms.vdouble(0.0598, 0.073) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock7.GoodForSizeRange = cms.vdouble(0.073 , 0.1065) # cm2, range from minimum size through maximum size
SiPadFrontEndBlock8.GoodForSizeRange = cms.vdouble(0.1065 , 100.0) # cm2, range from minimum size through maximum size
#-------------------------


SiPadFrontEndBlock1.CFD_Fraction = cms.double(0.53)  
SiPadFrontEndBlock1.lpGBT_AlignerDelay = cms.double(5.4) # ns
SiPadFrontEndBlock1.ZCComp_LowerTsh = cms.double(-42.0) # mV, threshold
#

SiPadFrontEndBlock2.CFD_Fraction = cms.double(0.54)  
SiPadFrontEndBlock2.lpGBT_AlignerDelay = cms.double(5.5) # ns
SiPadFrontEndBlock2.ZCComp_LowerTsh = cms.double(-40.0) # mV
#

SiPadFrontEndBlock3.CFD_Fraction = cms.double(0.58)  
SiPadFrontEndBlock3.lpGBT_AlignerDelay = cms.double(5.7) # ns
SiPadFrontEndBlock3.ZCComp_LowerTsh = cms.double(-40.0) # mV
#

SiPadFrontEndBlock4.CFD_Fraction = cms.double(0.58)  
SiPadFrontEndBlock4.lpGBT_AlignerDelay = cms.double(5.8) # ns
SiPadFrontEndBlock4.ZCComp_LowerTsh = cms.double(-37.0) # mV
#

SiPadFrontEndBlock5.CFD_Fraction = cms.double(0.6)  
SiPadFrontEndBlock5.lpGBT_AlignerDelay = cms.double(6.0) # ns
SiPadFrontEndBlock5.ZCComp_LowerTsh = cms.double(-35.0) # mV
#

SiPadFrontEndBlock6.CFD_Fraction = cms.double(0.64)  
SiPadFrontEndBlock6.lpGBT_AlignerDelay = cms.double(6.2) # ns
SiPadFrontEndBlock6.ZCComp_LowerTsh = cms.double(-34.0) # mV
#

SiPadFrontEndBlock7.CFD_Fraction = cms.double(0.66)  
SiPadFrontEndBlock7.lpGBT_AlignerDelay = cms.double(6.4) # ns
SiPadFrontEndBlock7.ZCComp_LowerTsh = cms.double(-31.0) # mV
#

SiPadFrontEndBlock8.CFD_Fraction = cms.double(0.72)  
SiPadFrontEndBlock8.lpGBT_AlignerDelay = cms.double(7.0) # ns
SiPadFrontEndBlock8.ZCComp_LowerTsh = cms.double(-24.0) # mV

SiPadFrontEndBlock8.ArmingComp_UpperTsh = cms.double(40.0) # mV


