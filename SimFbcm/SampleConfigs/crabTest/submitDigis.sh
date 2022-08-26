eval `scramv1 runtime -sh`;
source /cvmfs/cms.cern.ch/common/crab-setup.sh;
for pu in 200
do 
    crab submit -c crabDIGI_cfg.py General.requestName=FBCMDIGIPU$pu
done
