eval `scramv1 runtime -sh`;
source /cvmfs/cms.cern.ch/common/crab-setup.sh;
for pu in 200 140 100 50 10 0p5 1 1p5
do 
    crab submit -c crabDIGI_cfg.py General.requestName=FBCMDIGIPU$pu
    crab submit -c crabDIGIAging1k_cfg.py General.requestName=FBCMDIGIA1KPU$pu
    crab submit -c crabDIGIAging3k_cfg.py General.requestName=FBCMDIGIA3KPU$pu
    crab submit -c crabDIGIAging4k_cfg.py General.requestName=FBCMDIGIA4KPU$pu
done
