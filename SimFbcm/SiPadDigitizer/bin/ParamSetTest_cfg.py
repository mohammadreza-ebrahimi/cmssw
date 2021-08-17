import FWCore.ParameterSet.Config as cms

process = cms.Process('Test2')

#process.source = cms.Source('EmptySource')

#process.load('SimGeneral.MixingModule.SiPadDigitizer_cfi')
process.load('SimFbcm.SiPadDigitizer.SiPadDigitizer_cfi')
