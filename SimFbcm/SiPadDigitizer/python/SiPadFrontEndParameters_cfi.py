import FWCore.ParameterSet.Config as cms


fftSimParam = cms.PSet(
	NumOfFFT_Points = cms.int32(2048), # Length of signal, This should be an integer number with power of 2
	SamplingRepetition = cms.int32(10) # FS: Sampling repetition per ns [1/ns]
)
TofCharge_Test = cms.PSet(
	TofVector =  cms.vdouble(0.0, 25.0), 
	ChargeVect = cms.vdouble(3.*6242, 3.*6242 ), 
    # 1, 1.1, 2, 3, 5, 6, 8 
	TestSensorSize= cms.double(0.0331) # cm2 
    # 0.0225	0.0289	0.0335	0.0385	0.0462	0.0537	0.0658	0.0802	0.1327
)

SiHitPulseShapeParam =cms.PSet(
	HitPulseParam =  cms.vdouble(0.6294422, 99.999855, 40.371655, 1.0, 3.5/2.2) # 0.6294422, 99.999855, 40.371655, 1.0, 3.5/2.2
) 

SiPadFrontEndBlock0 = cms.PSet(
	FrontEndType = cms.int32(1), # 0:CFD_TDR, 1: BCM1F VME, 2: FixedThreshold_only+timewalk compemsation
                           # 3: bcm1f_VME, 4: bcm1f_uTCA, 5: FBCMNewASIC_LE, 6: FBCMNewASIC_CFD 
    GoodForSizeRange = cms.vdouble(0.0,0.0255), # cm2, range from minimum size through maximum size
	BlockIndex = cms.int32(0),
	MaxFEOutputVoltage = cms.double(700.0), # mV
	#LimmiterEdgeCorrFactor = cms.double(1.5), # unitless, by default should be 1.5 
	
	ZCComp_LowerTsh = cms.double(-43.0), # mV, 
	ZCComp_UpperTsh = cms.double(0.0), # mV
	ArmingComp_LowerTsh = cms.double(85.0), # mV , 3*5, 25
	ArmingComp_UpperTsh = cms.double(85.0), # mV, 3*30, 60
	
	TIA_Shaper_Gain = cms.double(10), #120.0 V/V (the amplifier gain after TIA and Shaper1), to keep the linearity at least to 6MIPs
	Tia_Rf = cms.double(47.0), # kOhm
	Tia_Cf = cms.double(0.115), # pF
	Tia_Cin_gs = cms.double(0.5), # pf (just the TIA input Capacitance), the SiPad Capacitance will be added to this
	Tia_Co = cms.double(0.3), # pf
	Tia_gin = cms.double(4.0), # mS
	SensorCouplingCapacitance = cms.double(315.0), # pF
	SensorCapPerCm2 = cms.double(86.207), # pF/cm2
	Shaper1_Tau = cms.double(0.6), # ns
	CFD_Delay  = cms.double(2.0), # ns
	CfdShaper_Gain = cms.double(1.5), # V/V
	CfdShaper_Tau = cms.double(0.25), # ns
	DelayModel = cms.string('FirstOrderPadeDelay'), # 'IdealDelay' or 'FirstOrderPadeDelay'
	CFD_Fraction = cms.double(0.5), # between 0-1, typically around 0.5
	
	lpGBT_AlignerDelay = cms.double(0.0), # ns # it was 5.2ns
	Bx_Duration = cms.double(25.0), # ns
	
    ToAUpperCut = cms.double(30.0), # ns // for BIB study, more than one BX should be investigated
	ToALowerCut = cms.double(-30.0), # ns // for BIB study, more than one BX should be investigated
	#BinLength = cms.double(6.25), # ns, usefull for RHU
    NumOfSubBXbins = cms.int32(4), # RHU num of bins. 
	BinOffset = cms.double(0.0), # ns, plus/minus small time for synchronization to the LHC clk!
    # if the correct RHU is the third one with index of 2 (amonung 0,1,2,3), so it is good to set BinOffset=2*BinLength
   
    ##--------- BMC1F VME param ------------
    VME_CompThreshold = cms.double(25.0), # mV, between 1 mV to 255 mV
    VME_Mode = cms.int32(0), # 0:Updating mode; 1:Non-Updating mode
    VME_pulseWidth = cms.double(5.0), # output pulse width, between 5 ns to 40 ns
    # double-pulse resolution should be fixed  (according to the equip. manual) 
    # for updating (7ns) and non-updating (12ns)
    # but for flexibility, it is set via this interface
    VME_doublePulseResol_Updating = cms.double(7.0), # should be 7 ns
    VME_doublePulseResol_NonUpdating = cms.double(12.0), # should be 12 ns
    ##--------- BMC1F VME param ------------
	
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

#----------------------------

SiPadFrontEndBlock0.BlockIndex = cms.int32(0) 
SiPadFrontEndBlock1.BlockIndex = cms.int32(1) 
SiPadFrontEndBlock2.BlockIndex = cms.int32(2) 
SiPadFrontEndBlock3.BlockIndex = cms.int32(3) 
SiPadFrontEndBlock4.BlockIndex = cms.int32(4) 
SiPadFrontEndBlock5.BlockIndex = cms.int32(5) 
SiPadFrontEndBlock6.BlockIndex = cms.int32(6) 
SiPadFrontEndBlock7.BlockIndex = cms.int32(7) 
SiPadFrontEndBlock8.BlockIndex = cms.int32(8) 

#----------------------------------------------

SiPadFrontEndBlock0.BinOffset = cms.double(-6.0)
SiPadFrontEndBlock1.BinOffset = cms.double(-4.0)
SiPadFrontEndBlock2.BinOffset = cms.double(-2.0) 
SiPadFrontEndBlock3.BinOffset = cms.double(0.0) 
SiPadFrontEndBlock4.BinOffset = cms.double(2.0) 
SiPadFrontEndBlock5.BinOffset = cms.double(4.0) 
SiPadFrontEndBlock6.BinOffset = cms.double(6.0) 
SiPadFrontEndBlock7.BinOffset = cms.double(8.0) 
SiPadFrontEndBlock8.BinOffset = cms.double(10.0)

#-------------------------





# SiPadFrontEndBlock1.CFD_Fraction = cms.double(0.53)  
# #SiPadFrontEndBlock1.lpGBT_AlignerDelay = cms.double(5.4) # ns
# SiPadFrontEndBlock1.ZCComp_LowerTsh = cms.double(-42.0) # mV, threshold
# #

# SiPadFrontEndBlock2.CFD_Fraction = cms.double(0.54)  
# #SiPadFrontEndBlock2.lpGBT_AlignerDelay = cms.double(5.5) # ns
# SiPadFrontEndBlock2.ZCComp_LowerTsh = cms.double(-40.0) # mV
# #

# SiPadFrontEndBlock3.CFD_Fraction = cms.double(0.58)  
# #SiPadFrontEndBlock3.lpGBT_AlignerDelay = cms.double(5.7) # ns
# SiPadFrontEndBlock3.ZCComp_LowerTsh = cms.double(-40.0) # mV
# #

# SiPadFrontEndBlock4.CFD_Fraction = cms.double(0.58)  
# #SiPadFrontEndBlock4.lpGBT_AlignerDelay = cms.double(5.8) # ns
# SiPadFrontEndBlock4.ZCComp_LowerTsh = cms.double(-37.0) # mV
# #

# SiPadFrontEndBlock5.CFD_Fraction = cms.double(0.6)  
# #SiPadFrontEndBlock5.lpGBT_AlignerDelay = cms.double(6.0) # ns
# SiPadFrontEndBlock5.ZCComp_LowerTsh = cms.double(-35.0) # mV
# #

# SiPadFrontEndBlock6.CFD_Fraction = cms.double(0.64)  
# #SiPadFrontEndBlock6.lpGBT_AlignerDelay = cms.double(6.2) # ns
# SiPadFrontEndBlock6.ZCComp_LowerTsh = cms.double(-34.0) # mV
# #

# SiPadFrontEndBlock7.CFD_Fraction = cms.double(0.66)  
# #SiPadFrontEndBlock7.lpGBT_AlignerDelay = cms.double(6.4) # ns
# SiPadFrontEndBlock7.ZCComp_LowerTsh = cms.double(-31.0) # mV
# #

# SiPadFrontEndBlock8.CFD_Fraction = cms.double(0.72)  
# #SiPadFrontEndBlock8.lpGBT_AlignerDelay = cms.double(7.0) # ns
# SiPadFrontEndBlock8.ZCComp_LowerTsh = cms.double(-24.0) # mV

# SiPadFrontEndBlock8.ArmingComp_UpperTsh = cms.double(40.0) # mV

#SiPadFrontEndBlock1.TIA_Shaper_Gain = cms.double(27.5)

