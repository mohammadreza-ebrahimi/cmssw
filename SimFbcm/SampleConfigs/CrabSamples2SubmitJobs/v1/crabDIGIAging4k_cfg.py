from WMCore.Configuration import Configuration
import os,sys
config = Configuration()

reqNamedFromArg = [ arg for arg in sys.argv if arg.startswith( 'General.requestName=' ) ][0].split( '=' )[-1]
puFromArg = reqNamedFromArg[ reqNamedFromArg.find('PU')+2:]
generationInfo = {'0p5':[0.5 , 500 , 500] ,
                  '1' : [1.0 , 500 , 500] ,
                  '1p5' : [1.5 , 500 , 500 ] ,
                  '10' : [10 , 500 , 500 ] ,
                  '50' : [50 , 200 , 200 ] , 
                  '100' : [100 , 500 , 100],
                  '140' : [140 , 600 , 80 ] ,
                  '200' : [200 , 1000 , 50 ] }
config.section_('General')
config.General.requestName = ''
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'GEN_SIM_DIGI_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 3000
config.JobType.sendPythonFolder	 = True
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 5000
config.JobType.maxJobRuntimeMin = 5000
config.JobType.pyCfgParams = ["pu={0}".format(generationInfo[puFromArg][0])  , "aging=4000"]

config.section_('Data')
config.Data.outputPrimaryDataset = 'NuGun'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = generationInfo[puFromArg][2]
config.Data.totalUnits = generationInfo[puFromArg][2] * generationInfo[puFromArg][1]
config.Data.publication = True
config.Data.outputDatasetTag = 'FBCMNuGunAging4000PU{0}'.format(puFromArg)
config.Data.outLFNDirBase = '/store/group/dpg_bril/comm_bril/phase2-sim/FBCMV2/'

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
config.Site.whitelist = ["T2_CH_CERN"]
