///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------

#ifndef _FbcmFE_VME_LogicCircuit_h
#define _FbcmFE__VME_LogicCircuit_h

#include "SimFbcm/SiPadDigitizer/interface/GeneralUtilities.h"

namespace FbcmFE {

	class VmeLogicCircuit {

    enum LogicLevel
	{
		LOW,
		HIGH,
		UNKNOWN
	};


	public:
		VmeLogicCircuit(LogicSignalType & InputSig, LogicSignalType & OutputSignal);
		~VmeLogicCircuit();
		void RunLogic();
        void SetParameters( const edm::ParameterSet * FEParamPtr , unsigned int FS );

	private:
		LogicSignalType & InputSig_;
		LogicSignalType & OutputSignal_;
        unsigned int FS_;
        int outMode_; // 0: updatingMode, 1:NonUpdatgingMode
        double pulseWidth_; // ns
        double doubleHitResoluoiton_; // 7ns or 12ns based on updatingMode or NonUpdatgingMode. 
	};

}
#endif
