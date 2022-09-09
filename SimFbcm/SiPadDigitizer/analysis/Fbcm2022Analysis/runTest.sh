#!/bin/bash
eval `scramv1 runtime -sh`;
SrcDIR=$CMSSW_BASE/src
insName=SiPad
cd $SrcDIR/SimFbcm/SampleConfigs/Fbcm2022Aug
cmsRun GEN_SIM_DIGI_cfg.py 
echo "step 1 done: (GEN-SIM-DIGI)"
cd $SrcDIR/SimFbcm/SiPadDigitizer/test/Fbcm2022Analysis
# cmsRun Fbcm2022_Ntuplizer_cfg.py InstanceName=$insName
# echo "step 2 done: (Ntuplizer)"

#./FbcmPlotterV2.py -i outFbcm2022_$insName\_pu1.root
echo "step 3 done: (Plotter)"
#./ExtractPlots_v8.py -i ./output/results/outPlotterMerged_$insName\_pu1.root -p 1
echo "step 4 done: (extact plots)"
echo "finished"
