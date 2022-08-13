///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------


#ifndef _FbcmFE_Filter_h
#define _FbcmFE_Filter_h


#include <string>
#include <vector>
#include <cmath>
#include <iostream>
#include "SimFbcm/SiPadDigitizer/interface/Complx.h"
#include <fstream>


namespace FbcmFE {

	const static double PI=3.14159265359;
	enum FilterType
	{
		TIA_Filter,
		Shaper_Filter,
		TIA_Shaper_Filter,
		IdealDelay,
		FirstOrderPadeDelay,
		CDFShaper,
        preAmp_Filter,
        booster_Filter,
        shaperFEv2_Filter,
		NotSet
	};

	class Filter {
	public:
		Filter(SignalType & FreqGHz);
		~Filter();
		ComplexSignalType &  GetTransferFunction() {return Filter_Tf;}
		void RunFilter(FilterType type_);
		void SetParameters( const edm::ParameterSet * FEParamPtr );
		void SetSensorArea( float Area ){ SensorArea = Area; }

	private:
		void RunTIAFilter();
		void RunShaperFilter();
		void RunIdealDelayFilter();
		void Run1stPadeDelayFilter();
		void RunCDFShaper();
        
        void RunPreAmpFilter_old();
        void RunPreAmpFilter();
		void RunBoosterFilter();
		void RunBoosterShaperFilter();
        
        FilterType Type_;
		ComplexSignalType Filter_Tf;
		SignalType & freq_GHz_ ;
		const edm::ParameterSet * FrontEndParamPtr; 
		
		double TIA_ShaperGain;
		double rf; // kOhm
		double cf; // pF
        double cgs; // pF
        double cc; // pF // coupling capacitance
		double C_per_cm2; // pF/cm2
		float SensorArea;
		double co; // pF
		double gin; // mS
		double Tau_sh; // ns //Shaper1 Tau
		double CDF_Delay; // ns
		double CFD_Gain; // gain [V/V]
		double Tau_CFDsh; // ns
        
        ///---------------
        double R12, C2, R1, R0, Cf0, Cf1, R5, G0, C1, E0, G1;
        double R8, R9, R10, R11, C7, C8, C9, R6, C10, C0, G2,
               R2, C4, G3, R3, C3, C5, G4, R4, C6, E5, R7, C11, R13 ;

        
        
        
		
	};

}
#endif

