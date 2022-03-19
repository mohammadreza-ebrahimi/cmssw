///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------

#include <iostream>

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSetReader/interface/ParameterSetReader.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "SimFbcm/SiPadDigitizer/interface/GeneralUtilities.h"
#include "SimFbcm/SiPadDigitizer/interface/FftPreparation.h"
#include "SimFbcm/SiPadDigitizer/interface/FbcmFrontEndChip.h"
#include "SimFbcm/SiPadDigitizer/interface/SiHitPulseShape.h"
//#include "SimFbcm/SiPadDigitizer/interface/HitAnalysisInfo.h"
#include "DataFormats/FbcmDigi/interface/HitAnalysisInfo.h"
#include "SimFbcm/SiPadDigitizer/interface/FeConfigSelector.h"

//#include "GeneralUtilities.h"
//#include "FftPreparation.h"
//#include "FbcmFrontEndChip.h"
//#include "SiHitPulseShape.h"
//#include "HitAnalysisInfo.h"
//#include "FeConfigSelector.h"

using namespace FbcmFE;
using namespace std;
int main()
{
  std::string fileName("ParamSetTest_cfg.py");
    std::shared_ptr<edm::ParameterSet> iConfig = edm::readConfig(fileName);
  //std::cout << iConfig->dump() << std::endl;
  const edm::ParameterSet& SiPadDigitizerParam = iConfig->getParameter<edm::ParameterSet>("SiPadDigitizer");
  
  //-------------------------------------------------------------
  const edm::ParameterSet& FFT_SimParam = SiPadDigitizerParam.getParameter<edm::ParameterSet>("FFT_SimParam");
  const edm::ParameterSet& SiHitPulseShapeParam = SiPadDigitizerParam.getParameter<edm::ParameterSet>("SiHitPulseShapeParam");
  const std::vector< edm::ParameterSet > & SiPadFrontEndParamVect = SiPadDigitizerParam.getParameter< std::vector< edm::ParameterSet > >("SiPadFrontEndParam");
    
 
    FftPreparation FftPrep(FFT_SimParam); 
	SiHitPulseShape HitPulse( SiHitPulseShapeParam.getParameter< std::vector<double> >("HitPulseParam") );
    FbcmFrontEndChip FrontEnd(FftPrep); // the FrontEnd parameters will be set just before running for each sensor size
	FeConfigSelector FeParamSelector(SiPadFrontEndParamVect);


	///-------------------------------------------------------------------------------------------
	const edm::ParameterSet& TofCharge_Test = SiPadDigitizerParam.getParameter<edm::ParameterSet>("TofCharge_Test");
	std::vector<double> TofVectTest(TofCharge_Test.getParameter< std::vector<double> >("TofVector"));
	std::vector<double> ChargeVectTest(TofCharge_Test.getParameter< std::vector<double> >("ChargeVect"));
	if (TofVectTest.size() != ChargeVectTest.size())
		throw cms::Exception("Tof-Charge size mismatch")
          << "The size of TofVectTest and ChargeVectTest in the TofCharge_Test should be the same\n";
	
	std::vector< TofChargePair > Tof_Q_pairTest;
	for (unsigned int j=0 ; j < TofVectTest.size() ; j++) {
		Tof_Q_pairTest.emplace_back(std::make_pair(TofVectTest[j], ChargeVectTest[j]));
	}
	double TestSensorSize = TofCharge_Test.getParameter< double >("TestSensorSize");
	///-------------------------------------------------------------------------------------------
	
	HitPulse.GetPulseSeriesShape(FftPrep, Tof_Q_pairTest); // vector for charge amplitude
	std::pair<float, const edm::ParameterSet * > Area_FeParamPtr = FeParamSelector.SelectFrontEndConfig(TestSensorSize);
	FrontEnd.RunFECircuit(Area_FeParamPtr);

    HitAnalysisInfo HitTotToaInfo;
    FrontEnd.GetHitAnalysisInfo(0, HitTotToaInfo);
    //std:: cout << HitTotToaInfo ;

	//FrontEnd.printInfo();
	//FrontEnd.printInfo_with_AlignedTime();
    FrontEnd.printInfo_with_AlignedTime_BCM1FVME();

	return 0;
}

