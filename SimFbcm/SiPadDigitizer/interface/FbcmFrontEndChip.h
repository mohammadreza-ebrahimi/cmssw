///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------


#ifndef _FbcmFE_FbcmFrontEndChip_h
#define _FbcmFE_FbcmFrontEndChip_h

#include "SimFbcm/SiPadDigitizer/interface/GeneralUtilities.h"
#include "SimFbcm/SiPadDigitizer/interface/FftPreparation.h"
#include "SimFbcm/SiPadDigitizer/interface/Complx.h"
#include "SimFbcm/SiPadDigitizer/interface/FourierTransformableSignal.h"
#include "SimFbcm/SiPadDigitizer/interface/Filter.h"
#include "SimFbcm/SiPadDigitizer/interface/LinearCircuitFreqDomain.h"
#include "SimFbcm/SiPadDigitizer/interface/NonlinearLimiter.h"
#include "SimFbcm/SiPadDigitizer/interface/CFDCore.h"
#include "SimFbcm/SiPadDigitizer/interface/Comparator.h"
#include "SimFbcm/SiPadDigitizer/interface/LogicCircuit.h"
#include "SimFbcm/SiPadDigitizer/interface/HitAnalyzer.h"
//#include "SimFbcm/SiPadDigitizer/interface/HitAnalysisInfo.h"
#include "DataFormats/FbcmDigi/interface/HitAnalysisInfo.h"

#include "SimFbcm/SiPadDigitizer/interface/VmeLogicCircuit.h"

#include <fstream>

namespace FbcmFE {

    class FbcmFrontEndChip  {
    public:
        FbcmFrontEndChip(FftPreparation & FFtPrep); 


        ~FbcmFrontEndChip();
        void printInfo();
        void printInfo_with_AlignedTime();
        void printInfo_with_AlignedTime_BCM1FVME();
        void printInfo_with_AlignedTime_ASIC2022();
        void PrintInputCurrent_uA();
        void Print_TIAOutput_Voltage_mV();
        void Print_ShaperOutput_Voltage_mV();
        void PrintTiaOutput();

        void RunFECircuit( std::pair<float, const edm::ParameterSet * > Area_FeParamPtr );
        void GetHitAnalysisInfo(int BXC_SlotNo, HitAnalysisInfo & HitTotToaInfo);

    private:

		void SetSubmoduleParameters();
        void setBcm1fVME_Parameters();
        void setASIC2022_Parameters();
        void prepareAnalogSampler();
        void prepareInputSignal(SignalType & PulseShape);

        FftPreparation & fftPrep;
		const edm::ParameterSet * ActiveFrontEndParamPtr;
		float SensorArea;
		unsigned int nFFT_;
		SignalType & freqVect_GHz;
		SignalType SiPadReceivedSig_;
		SignalType TIA_OutputSig_;
		SignalType Limiter_OutputSig_;
		SignalType Shaper_OutputSig_;
		SignalType DelayedSig_;
		SignalType DiscrimSig_;
		SignalType DiscrimShaperOutSig_;
		LogicSignalType CFD_ZeroCCompOutSig_;
		LogicSignalType CFD_ArmingCompOutSig_;
		LogicSignalType signalLogicOutput_;
        //----- VME BCM1F ------------
        LogicSignalType vmeCompOutSig_;
        Comparator vmeComp;
        VmeLogicCircuit VMELogicCirc;
        //----- end VME BCM1F ------------
		//----------------- new FBCM FE 2022 ------------
        Filter preAmp_Hf_; 
		Filter boosterAmp_Hf_; 
		Filter shaperFE_Hf_; 
        SignalType preAmpOutputSig_;
        //SignalType preAmpLimittedOutputSig_;
		SignalType boosterOutputSig_;
		SignalType limiterFEv2OutputSig_;
        SignalType sigAnalogSampler_;
        LinearCircuitFreqDomain preAmp_;
        //NonlinearLimiter limiterFEPreAmpv2_;
		LinearCircuitFreqDomain boosterAmp_;
        NonlinearLimiter limiterFEv2_;
		LinearCircuitFreqDomain shaperFEv2_;
        //LogicSignalType asicComparatorOutSig_; // no need. 
        Comparator asicComparator;

        
        //------- end of the new FBCM FE 2022 -----------
        
        Filter TIA_Hf_;
		Filter Shaper_Hf_;
		Filter Delay_Hf_;
		Filter CFD_ShaperHf_;
        
       
		LinearCircuitFreqDomain TIA_;
		NonlinearLimiter Limiter_;
		LinearCircuitFreqDomain Shaper_;
		LinearCircuitFreqDomain DelayCircuit_;
		CFDCore Cfd_;
		LinearCircuitFreqDomain CFD_Shaper_;
		Comparator ZC_Comp;
		Comparator Arming_Comp;
		LogicCircuit OutputLogicCirc;
		HitAnalyzer Hit_Analyzer;
        
        //string testFileDir; 
		
		
};


}
#endif
