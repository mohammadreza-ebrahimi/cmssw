///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------


#include "SimFbcm/SiPadDigitizer/interface/VmeLogicCircuit.h"

namespace FbcmFE {

	VmeLogicCircuit::VmeLogicCircuit(LogicSignalType & InputSig, LogicSignalType & OutputSignal):
		InputSig_(InputSig),
		OutputSignal_(OutputSignal),
        outMode_(0),
        pulseWidth_(5.0),
        doubleHitResoluoiton_(7.0)
		{ 		};

	VmeLogicCircuit::~VmeLogicCircuit(){};

    void VmeLogicCircuit::RunLogic(){
        
    bool lastInputSig=LogicLevel::HIGH;
    bool InSig;
    bool out=LogicLevel::LOW;
    int pluseLen=0;
    int dblPlsResul=0;
    //std::cout <<"size is " << InternalUpdatingOutSig_.size() << "\n";
    for (unsigned int i=0; i < InputSig_.size() ; i++) {
        InSig=InputSig_[i];
            if (InSig!=lastInputSig && InSig==LogicLevel::HIGH && dblPlsResul<=0)
            {
                dblPlsResul=(int)(doubleHitResoluoiton_*FS_);
                
                if (outMode_==1 && pluseLen<=0) //NonUpdatgingMode
                  pluseLen=(int)(pulseWidth_*FS_); 
                else if (outMode_==0) // Updating mode
                  pluseLen=(int)(pulseWidth_*FS_);
            }
            
            if (pluseLen>0)
            {
                out=LogicLevel::HIGH;
                pluseLen--;
            }
            else
                out=LogicLevel::LOW;
            
            if (dblPlsResul>0)
                dblPlsResul--;
            
            lastInputSig=InSig;
            OutputSignal_[i]=out;

    }
    
    
    }
    
    
    void VmeLogicCircuit::SetParameters( const edm::ParameterSet * FEParamPtr , unsigned int FS){
		
        FS_=FS;
        
        //std::cout << "FS is VME is " << FS_ << "\n";
        
		outMode_ = FEParamPtr->getParameter< int >("VME_Mode");
		pulseWidth_ = FEParamPtr->getParameter< double >("VME_pulseWidth");
        
        switch (outMode_){
            case 0: // 0: Updating mode // // should be 7 ns
            doubleHitResoluoiton_= FEParamPtr->getParameter< double >("VME_doublePulseResol_Updating");
            break;
            case 1: // 1: Non-Updating mode // should be 12 ns
            doubleHitResoluoiton_= FEParamPtr->getParameter< double >("VME_doublePulseResol_NonUpdating");
            break;
            
            default:
            throw cms::Exception("Wrong VME Mode") << "only 0 or 1, i.e., 0: Updating mode; 1: Non-Updating mode\n";
            break; 
            
        }

	}
    
}


