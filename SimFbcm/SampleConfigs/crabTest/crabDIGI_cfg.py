from WMCore.Configuration import Configuration
import os,sys
config = Configuration()

reqNamedFromArg = [ arg for arg in sys.argv if arg.startswith( 'General.requestName=' ) ][0].split( '=' )[-1]
puFromArg = reqNamedFromArg[ reqNamedFromArg.find('PU')+2:]
generationInfo = {'0p5':[0.5 , 2 , 500] ,
                  '1' : [1.0 , 2 , 500] ,
                  '1p5' : [1.5 , 1 , 1 ] ,
                  '10' : [10 , 1 , 1 ] ,
                  '50' : [50 , 1 , 1 ] , 
                  '100' : [100 , 1 , 1],
                  '140' : [140 , 1 , 1 ] ,
                  '200' : [200 , 100 , 25 ] }
config.section_('General')
config.General.requestName = ''
config.General.workArea = 'crab_multiInstance'
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'GEN_SIM_DIGI_M_cfg.py'
config.JobType.allowUndistributedCMSSW = True
# config.JobType.maxJobRuntimeMin = 3000
config.JobType.sendPythonFolder	 = True
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 4000
config.JobType.maxJobRuntimeMin = 1000
config.JobType.pyCfgParams = ["pu={0}".format(generationInfo[puFromArg][0])  , "aging=0"]

config.section_('Data') 
config.Data.outputPrimaryDataset = 'NuGun'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = generationInfo[puFromArg][2]
config.Data.totalUnits = generationInfo[puFromArg][2] * generationInfo[puFromArg][1]
config.Data.publication = False
config.Data.outputDatasetTag = 'FbcmMultiInstanceNuGunPU{0}'.format(puFromArg)11
# config.Data.outLFNDirBase = '/store/user/msedghi/multi-Instance/'
# config.Data.outLFNDirBase = '/store/group/dpg_bril/comm_bril/vtest/'
config.Data.outLFNDirBase = '/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/Aug2022Workshop/'


config.section_("Site")
# config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.storageSite = "T2_CH_CERN"
config.Site.whitelist = ["T2_CH_CERN"]
# "T3_CH_CERNBOX"
