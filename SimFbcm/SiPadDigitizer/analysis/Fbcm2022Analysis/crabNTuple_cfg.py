from WMCore.Configuration import Configuration
import os,sys
config = Configuration()


reqNamedFromArg = [ arg for arg in sys.argv if arg.startswith( 'General.requestName=' ) ][0].split( '=' )[-1]
puFromArg = reqNamedFromArg[ reqNamedFromArg.find('PU')+2:]

scanName = [ arg for arg in sys.argv if arg.startswith( 'General.InstanceName=' ) ][0].split( '=' )[-1]

# since in one of the DIGI outputs, they have not been pulished as a dadatbase, I should do with some modification.. 
generationInfo = {'0p5':[0.5 , 'address to the DIGI directory'] ,
                  '1' : [1.0 , 'address to the DIGI directory'] ,
                  '1p5' : [1.5 , 'address to the DIGI directory'] ,
                  '10' : [10 , 'address to the DIGI directory' ] ,
                  '50' : [50 , 'address to the DIGI directory' ] , 
                  '100' : [100 , 'address to the DIGI directory'],
                  '140' : [140 , 'address to the DIGI directory' ] ,
                  '200' : [200 , '/eos/cms/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/Aug2022Workshop/NuGun/FbcmMultiInstanceNuGunPU200/220824_150438'] }

def getInputFileList(baseDirectory, beginsWithTheseChars ): # without "/" at the end
    # baseDir = "/".join(baseDirectory.split('/')[:-1]) + "/"
    baseDir = baseDirectory + "/"
    storeDir = "/" + "/".join(baseDir.split('/')[3:])
    subDirs = os.listdir(baseDir)
    minBiasFiles = []
    for folder in subDirs:
        minBiasDirectory = baseDir + folder
        filesinDirectory = [storeDir + folder + "/" + f for f in os.listdir(minBiasDirectory) if f[:len(beginsWithTheseChars)] == beginsWithTheseChars]
        minBiasFiles = minBiasFiles + filesinDirectory
    return minBiasFiles


# baseDirectory ='/eos/cms/store/group/dpg_bril/comm_bril/phase2-sim/FBCM/Aug2022Workshop/NuGun/FbcmMultiInstanceNuGunPU200/220824_150438'
baseDirectory = generationInfo[puFromArg][1]
inputDigiFiles = getInputFileList(baseDirectory, "GEN_SIM_DIGI" )
# inputDigiFiles = [inputDigiFiles[0]]
# print(inputDigiFiles)
# exit(0)



config.section_('General')
config.General.requestName = ''
config.General.workArea = "crabNtuples_{0}".format(scanName)
config.General.transferOutputs = True

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'Fbcm2022_Ntuplizer_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.sendPythonFolder	 = True
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 1000
config.JobType.maxJobRuntimeMin = 100
config.JobType.pyCfgParams = ["PU={0}".format(puFromArg), "InstanceName={0}".format(scanName)]

config.section_('Data')
# config.Data.inputDataset = generationInfo[puFromArg][1]
config.Data.userInputFiles = inputDigiFiles
config.Data.splitting = 'FileBased'
# config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 5
config.Data.outputPrimaryDataset = "nTuple{}".format(scanName)
config.Data.outputDatasetTag = 'FbcmNtuplePU{0}'.format(puFromArg)

config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/msedghi/Fbcm/Aug2022Workshop/nTuples/'
# config.Data.inputDBS = 'phys03'

config.section_("Site")
# config.Site.storageSite = "T2_CH_CERN"
config.Site.storageSite = "T3_CH_CERNBOX"
config.Site.whitelist = ["T2_CH_CERN"]
