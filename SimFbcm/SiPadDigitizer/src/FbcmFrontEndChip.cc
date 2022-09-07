///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------

#include "SimFbcm/SiPadDigitizer/interface/FbcmFrontEndChip.h"


namespace FbcmFE {

FbcmFrontEndChip::FbcmFrontEndChip(FftPreparation & FFtPrep):
        fftPrep(FFtPrep),
		nFFT_(fftPrep.nbrFFTpoints()),
        freqVect_GHz(FFtPrep.FreqVectGHz()),
		SiPadReceivedSig_(nFFT_),
		TIA_OutputSig_(nFFT_),
		Limiter_OutputSig_(nFFT_),
		Shaper_OutputSig_(nFFT_),
		DelayedSig_(nFFT_),
        DiscrimSig_(nFFT_),
        DiscrimShaperOutSig_(nFFT_),
        CFD_ZeroCCompOutSig_(nFFT_),
		CFD_ArmingCompOutSig_(nFFT_),
		signalLogicOutput_(nFFT_),
        //----- VME BCM1F ------------
        vmeCompOutSig_(nFFT_),
        vmeComp(Shaper_OutputSig_,vmeCompOutSig_),
        VMELogicCirc(vmeCompOutSig_,signalLogicOutput_),
        //----- end of VME BCM1F ------------
        
        //----------------- new FBCM FE 2022 ------------
        preAmp_Hf_(freqVect_GHz),
        boosterAmp_Hf_(freqVect_GHz),
        shaperFE_Hf_(freqVect_GHz),
        preAmpOutputSig_(nFFT_),
        //preAmpLimittedOutputSig_(nFFT_),
        boosterOutputSig_(nFFT_),
        limiterFEv2OutputSig_(nFFT_),
        sigAnalogSampler_(nFFT_),
        preAmp_(SiPadReceivedSig_,preAmpOutputSig_, preAmp_Hf_),
        //limiterFEPreAmpv2_(preAmpOutputSig_,preAmpLimittedOutputSig_),
        boosterAmp_(preAmpOutputSig_,boosterOutputSig_, boosterAmp_Hf_),
        limiterFEv2_(boosterOutputSig_,limiterFEv2OutputSig_),
        shaperFEv2_(limiterFEv2OutputSig_, Shaper_OutputSig_, shaperFE_Hf_ ),
        //asicComparatorOutSig_(nFFT_),
        asicComparator(Shaper_OutputSig_,signalLogicOutput_),

                
        //------- end of the new FBCM FE 2022 -----------
        
		TIA_Hf_(freqVect_GHz),
		Shaper_Hf_(freqVect_GHz),
		Delay_Hf_(freqVect_GHz), // IdealDelay or FirstOrderPadeDelay
		CFD_ShaperHf_(freqVect_GHz),
		TIA_(SiPadReceivedSig_,TIA_OutputSig_,TIA_Hf_),
		Limiter_(TIA_OutputSig_,Limiter_OutputSig_),
		Shaper_(Limiter_OutputSig_,Shaper_OutputSig_,Shaper_Hf_),
		DelayCircuit_(Shaper_OutputSig_,DelayedSig_,Delay_Hf_),
		Cfd_(Shaper_OutputSig_,DelayedSig_,DiscrimSig_),
		CFD_Shaper_(DiscrimSig_,DiscrimShaperOutSig_,CFD_ShaperHf_),
		ZC_Comp(DiscrimShaperOutSig_,CFD_ZeroCCompOutSig_),
		Arming_Comp(Shaper_OutputSig_,CFD_ArmingCompOutSig_),
		OutputLogicCirc(CFD_ZeroCCompOutSig_,CFD_ArmingCompOutSig_,signalLogicOutput_),
		Hit_Analyzer(FFtPrep, signalLogicOutput_, sigAnalogSampler_)
    {

} ;
	FbcmFrontEndChip::~FbcmFrontEndChip(){};

