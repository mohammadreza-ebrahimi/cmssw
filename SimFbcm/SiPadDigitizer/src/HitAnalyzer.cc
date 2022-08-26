///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------

#include "SimFbcm/SiPadDigitizer/interface/HitAnalyzer.h"

namespace FbcmFE {
    HitAnalyzer::HitAnalyzer(FftPreparation & FFtPrep,LogicSignalType & CFD_LogicalSignal, const SignalType & Signal2PeakAmplSampler):
    FFtPrep_(FFtPrep),
    CFD_LogicalSignal_(CFD_LogicalSignal),
    Signal2PeakAmplSampler_(Signal2PeakAmplSampler),
    BX_Duration_(25.0),
    FS_(FFtPrep_.SamplingRepetition()),
    BxHitStatus(HitStatus::Zero),
    NumOfRecognizedHits(0),
    isTimewalkEnabled_(0)
	{
		timeVectAligned_=FFtPrep_.TimeVectZeroCenter()-AlignerDelay_;
		};

	HitAnalyzer::~HitAnalyzer(){};

    void HitAnalyzer::RunHitAnalyzer(int BXC_SlotNo){

        TotToaVect.clear();
		const float Eps=0.000;
		
        float HalfBxLen=BX_Duration_/2.0;
        int Len=timeVectAligned_.size();
        BXC_SlotNo_=BXC_SlotNo;
        unsigned int AlignerDelayIndexShift=(unsigned int)(AlignerDelay_ * FS_);
        unsigned int ZeroTimeIndex=Len/2 + AlignerDelayIndexShift;
        unsigned int BX_IndShift=(unsigned int)(BX_Duration_ * FS_);
        int BX_CenterIndex=ZeroTimeIndex + BX_IndShift * BXC_SlotNo_ ;
		
        int lowerTimeIndexCut=BX_CenterIndex + (int)(ToALowerCut_*FS_) ; // BX_CenterIndex-BX_IndShift/2;
        int UpperTimeIndexCut=BX_CenterIndex + (int)(ToAUpperCut_*FS_) ; // BX_CenterIndex+BX_IndShift/2;
        
        if (lowerTimeIndexCut<=0)
             lowerTimeIndexCut=1;
            
         if (UpperTimeIndexCut>=Len)
             UpperTimeIndexCut=Len-1;
        
        bool HitDetected=false;
        unsigned int start_ = 0, end_;
        int BckwardCNT,i;
        float ToA,ToT;
        ToaTotPair TotToa;
        ToAStatus ToAState=ToAStatus::UnKnown;
        float ToTCorrectionCount = 0;

        float binshift=BinShift_-Eps;
        int16_t SubBxBinNo;
        bool LastState=CFD_LogicalSignal_ [lowerTimeIndexCut-1];
        for (i=lowerTimeIndexCut; ((i <= UpperTimeIndexCut) || HitDetected==true ) && (i < Len) ; i++)
        { 

            if ( i==lowerTimeIndexCut && CFD_LogicalSignal_[lowerTimeIndexCut]) {
                for (BckwardCNT=lowerTimeIndexCut+1; (CFD_LogicalSignal_ [BckwardCNT]) && BckwardCNT > 0  ; BckwardCNT--) ;

                // if (BckwardCNT==0 && CFD_LogicalSignal_ [Len-1])
                // {
                    // for (ToTCorrectionCount=0 ; !CFD_LogicalSignal_[ToTCorrectionCount]; ToTCorrectionCount++ );
                    // for (jj=Len-1 ; (CFD_LogicalSignal_ [jj]) && jj > 0 ; jj--);
                    // std::cout <<"first and end continued., New ToAInd is:" << jj << "\n"; 
                    // start_= jj;
                    
                // } else
                // {
                    // start_=BckwardCNT;
                // }
                
                start_=BckwardCNT;
                
                HitDetected=true;
            }
            else if (CFD_LogicalSignal_[i] != LastState)  // rising-edge or falling-edge occurred
            {
                if (CFD_LogicalSignal_[i]) /// rising-edge
                {
                    start_=i;
                    HitDetected=true;
                }
                else if (HitDetected) /// falling-edge & ValidPulse
                {
                    end_=i;
                    HitDetected=false;
                    ToA=timeVectAligned_[start_]-(BXC_SlotNo_*BX_Duration_);
                    ToT=timeVectAligned_[end_]-timeVectAligned_[start_];
                    
                    // -- update ToA with timewalk, if needed ------------
                   //std::cout << "toa: " << ToA << ", ToT: " << ToT << "\n";
                    if(isTimewalkEnabled_)
                        updateToAwithTimewalkTable(ToT, &ToA);
                   
                  //std::cout << "after update: toa: " << ToA << ", ToT: " << ToT << "\n";                   
                    //----------------------------------------------------
                    
                    SubBxBinNo= (int16_t)(round((ToA-binshift)/BinLen_));
                    
                    
                    
                    ToAState=GetToAStatus(ToA,ToT,HalfBxLen);
                    
                    pAmpl = Signal2PeakAmplSampler_[start_];
                    for (unsigned int k=start_ ; k < end_ ; k++ )
                        if (Signal2PeakAmplSampler_[k] > pAmpl) 
                            pAmpl=Signal2PeakAmplSampler_[k]; 
                        

                    TotToa.SetPairInfo(ToA,ToT, true, ToAState ,SubBxBinNo, pAmpl );
                    TotToaVect.emplace_back(TotToa);

//                    std::cout << "A hit detected, ToA: " << TotToa.ToA() << ", "
//                            << "ToT: " << TotToa.ToT() << "\n\n";

                }

            }
            LastState=CFD_LogicalSignal_[i];

        }

        if (HitDetected) // if HitDetected is still true, this means that a too long hit observed reaching to the end of time span. this is not a valid hit.
        {

                    HitDetected = false;
                    ToA=timeVectAligned_[start_]-(BXC_SlotNo_*BX_Duration_);
                    end_=i-1;
                    
                    // due to cyclic FFT!, the signal will return back and starts from begining. 
                    for (ToTCorrectionCount=0 ; CFD_LogicalSignal_ [ToTCorrectionCount] ;  ToTCorrectionCount++);
                    ToTCorrectionCount--;
                    
                    ToT=timeVectAligned_[end_]-timeVectAligned_[start_] +  ToTCorrectionCount/FS_ ;
                    //ToT=1000.0;


                    // -- update ToA with timewalk, if needed -----------
                    // however, for invalid ToT, no need to updated ToA
                     if(isTimewalkEnabled_)
                        updateToAwithTimewalkTable(ToT, &ToA);
                    
                    //----------------------------------------------------
                    
                    SubBxBinNo= (int16_t)(round((ToA-binshift)/BinLen_));
                    ToAState=GetToAStatus(ToA,ToT,HalfBxLen);

                    pAmpl = Signal2PeakAmplSampler_[start_];
                    for (unsigned int k=start_ ; k < end_ ; k++ )
                        if (Signal2PeakAmplSampler_[k] > pAmpl) 
                            pAmpl=Signal2PeakAmplSampler_[k]; 

                    //TotToa.SetPairInfo(ToA,ToT,false, ToAState , SubBxBinNo, pAmpl );
                    
                    TotToa.SetPairInfo(ToA,ToT,true, ToAState , SubBxBinNo, pAmpl );
                    TotToaVect.emplace_back(TotToa);
        }
            NumOfRecognizedHits=CheckHitInBx();
    }

