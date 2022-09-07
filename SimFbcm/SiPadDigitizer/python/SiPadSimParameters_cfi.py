import FWCore.ParameterSet.Config as cms

SiPadSimBlock = cms.PSet(
	
	ReadoutNoiseInElec = cms.double(700.0), #readout noise, including all readout chain 
	GaussianTailNoise = cms.double(0.0),    # for GaussianTailNoiseGenerator, not impelemented YET
	HitSelectionMode = cms.int32(1), # 1 or 0 # 1 means select all hits, 0 means filter hits according to the TofUpperCut and TofLowerCut
    TofUpperCut = cms.double(12.5), #  between 60 ns and -60 ns, the Tof for the positin of FBCM is ~9.4ns for the BxSlotNo=0
    TofLowerCut = cms.double(-12.5), 
    FirstBxSlotNo = cms.int32(-2), # by default BxSlotNo Zero is the first one for each Event
    LastBxSlotNo = cms.int32(2), # this means the last BxSlotNo to study hitAnalsis and Store HitAnalysisInfo in the vector
	# PseudoRadDamage = cms.untracked.double(210.25), # in cm2 , as an example 14.5x14.5
	# PseudoRadDamageRadius = cms.untracked.double(22.0), # cm, as an example maximum radius of sensors
	chargeCollectionEfficiency = cms.double(0.89744),
	#FluctuateCharge = cms.untracked.bool(True), # Fluctuate charge in track subsegments, by default should be True. 
	DeltaProductionCut = cms.double(0.03),   # it was 0.03 delta cutoff in MeV, has to be same as in OSCAR(0.030/cmsim=1.0 MeV)  // tMax(0.030) In MeV.
	AddNoise = cms.bool(True),
	Alpha2Order = cms.bool(True),			# second order effect, does not switch off magnetic field as described
    SigmaZero = cms.double(0.00037),  		# 0.00037 : 3.7um spread for 300um-thick sensor, renormalized in digitizerAlgo
    SigmaCoeff = cms.double(1.8),  		    # 1.8 to be confirmed with simulations in CMSSW_6.X
    ClusterWidth = cms.double(3),		    # 3  this is used as number of sigmas for charge collection (3=+-3sigmas)
    TanLorentzAnglePerTesla_Fbcm = cms.double(0.07), 
    # TanLorentzAnglePerTesla: 0.07 is for the Tracker-endcap (Pixel and Strip in PS and 2S) 
    # TanLorentzAnglePerTesla: 0.106 is for the inner Tracker Pixel 
	    
) 


# Threshold in electrons are the Official CRAFT09 numbers:
# FPix(smearing)/BPix(smearing) = 2480(160)/2730(200)