	void FbcmFrontEndChip::printInfo(){
      std::ofstream myfile;
      myfile.open ("Result.txt");

        for (unsigned int i=0; i < nFFT_; i++ )
            myfile << SiPadReceivedSig_[i] << "\t"
                    << TIA_OutputSig_[i] << "\t"
                    << Shaper_OutputSig_[i] << "\t"
                    << DelayedSig_[i] << "\t"
                    << DiscrimShaperOutSig_[i] << "\t"
                    << CFD_ZeroCCompOutSig_[i] << "\t"
                    << CFD_ArmingCompOutSig_[i] << "\t"
                    << signalLogicOutput_[i] << "\n";

        myfile.close();
        std::cout << "done! \n";
	}


	void FbcmFrontEndChip::printInfo_with_AlignedTime_BCM1FVME(){
       SignalType & timeVectAligned_=Hit_Analyzer.GetAlignedTimeVect();
        std::ofstream myfile;
      myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/Result_BCM1FVME.txt");

        for (unsigned int i=0; i < nFFT_; i++ )
            myfile << timeVectAligned_[i] << "\t"
                    << SiPadReceivedSig_[i] << "\t"
                    << TIA_OutputSig_[i] << "\t"
                    << Shaper_OutputSig_[i] << "\t"
                    << vmeCompOutSig_[i] << "\t"
                    << signalLogicOutput_[i] << "\n";

        myfile.close();
        std::cout << "BCMF VME done! \n";
	}




	void FbcmFrontEndChip::printInfo_with_AlignedTime(){
       SignalType & timeVectAligned_=Hit_Analyzer.GetAlignedTimeVect();
        std::ofstream myfile;
      myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/Result.txt");

        for (unsigned int i=0; i < nFFT_; i++ )
            myfile << timeVectAligned_[i] << "\t"
                    << SiPadReceivedSig_[i] << "\t"
                    << TIA_OutputSig_[i] << "\t"
                    << Shaper_OutputSig_[i] << "\t"
                    << DelayedSig_[i] << "\t"
                    << DiscrimShaperOutSig_[i] << "\t"
                    << CFD_ZeroCCompOutSig_[i] << "\t"
                    << CFD_ArmingCompOutSig_[i] << "\t"
                    << signalLogicOutput_[i] << "\n";

        myfile.close();
        std::cout << "done! \n";
	}
    
    void FbcmFrontEndChip::printInfo_with_AlignedTime_ASIC2022(){
       SignalType & timeVectAligned_=Hit_Analyzer.GetAlignedTimeVect();
        std::ofstream myfile;
      myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/ResultASIC2022.txt");

        for (unsigned int i=0; i < nFFT_; i++ )
            myfile << timeVectAligned_[i] << "\t"
                    << SiPadReceivedSig_[i] << "\t"
                    << preAmpOutputSig_[i] << "\t"
                   // << preAmpLimittedOutputSig_[i] << "\t"
                    << boosterOutputSig_[i] << "\t"
                    << Shaper_OutputSig_[i] << "\t"
                    << signalLogicOutput_[i] << "\n"; 
                    
                    
        myfile.close();
        std::cout << "New ASIC done! \n";
	}


    void FbcmFrontEndChip::Print_ShaperOutput_Voltage_mV(){
		for (auto i:Shaper_OutputSig_)
			 std::cout << i << "\n";
    }

    void FbcmFrontEndChip::Print_TIAOutput_Voltage_mV(){
		for (auto i:TIA_OutputSig_)
			 std::cout << i << "\n";
    }

	void FbcmFrontEndChip::PrintInputCurrent_uA(){
		for (auto i:SiPadReceivedSig_)
			 std::cout << i << "\n";
    }



	void FbcmFrontEndChip::prepareInputSignal(SignalType & PulseShape){
	    double Dimention=e_q/_ns/_uA; // the current will be in micro Ampere (uA)
		for (unsigned int i=0; i< nFFT_ ; i++ )
			SiPadReceivedSig_[i]=PulseShape[i]*Dimention; // uA
	}

	void FbcmFrontEndChip::PrintTiaOutput(){

	    double max_=0.0;
	    for (uint16_t i=0 ; i< nFFT_ ; i++ )
            if (Shaper_OutputSig_[i] > max_)
                max_=Shaper_OutputSig_[i];
        std::cout << max_ << "\n";


	}

