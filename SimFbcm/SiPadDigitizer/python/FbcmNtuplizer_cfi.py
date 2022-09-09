import FWCore.ParameterSet.Config as cms

#
# This cfi should be included to build the FBCM geometry model.
#
FbcmNtuple = cms.EDAnalyzer('FbcmNtuplizer_v4',
                                    # FbcmDigiTag = cms.InputTag("simFbcmDigis", instanceName),
                                    # FbcmDigiTag = cms.InputTag("simFbcmDigis", "SiPad"), # study another instance
                                    RHU_InterestedHitBins = cms.vint32(0), # cms.vint32(0,1), first and last elements are included, higly depends on "BinOffset" in SiPadFrontEndParameters_cfi.py
                                    TreeName = cms.string( 'PU{0}'.format(options.pu)),
                                    InstanceNameTags = cms.vstring(
                                                    'WithTimewalkComp',
                                                    'NoTimewalkComp',
                                                    'Vtsh30mV', 
                                                    'Vtsh60mV',
                                                    'Vtsh90mV') # provide a list of valid instanse
                                    )
 