eval `scramv1 runtime -sh`;
source /cvmfs/cms.cern.ch/common/crab-setup.sh;
for pu in 200
do 
    for scanName in SiPadWithTimewalk SiPadNoTimewalk SiPad25mVtsh SiPad100mVtsh SiPadRfa38k154
    do
        crab submit -c crabNTuple_cfg.py General.requestName=FBCMnTuplePU$pu General.InstanceName=$scanName
    done    
done