	void FbcmFrontEndChip::SetSubmoduleParameters() {
		
	TIA_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Shaper_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Delay_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	CFD_ShaperHf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Limiter_.SetAbsMaxOut(ActiveFrontEndParamPtr->getParameter< double >("MaxFEOutputVoltage"));
	Cfd_.SetFraction(ActiveFrontEndParamPtr->getParameter< double >("CFD_Fraction"));
	//ZC_Comp.SetComparatorThresholds(-5.0,0.0);
	ZC_Comp.SetComparatorThresholds(ActiveFrontEndParamPtr->getParameter< double >("ZCComp_LowerTsh"),
									ActiveFrontEndParamPtr->getParameter< double >("ZCComp_UpperTsh"));
	
	//Arming_Comp.SetComparatorThresholds(5.0,20.0);
	Arming_Comp.SetComparatorThresholds(ActiveFrontEndParamPtr->getParameter< double >("ArmingComp_LowerTsh"),
										ActiveFrontEndParamPtr->getParameter< double >("ArmingComp_UpperTsh"));

	Hit_Analyzer.SetParameters( ActiveFrontEndParamPtr ) ;
	
	}
    
    
    void FbcmFrontEndChip::setBcm1fVME_Parameters() {
		
	TIA_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Shaper_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Delay_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	CFD_ShaperHf_.SetParameters( ActiveFrontEndParamPtr ) ;
	Limiter_.SetAbsMaxOut(ActiveFrontEndParamPtr->getParameter< double >("MaxFEOutputVoltage"));
	
    vmeComp.SetComparatorThresholds(ActiveFrontEndParamPtr->getParameter< double >("VME_CompThreshold"),
									ActiveFrontEndParamPtr->getParameter< double >("VME_CompThreshold"));
	VMELogicCirc.SetParameters( ActiveFrontEndParamPtr , fftPrep.SamplingRepetition()) ;
	Hit_Analyzer.SetParameters( ActiveFrontEndParamPtr ) ;
	
	}

    void FbcmFrontEndChip::setASIC2022_Parameters() {

    edm::ParameterSet ASICParamPset; 
    ASICParamPset = ActiveFrontEndParamPtr->getParameter< edm::ParameterSet >("FE2022ASIC");
		
	preAmp_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
	boosterAmp_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
    shaperFE_Hf_.SetParameters( ActiveFrontEndParamPtr ) ;
    //limiterFEPreAmpv2_.SetAbsMaxOut(ActiveFrontEndParamPtr->getParameter< double >("MaxFEOutputVoltage"));
	limiterFEv2_.SetAbsMaxOut(ActiveFrontEndParamPtr->getParameter< double >("MaxFEOutputVoltage"));
	
    asicComparator.SetComparatorThresholds(ASICParamPset.getParameter< double >("ComparatorThreshold"),
									       ASICParamPset.getParameter< double >("ComparatorThreshold"));
                                           
	Hit_Analyzer.SetParameters( ActiveFrontEndParamPtr ) ;
	
	}

