import FWCore.ParameterSet.Config as cms

process = cms.Process("ntuple")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#process.load('Configuration.Geometry.GeometryExtended2026D80_cff') # FBCM
process.load('Configuration.Geometry.GeometryExtended2021Bcm1fRun3_cff') # BCM1F Run3
#process.load('Configuration.Geometry.GeometryExtended2021Bcm1fMSMR_cff') # BCM1F multiFE_MultiRho
process.load('Geometry.FbcmGeometryBuilder.FbcmGeometry_cfi')

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:/eos/cms/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/NuGun/FBCMNuGunPU100/210130_220345/0000/GEN_SIM_DIGI_1.root'
        #'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/GEN_SIM_DIGI.root'
        #'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/new4BCM1F/GEN_SIM_DIGI.root'
        'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/new4BCM1F/GEN_SIM_DIGI_Run3.root'
    )
)


from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register ('PU',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "puvalue")
options.parseArguments()

process.FbcmNtuple = cms.EDAnalyzer('FbcmNtuplizer_v3',
                                    FbcmDigiTag = cms.InputTag("simFbcmDigis", "SiPad"),
                                    #FbcmDigiTag = cms.InputTag("simFbcmDigis", "SiPad2"), # study another instance
                                    RHU_InterestedHitBins = cms.vint32(0), # cms.vint32(0,1), first and last elements are included, higly depends on "BinOffset" in SiPadFrontEndParameters_cfi.py
                                    TreeName = cms.string( 'PU{0}'.format(options.PU) )
)

outFName = 'outBcm1FRun3_pu{0}.root'.format( options.PU )
print("output is saved in {0}".format( outFName ) )
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(outFName),
                                   closeFileFast = cms.untracked.bool(True) )

process.p = cms.Path(process.FbcmNtuple)
