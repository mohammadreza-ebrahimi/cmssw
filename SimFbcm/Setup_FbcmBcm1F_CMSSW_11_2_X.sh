#!/bin/bash
SrcDIR=$CMSSW_BASE/src
cd $SrcDIR
git cms-init
git remote add fbcm-cmssw https://github.com/m-sedghi/cmssw.git
git pull my-cmssw CMSSW_11_2_FbcmBcm1f

git cms-addpkg DataFormats/DetId
git cms-addpkg DataFormats/FbcmDetId
git cms-addpkg DataFormats/GeometrySurface
git cms-addpkg Geometry/CommonTopologies
git cms-addpkg Geometry/CommonDetUnit
git cms-addpkg Geometry/FbcmGeometry
git cms-addpkg Geometry/Records
git cms-addpkg Geometry/FbcmGeometryBuilder
git cms-addpkg SimG4Core
git cms-addpkg SimG4CMS
git cms-addpkg DataFormats/FbcmDigi
git cms-addpkg SimFbcm
git cms-addpkg SimGeneral/MixingModule
git cms-addpkg Geometry/TrackerCommonData
git cms-addpkg Geometry/CMSCommonData
git cms-addpkg Geometry/ForwardCommonData
git cms-addpkg Configuration/Geometry
git cms-addpkg Configuration/Eras
git cms-addpkg Configuration/EventContent
git cms-addpkg Configuration/StandardSequences
git cms-addpkg Geometry/FbcmCommonData
git cms-addpkg Geometry/FbcmSimData
git cms-addpkg SimGeneral/Configuration
git cms-addpkg GeneratorInterface/BeamHaloGenerator

cd $SrcDIR/GeneratorInterface/BeamHaloGenerator && scram b -j 24
cd $SrcDIR/DataFormats && scram b -j 24
cd $SrcDIR/Geometry && scram b -j 24
cd $SrcDIR/SimG4Core && scram b -j 24
cd $SrcDIR/SimG4CMS && scram b -j 24
cd $SrcDIR/SimFbcm && scram b -j 24
cd $SrcDIR/SimGeneral && scram b -j 24
cd $SrcDIR/Configuration && scram b -j 24
cd $SrcDIR

echo "done!"