	void FbcmFrontEndChip::RunFECircuit(std::pair<float, const edm::ParameterSet * > Area_FeParamPtr){
		
		SensorArea =  Area_FeParamPtr.first;
		ActiveFrontEndParamPtr=Area_FeParamPtr.second;
        
        std::string DelayModel(ActiveFrontEndParamPtr->getParameter< std::string >("DelayModel"));
        //std::string DelayModel = ActiveFrontEndParamPtr->getParameter< std::string >("DelayModel");
        
        FilterType DelayType;
        if (DelayModel == "FirstOrderPadeDelay")
            DelayType=FilterType::FirstOrderPadeDelay;
        else if ( DelayModel == "IdealDelay")
            DelayType=FilterType::IdealDelay;
        else
            throw cms::Exception("Wrong Delay type")
                << "the delay type in CFD should be either IdealDelay or FirstOrderPadeDelay\n";
        
        
        int FrontEndType_ = ActiveFrontEndParamPtr->getParameter< int >("FrontEndType"); 
        
       
        switch( FrontEndType_ )
        {
            case 0: // FBCM CFD_TDR 
            //std::cout << "FrontEndType_" << FrontEndType_ << "\n";
            TIA_Hf_.SetSensorArea( SensorArea ); 
            SetSubmoduleParameters();
            prepareInputSignal(fftPrep.TimeDomainSignal());
            TIA_Hf_.RunFilter(FilterType::TIA_Filter);
            TIA_.CalculateOutputSignal();
            Limiter_.RunLimiter();
            Shaper_Hf_.RunFilter(FilterType::Shaper_Filter);
            Shaper_.CalculateOutputSignal();
            Delay_Hf_.RunFilter(DelayType);
            DelayCircuit_.CalculateOutputSignal();
            Cfd_.RunCFD();
            CFD_ShaperHf_.RunFilter(FilterType::CDFShaper);
            CFD_Shaper_.CalculateOutputSignal();
            
            sigAnalogSampler_ = Shaper_OutputSig_; 
            
            ZC_Comp.RunComparator();
            Arming_Comp.RunComparator();
            OutputLogicCirc.RunLogic();
            
            break;
            
            case 1: // BCM1F VME
                //std::cout << "FrontEndType_" << FrontEndType_ << "\n";
                TIA_Hf_.SetSensorArea( SensorArea ); 
                setBcm1fVME_Parameters(); // should be updated
                prepareInputSignal(fftPrep.TimeDomainSignal());
                TIA_Hf_.RunFilter(FilterType::TIA_Filter);
                TIA_.CalculateOutputSignal();
                Limiter_.RunLimiter();
                Shaper_Hf_.RunFilter(FilterType::Shaper_Filter);
                Shaper_.CalculateOutputSignal();
                
                sigAnalogSampler_ = Shaper_OutputSig_; 
                
                vmeComp.RunComparator();
                VMELogicCirc.RunLogic();
            break;
            
            case 2: // FBCM_newFE_2022 (EDR)
                //std::cout << "This is New ASIC: FrontEndType_" << FrontEndType_ << "\n";
                preAmp_Hf_.SetSensorArea( SensorArea ); 
                setASIC2022_Parameters(); // should be updated
                prepareInputSignal(fftPrep.TimeDomainSignal()); // it preprares SiPadReceivedSig_
                preAmp_Hf_.RunFilter(FilterType::preAmp_Filter);
                preAmp_.CalculateOutputSignal();
                
                //limiterFEPreAmpv2_.RunLimiter();
                
                boosterAmp_Hf_.RunFilter(FilterType::booster_Filter);
                boosterAmp_.CalculateOutputSignal();
                limiterFEv2_.RunLimiter();
                shaperFE_Hf_.RunFilter(FilterType::shaperFEv2_Filter);
                shaperFEv2_.CalculateOutputSignal();
                asicComparator.RunComparator();
                prepareAnalogSampler();
                
                
            break;
            
            
            default:
              throw cms::Exception("Wrong FrontEnd Type") << " FrontEndType in SiPadFrontEndBlockX is invalid\n";
              break;
        }


	            
	
	}

	void FbcmFrontEndChip::GetHitAnalysisInfo(int BXC_SlotNo, HitAnalysisInfo & HitTotToaInfo){
	    Hit_Analyzer.RunHitAnalyzer(BXC_SlotNo);
	    HitTotToaInfo = Hit_Analyzer.GetHitAnalysisInfo();
    }
    
    void FbcmFrontEndChip::prepareAnalogSampler(){
        int signalCode_ = ActiveFrontEndParamPtr->getParameter< int >("signalCodeForPeakAmpl");
        //std::cout << signalCode_ << "\n";
        switch(signalCode_){ 
            case 0:                 
                sigAnalogSampler_ = SiPadReceivedSig_;
            break;
            
            case 1:                 
                sigAnalogSampler_ = (-1.0) * preAmpOutputSig_;  // to make it positive
            break;
            
            case 2:                 
                sigAnalogSampler_ = boosterOutputSig_;
            break;
            
            case 3:                 
                sigAnalogSampler_ = limiterFEv2OutputSig_;
            break;
            
            case 4:                 
                sigAnalogSampler_ = Shaper_OutputSig_; 
            break;  
            
           default:
              throw cms::Exception("Wrong signal sample name") << "pls use ";
              break; 
        }
        
    }


}


