import FWCore.ParameterSet.Config as cms

# import os
# def getInputFileList(baseDirectory, beginsWithTheseChars ): # without "/" at the end
    # # baseDir = "/".join(baseDirectory.split('/')[:-1]) + "/"
    # baseDir = baseDirectory + "/"
    # storeDir = "/" + "/".join(baseDir.split('/')[3:])
    # subDirs = os.listdir(baseDir)
    # minBiasFiles = []
    # for folder in subDirs:
        # minBiasDirectory = baseDir + folder
        # filesinDirectory = [storeDir + folder + "/" + f for f in os.listdir(minBiasDirectory) if f[:len(beginsWithTheseChars)] == beginsWithTheseChars]
        # minBiasFiles = minBiasFiles + filesinDirectory
    # return minBiasFiles


# baseDirectory ='/eos/cms/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/Aug2022Workshop/NuGun/FbcmMultiInstanceNuGunPU200/220824_150438'
# minBiasFiles = getInputFileList(baseDirectory, "GEN_SIM_DIGI" )
# # minBiasFiles = [minBiasFiles[0]]
# # print(minBiasFiles)
# # exit(0)


process = cms.Process("ntuple")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#process.load('Configuration.Geometry.GeometryExtended2026D80_cff') # FBCM TDR
process.load('Configuration.Geometry.GeometryExtended2026D81_cff') # FBCM 2022
#process.load('Configuration.Geometry.GeometryExtended2021Bcm1fRun3_cff') # BCM1F Run3
#process.load('Configuration.Geometry.GeometryExtended2021Bcm1fMSMR_cff') # BCM1F multiFE_MultiRho
process.load('Geometry.FbcmGeometryBuilder.FbcmGeometry_cfi')

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        # this will be provided by the CRAB, otherwise you should mention it here. 
        # minBiasFiles
        #'file:/eos/cms/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/NuGun/FBCMNuGunPU100/210130_220345/0000/GEN_SIM_DIGI_1.root'
        #'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/GEN_SIM_DIGI.root'
        #'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/new4BCM1F/GEN_SIM_DIGI.root'
        #'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/new4BCM1F/GEN_SIM_DIGI_Run3.root'
        # 'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/Fbcm2022Aug/GEN_SIM_DIGI.root'
        #'file:/eos/home-m/msedghi/NuGun/FBCMNuGunPU200/220823_215040/0000/GEN_SIM_DIGI_1.root'
        # 'file:/afs/cern.ch/work/m/msedghi/CMSSW_11_2_0_pre10/src/SimFbcm/SampleConfigs/crabTest/GEN_SIM_DIGI.root'
    )
)


from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register ('PU',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "puvalue")
options.register ('InstanceName',
                  'SiPadWithTimewalk',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "instanceName")
options.parseArguments()

# print(options.InstanceName)
# print(options.PU)
# exit(0)

process.FbcmNtuple = cms.EDAnalyzer('FbcmNtuplizer_v3',
                                    FbcmDigiTag = cms.InputTag("simFbcmDigis", options.InstanceName),
                                    #FbcmDigiTag = cms.InputTag("simFbcmDigis", "SiPad2"), # study another instance
                                    RHU_InterestedHitBins = cms.vint32(0), # cms.vint32(0,1), first and last elements are included, higly depends on "BinOffset" in SiPadFrontEndParameters_cfi.py
                                    TreeName = cms.string( 'PU{0}'.format(options.PU) )
)

outFName = 'outFbcm2022{0}_pu{1}.root'.format( options.InstanceName , options.PU )
print("output is saved in {0}".format( outFName ) )
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(outFName),
                                   closeFileFast = cms.untracked.bool(True) )
process.options.numberOfThreads=cms.untracked.uint32(1)
process.p = cms.Path(process.FbcmNtuple)
