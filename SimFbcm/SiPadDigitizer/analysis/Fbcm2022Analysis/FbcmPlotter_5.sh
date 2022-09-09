#! /bin/bash 

echo "$(dirname "$0")";
cd "$(dirname "$0")";


export SCRAM_ARCH=slc7_amd64_gcc820;
eval `scramv1 runtime -sh`;

./FbcmPlotterV3_5.py $@;
