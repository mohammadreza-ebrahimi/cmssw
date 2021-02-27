import FWCore.ParameterSet.Config as cms

# def getSiPadDigitizer(process):
    # if hasattr(process,'mix') and hasattr(process.mix,'digitizers') and hasattr(process.mix.digitizers,'SiPad'):
        # return process.mix.digitizers.SiPad
    # return None
def no_aging(process):
	return process

def _1000invfb(process):
	#SiPadDigi=getSiPadDigitizer(process)
	if hasattr(process.mix.digitizers,'SiPad'):
		process.mix.digitizers.SiPad.SiPadSimParam.ReadoutNoiseInElec = cms.double(808.0)
		process.mix.digitizers.SiPad.SiPadSimParam.chargeCollectionEfficiency = cms.double(0.517)
		for SiPadFE in process.mix.digitizers.SiPad.SiPadFrontEndParam :
			SiPadFE.SensorCapPerCm2  = cms.double(95.26)
			SiPadFE.SensorCouplingCapacitance = cms.double(313.85)
	return process
	
def _3000invfb(process):
	#SiPadDigi=getSiPadDigitizer(process)
	if hasattr(process.mix.digitizers,'SiPad'):
		process.mix.digitizers.SiPad.SiPadSimParam.ReadoutNoiseInElec = cms.double(1409.0)
		process.mix.digitizers.SiPad.SiPadSimParam.chargeCollectionEfficiency = cms.double(0.3792)
		for SiPadFE in process.mix.digitizers.SiPad.SiPadFrontEndParam :
			SiPadFE.SensorCapPerCm2  = cms.double(124.23)
			SiPadFE.SensorCouplingCapacitance = cms.double(311.55)
	return process

def _4000invfb(process):
	#SiPadDigi=getSiPadDigitizer(process)
	if hasattr(process.mix.digitizers,'SiPad'):
		process.mix.digitizers.SiPad.SiPadSimParam.ReadoutNoiseInElec = cms.double(1628.0)
		process.mix.digitizers.SiPad.SiPadSimParam.chargeCollectionEfficiency = cms.double(0.3497)
		for SiPadFE in process.mix.digitizers.SiPad.SiPadFrontEndParam :
			SiPadFE.SensorCapPerCm2  = cms.double(136.42)
			SiPadFE.SensorCouplingCapacitance = cms.double(310.4)
	return process
