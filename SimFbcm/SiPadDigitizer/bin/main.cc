///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------

#include <iostream>
#include <cstdlib>

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
int main(int argc, char* argv[])
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
    double TestSensorSize;
    std::vector< TofChargePair > Tof_Q_pairTest;
    // assumptions: 1st arg is sensor size in cm2
    //              2nd arg is tof in ns
    //              3rd arg is charge in electrons
    // std::cout << "Have " << argc << " arguments:" << std::endl;
    // double testVal;
    // for (int i = 0; i < argc; ++i) {
        // std::cout << argv[i] << " ";
        
        // std::cout << testVal << "\n";
    // }
    if (argc==4)
    {
        TestSensorSize = std::atof(argv[1]); 
        Tof_Q_pairTest.emplace_back(std::make_pair(std::atof(argv[2]), std::atof(argv[3])));
        std::cout << "sensor Area: " << TestSensorSize << ", tof: " << Tof_Q_pairTest.front().first 
                  << ", charge: " << Tof_Q_pairTest.front().second << "\n";
    }
    else
    {
        const edm::ParameterSet& TofCharge_Test = SiPadDigitizerParam.getParameter<edm::ParameterSet>("TofCharge_Test");
        std::vector<double> TofVectTest(TofCharge_Test.getParameter< std::vector<double> >("TofVector"));
        std::vector<double> ChargeVectTest(TofCharge_Test.getParameter< std::vector<double> >("ChargeVect"));
        if (TofVectTest.size() != ChargeVectTest.size())
            throw cms::Exception("Tof-Charge size mismatch")
              << "The size of TofVectTest and ChargeVectTest in the TofCharge_Test should be the same\n";
        
        
        for (unsigned int j=0 ; j < TofVectTest.size() ; j++) {
            Tof_Q_pairTest.emplace_back(std::make_pair(TofVectTest[j], ChargeVectTest[j]));
        }
        TestSensorSize = TofCharge_Test.getParameter< double >("TestSensorSize");
    }
	///-------------------------------------------------------------------------------------------
	
	HitPulse.GetPulseSeriesShape(FftPrep, Tof_Q_pairTest); // vector for charge amplitude
	std::pair<float, const edm::ParameterSet * > Area_FeParamPtr = FeParamSelector.SelectFrontEndConfig(TestSensorSize);
	FrontEnd.RunFECircuit(Area_FeParamPtr);

    HitAnalysisInfo HitTotToaInfo;
    FrontEnd.GetHitAnalysisInfo(0, HitTotToaInfo);
    //std:: cout << HitTotToaInfo ;

	//FrontEnd.printInfo();
	FrontEnd.printInfo_with_AlignedTime();
    FrontEnd.printInfo_with_AlignedTime_BCM1FVME();
    FrontEnd.printInfo_with_AlignedTime_ASIC2022();

	return 0;
}