    unsigned int HitAnalyzer::CheckHitInBx(){
        NumOfRecognizedHits=0;
        //float HalfBx=-BX_Duration_/2.0;
         BxHitStatus=HitStatus::Zero;
           for (ToaTotPair v:TotToaVect)
             {
                 if (v.ToAToAStatus()==ToAStatus::FullyWithinBx || v.ToAToAStatus()==ToAStatus::WithinBx_LastsAfter ){
                        NumOfRecognizedHits++;
                        if (BxHitStatus==HitStatus::Zero)
                            BxHitStatus=HitStatus::NonZero;
                     }
                else if (v.ToAToAStatus()==ToAStatus::BeforeBx_Overlapping )
                        BxHitStatus=HitStatus::Uncertain;
             }

        return NumOfRecognizedHits;

    }



    HitAnalysisInfo HitAnalyzer::GetHitAnalysisInfo(){
    HitAnalysisInfo tmp(BXC_SlotNo_,
                        TotToaVect,
                        AlignerDelay_,
                        BxHitStatus,
                        NumOfRecognizedHits );
    return tmp;
    }


    ToAStatus HitAnalyzer::GetToAStatus(float ToA, float ToT, float HalfBxLen){
        ToAStatus Status=ToAStatus::UnKnown;
        float Ending=ToA+ToT;
        if (ToA > HalfBxLen)
            Status=ToAStatus::AfterBx;
        else if ( (ToA >= -HalfBxLen) && (Ending > HalfBxLen) )
            Status=ToAStatus::WithinBx_LastsAfter;
        else if ( (ToA >= -HalfBxLen) && (Ending <= HalfBxLen) )
            Status=ToAStatus::FullyWithinBx;
        else if ( (ToA < -HalfBxLen) && (Ending > -HalfBxLen) )
            Status=ToAStatus::BeforeBx_Overlapping;
        else //if ( (ToA < -HalfBxLen) && (Ending < -HalfBxLen) )
            Status=ToAStatus::BeforeBx_NonOverlapping;

        return Status;

    }
	
	
	void HitAnalyzer::SetParameters( const edm::ParameterSet * FEParamPtr ){
		
		
		BX_Duration_ = FEParamPtr->getParameter< double >("Bx_Duration");
		AlignerDelay_ = FEParamPtr->getParameter< double >("lpGBT_AlignerDelay");
		ToAUpperCut_  = FEParamPtr->getParameter< double >("ToAUpperCut");
        ToALowerCut_  = FEParamPtr->getParameter< double >("ToALowerCut");
        
        nSubBins_  = FEParamPtr->getParameter< int >("NumOfSubBXbins");
		BinShift_ = FEParamPtr->getParameter< double >("BinOffset");
		
		timeVectAligned_=FFtPrep_.TimeVectZeroCenter()-AlignerDelay_;
		
        //BinLen_  = FEParamPtr->getParameter< double >("BinLength");
        BinLen_ = BX_Duration_ / nSubBins_;
        
        isTimewalkEnabled_ = FEParamPtr->getParameter< bool >("ApplyTimewalk");
        if(isTimewalkEnabled_)
        {
        edm::ParameterSet TimeWalktablePSet = FEParamPtr->getParameter< edm::ParameterSet >("TimewalkTable"); 
        
        ToTentryVect_ = TimeWalktablePSet.getParameter< std::vector<double> >("ToTentry"); 
        timewalkDelayVect_ = TimeWalktablePSet.getParameter< std::vector<double> >("timewalkDelay"); 
        timewalkTable_.clear(); 
        if (ToTentryVect_.size() == timewalkDelayVect_.size()) 
            for (unsigned int j=0 ; j < ToTentryVect_.size() ; j++ ){ 
                timewalkTable_.emplace_back( std::make_pair(ToTentryVect_[j], timewalkDelayVect_[j]) );            
                }
        else
             throw cms::Exception("error SiPadFrontEndParameters.py") << "The lenght of ToTentry and timewalkDelay should be the same"; 
         
         //for (auto v:timewalkTable_)
             //std::cout << v.first << " " << v.second << "\n";
        }
        
		// std::cout << "BX_Duration_: " << BX_Duration_ << "\n"
					// << "AlignerDelay_: " << AlignerDelay_ << "\n"
					// << "ToAUpperCut_: " << ToAUpperCut_ << "\n"
					// << "ToALowerCut_: " << ToALowerCut_ << "\n"
					// << "BinLen_: " << BinLen_ << "\n"
					// << "BinShift_: " << BinShift_ << "\n" ;
					
	}
    
    float HitAnalyzer::updateToAwithTimewalkTable(float ToT, float *ToA){
        
        float ToaDelay=0;
        if (ToT < timewalkTable_.front().first )
            ToaDelay = timewalkTable_.front().second;
        else if (ToT >= timewalkTable_.back().first)
            ToaDelay = timewalkTable_.back().second;
        else
        {
            for (unsigned int j=0 ; j < timewalkTable_.size()-1 ; j++ ){ 
                //std::cout << v.first << " " << v.second << "\n";
                if (ToT >= timewalkTable_[j].first && ToT < timewalkTable_[j+1].first )
                    ToaDelay = timewalkTable_[j].second;                
            }
        }
        *ToA = *ToA - ToaDelay;
        
        return *ToA;
    }

}


