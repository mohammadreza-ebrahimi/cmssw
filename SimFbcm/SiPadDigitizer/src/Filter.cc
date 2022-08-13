///--------------------------------------------------------------------
//  A set of classes for simulating the hit response of FBCM Front-end
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: November 2020
///--------------------------------------------------------------------


#include "SimFbcm/SiPadDigitizer/interface/Filter.h"

namespace FbcmFE {

	Filter::Filter(SignalType & freqGHz):Type_(FilterType::NotSet),freq_GHz_(freqGHz){
		SensorArea = 0.0;
	};

	Filter::~Filter(){};

	void Filter::RunFilter(FilterType type_){
		Type_=type_;
		switch (Type_){
		case FbcmFE::TIA_Filter:
			RunTIAFilter();
			break;
		case FbcmFE::Shaper_Filter:
			RunShaperFilter();
			break;
        case FbcmFE::IdealDelay:
            RunIdealDelayFilter();
			break;
		case FbcmFE::FirstOrderPadeDelay:
            Run1stPadeDelayFilter();
			break;
        case FbcmFE::CDFShaper:
            RunCDFShaper();
			break;
            
        case FbcmFE::preAmp_Filter:
            RunPreAmpFilter(); // this is OK
            //RunPreAmpFilter_old();
		break;
        case FbcmFE::booster_Filter:
            RunBoosterFilter();
		break;
        case FbcmFE::shaperFEv2_Filter:
            RunBoosterShaperFilter();
		break;
        
		default:
		throw cms::Exception("Wrong FilterType")
          << "FilterType is wrong or has not been set.\n";
			break;
		}
	}

//----------------------------
	void Filter::RunPreAmpFilter_old(){
		Complx HfVal_preAmp;
		Complx d1,d2, d3, d4;
        Complx tmp1,tmp2,tmp3;
        Complx W0, W1, W2, W3, W4, W5, W6;
        Complx X0, X1, X6, X4, X5;
        Complx ZinA, Zd, Zc, inputZCoef, ZinB, ZLA;
		double omega; // rad per ns = f_Ghz*2*Pi
		double cd = SensorArea*C_per_cm2;
		        
        //std::cout <<"Area: " << SensorArea << "cd : " << cd << "cc : " << cc << "]n" ;
        
        
        //std::ofstream myfile;
        //myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/FileterTest.txt");

        
        
        
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
            W0=  tmp1.Set(1,omega*R1*C3) * tmp2.Set(1,omega*R0*(C2+Cf0)) * tmp3.Set(R12+R5,omega*Cf1*R12*R5) * R12; 
            W1=  tmp1 * tmp3 ; 
            W2= ( tmp1.Set(0, omega*Cf1*R12) * tmp2.Set(1, omega*R0*(C2+Cf0)) ) + tmp3.Set(0, omega*R0*(C2+Cf0)) ;
            W3 = tmp1.Set(0,-omega*R12*Cf0*R0) * tmp2.Set(-G0, omega*Cf0) 
                 + tmp1.Set(0,omega*R12*(C1+Cf0)) * tmp2.Set(1, omega*R0*(C2+Cf0)) + tmp3.Set(1,0);
            W4=tmp1.Set(1,omega*Cf1*R12);
            W5=tmp1.Set(0, omega*Cf1*R12*R5)* tmp2.Set(1,omega*C3*R1)*tmp3.Set(1, omega*R0*(C2+Cf0));
            W6= tmp1.Set(-G0, omega*Cf0) * (-E0*G1*R0*R1*R12) + tmp2.Set(1,omega*R1*C3)*tmp3.Set(1,omega*R0*(C2+Cf0))* R5;
            ZinA = W0 / (W1*(W2+W3)-W4*(W5+W6));
            Zd.Set(0, omega*cd);
            Zd.Reciprocal();
            Zc.Set(0, omega*cc);
            Zc.Reciprocal();
            //= (tmp1.Set(0, omega*cd)).Reciprocal();
            //Zc= (tmp1.Set(0, omega*cc)).Reciprocal();
            inputZCoef=(ZinA*Zd)/(Zd+Zc+ZinA);
            
            X0 = tmp1.Set(1,omega*C4*R2) * tmp2.Set(1, omega*C5*R3) * tmp3.Set(1, omega*R4*(C11+C6)) * (R13*(R13+R7));
            X1 = tmp1.Set(0,-omega*E5*R13*R4*C11) * tmp2.Set(1, omega*C4*R2) * tmp3.Set(1,omega*C5*R3) + tmp3.Set(E5*R13*R4*G2*G3*G4*R2*R3,0);
            X6 = tmp1.Set(1,omega*C4*R2)*tmp2.Set(1,omega*C5*R3)*tmp3.Set(1,omega*R4*(C11+C6))*(R13);
            X4 = tmp1.Set(0,-omega*(R13+R7)*R13*R4*C11)*(tmp2.Set(0,omega*C11)*tmp3.Set(1,omega*C4*R2)*tmp2.Set(1,omega*C5*R3)-tmp1.Set(-G2*G3*G4*R2*R3,0));
            X5 = tmp1.Set(0,omega*(R13+R7)*R13*(C0+C11)) * tmp2.Set(1,omega*C4*R2) * tmp3.Set(1, omega*C5*R3) * tmp1.Set(1, omega*R4*(C11+C6));
            ZinB=(X0)/(X1+X6+X4+X5);
            
            
            ZLA = ZinB + tmp1.Set(R6, 0);
            //ZLA = tmp1.Set(R6, 0);
            //ZLA.Reciprocal();
            d1 = tmp2.Set(-G0,omega*Cf0) * (-E0*G1);
            d2 = tmp1.Set(1/R1,omega*C3) * ( tmp2.Set(1/R0, omega*(C2+Cf0)) * R5 ); 
            tmp3= d1/d2;
            d3 = tmp1.Set(0, omega*Cf1) + tmp3 + tmp2.Set(1/R12,0);
            d4 = tmp1.Set(1/R5+1/R12, omega*Cf1) + ZLA.Reciprocal();
            //d4 = tmp1.Set(1/R5+1/R12, omega*Cf1);
            //HfVal_preAmp = ZinA * (d3 / d4);
            tmp2.Set(d3 / d4);
            HfVal_preAmp = tmp1.Set(-1, 0) * ZinA;
            //std::cout << inputZCoef ;
            //HfVal_preAmp.Set(1,0);     
            
            //myfile << f_ghz << '\t' << HfVal_preAmp.mag() << "\n";
            
			Filter_Tf.emplace_back(HfVal_preAmp);
		}
        
        //myfile.close();
		
	}


//----------------------------
	void Filter::RunPreAmpFilter(){
		Complx HfVal_preAmp;
		Complx d1,d2, d3, d4;
        Complx tmp1,tmp2,tmp3;
        Complx W0, W1, W2, W3, W4, W5, W6;
        Complx X0, X1, X6, X4, X5;
        Complx T0, T1, T2, T3, T4, T5, T6, T7, T8, T9, T10;
        Complx ZinA, Zd, Zc, inputCoef, ZinB, ZLA;
		double omega; // rad per ns = f_Ghz*2*Pi
		double cd = SensorArea*C_per_cm2;
        double cSourceNorton=(cc*cd/(cd+cc)); // pF
		double i_norton_factor=1.0/(1.0+(cd/cc));
		        
        //std::cout <<"Area: " << SensorArea << "cd : " << cd << "cc : " << cc << "]n" ;
        
        
        //std::ofstream myfile;
        //myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/FileterTest.txt");

        C1= C1 + cSourceNorton;
        
        
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
            
                        
            T0=tmp1.Set(0, omega*R12*Cf1*R12*R5)*tmp1.Set(1, omega*C3*R1)*tmp1.Set(1, omega*R0*(C2+Cf0));
            T1=tmp1.Set(-G0,omega*Cf0) * (-R12*E0*G1*R0*R1*R12) ;
            T2= tmp1.Set(1,omega*C3*R1)*tmp1.Set(1,omega*R0*(C2+Cf0)) * (R12*R5);
            T3=tmp1.Set(1,omega*C3*R1)*tmp1.Set(R5+R12,omega*R5*R12*Cf1);
            T4=tmp1.Set(0,omega*Cf1*R12)*tmp1.Set(1,omega*R0*(C2+Cf0))+ tmp1.Set(0,omega*R0*(C2+Cf0));
            T5=tmp1.Set(0,-omega*R12*Cf0*R0) * tmp1.Set(-G0,omega*Cf0);
            T6= tmp1.Set(0,omega*R12*(C1+Cf0)) * tmp1.Set(1,omega*R0*(C2+Cf0)) + tmp1.Set(1,0); 
            T7=tmp1.Set(1,omega*Cf1*R12);
            T8=tmp1.Set(0,omega*Cf1*R12*R5)* tmp1.Set(1,omega*C3*R1) * tmp1.Set(1,omega*R0*(C2+Cf0));
            T9=tmp1.Set(-G0,omega*Cf0) * (-E0*G1*R0*R1*R12); 
            T10=tmp1.Set(1,omega*C3*R1)*tmp1.Set(1,omega*R0*(C2+Cf0))* R5;
            //HfVal_preAmp =(T3*(T4+T5+T6)-T7*(T8+T9+T10)) ;
            //HfVal_preAmp.Reciprocal();
            //HfVal_preAmp=  (T0+T1+T2) * HfVal_preAmp ;
            HfVal_preAmp = ((T0+T1+T2) * i_norton_factor) / (T3*(T4+T5+T6)-T7*(T8+T9+T10));
            
            //HfVal_preAmp = tmp1.Set(-1, 0) * ZinA;
            //HfVal_preAmp.conjugate();
            //HfVal_preAmp = HfVal_preAmp * tmp1.Set(-1,0);
            //myfile << f_ghz << '\t' << inputCoef.mag() << "\n";
            
			Filter_Tf.emplace_back(HfVal_preAmp);
		}
        
        //myfile.close();
		
	}


    void Filter::RunBoosterFilter(){
        Complx HfVal_Booster;
        Complx tmp1,tmp2,tmp3;
        Complx N0, N1, N2, N3, N4;
        Complx X0, X1, X6, X4, X5;
        Complx P1, P2, P3, P4, P5;
        
        Complx ZinB, ZinB_Reciprocal, ZLB_Reciprocal;
		double omega; // rad per ns = f_Ghz*2*Pi
		        
       
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
            
            X0 = tmp1.Set(1,omega*C4*R2) * tmp2.Set(1, omega*C5*R3) * tmp3.Set(1, omega*R4*(C11+C6)) * (R13*(R13+R7));
            X1 = tmp1.Set(0,-omega*E5*R13*R4*C11)* tmp2.Set(1, omega*C4*R2) * tmp3.Set(1,omega*C5*R3) + tmp3.Set(E5*R13*R4*G2*G3*G4*R2*R3,0);
            X6 = tmp1.Set(1,omega*C4*R2)*tmp2.Set(1,omega*C5*R3)*tmp3.Set(1,omega*R4*(C11+C6))*(R13);
            X4 = tmp1.Set(0,-omega*(R13+R7)*R13*R4*C11)*(tmp2.Set(0,omega*C11)*tmp3.Set(1,omega*C4*R2)*tmp2.Set(1,omega*C5*R3)+tmp1.Set(-G2*G3*G4*R2*R3,0));
            X5 = tmp1.Set(0,omega*(R13+R7)*R13*(C0+C11)) * tmp2.Set(1,omega*C4*R2) * tmp3.Set(1, omega*C5*R3) * tmp1.Set(1, omega*R4*(C11+C6));
            ZinB=(X0)/(X1+X6+X4+X5);
            ZinB_Reciprocal = (X1+X6+X4+X5)/ X0;
            
            P1 = tmp1.Set(0, omega*R10*C10) * (tmp2.Set(0, omega*R8*C8) + tmp3.Set(1, omega*R8*C7) * tmp1.Set(1, omega*R9*C8) ) + tmp1.Set(0, omega*R8*C10) + tmp2.Set(0, omega*R9*C10) * tmp1.Set(1, omega*R8*C7) ;
            P2 = tmp1.Set(1, omega*R11*C10) * ( tmp1.Set(0, omega*R8*C9) + tmp2.Set(0, omega*R9*C9) * tmp3.Set(1, omega*R8*C7) ) ; 
            P3 = tmp1.Set(1, omega*C10*R11) * (tmp2.Set(0, omega*C8*R8) + tmp1.Set(1, omega*C7*R8) * tmp2.Set(1, omega*C8*R9)) * tmp1.Set(1, omega*C9*R10);
            P4 = tmp1.Set(0, omega*C10) * ( tmp2.Set(0, omega*C7*R9) + tmp1.Set(0, omega*C7*R10)*tmp2.Set(1, omega*C8*R9) + tmp3.Set(1, omega*C8*R10));
            P5 = (tmp1.Set(0, omega*C9) * tmp1.Set(1, omega*C7*R9) + (tmp1.Set(0, omega*C7)* tmp1.Set(1, omega*C8*R9) + tmp1.Set(0, omega*C8)) * tmp3.Set(1, omega*C9*R10)) * tmp1.Set(1, omega*C10*R11);
            
            
            N0 = ZinB /(ZinB + tmp1.Set(R6,0));
            
            //ZLB = (P1 + P2 + P3)/(P4 +P5);
            ZLB_Reciprocal = (P4 +P5) / (P1 + P2 + P3);
            //ZinB_Reciprocal.Set(1,0);
            //N1 = ZinB_Reciprocal * R6 + tmp1.Set(1,0);
            N2 = ZLB_Reciprocal + tmp1.Set(1/R7 + 1/R13, 0);
            //N2 = tmp1.Set(1/R7 + 1/R13, 0);
            N3 = tmp1.Set(1/R2, omega*C4) * tmp2.Set(1/R3, omega*C5); 
            N4 = tmp1.Set(1/R4, omega*(C6+C11)) * R7;
            N3.Reciprocal();
            tmp3 = N3 * (-G2*G3*G4);
            tmp1 = (tmp2.Set(0, omega*C11) + tmp3 ) * E5;
            
            tmp2 = tmp1/N4;
            tmp3 = tmp2 + tmp1.Set(1/R13,0);
            HfVal_Booster = (N0 * tmp3) / N2 ;
            
            //HfVal_Booster.Set(10.0,0);
            //std::cout << HfVal_Booster ;
            //HfVal_Booster.conjugate();
			Filter_Tf.emplace_back(HfVal_Booster);
		}
		
        
        
    }

    void Filter::RunBoosterShaperFilter(){
        
        Complx HfVal_ShaperV2;
        Complx tmp1,tmp2,tmp3;
        Complx Q1, Q2, Q3;
		double omega; // rad per ns = f_Ghz*2*Pi
		        
        //std::cout <<"Area: " << SensorArea << "\n" << tmp1 << tmp2 << tmp3 << W0 ;
        
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
            Q1 = tmp1.Set(0, omega*R10*C10) * (tmp2.Set(0, omega*R8*C8)+ tmp3.Set(1, omega*C7*R8) * tmp1.Set(1, omega*C8*R9))
                 +tmp1.Set(0, omega*R8*C10) + tmp2.Set(0, omega*R9*C10)* tmp3.Set(1, omega*C7*R8) ; 
            Q2 = tmp1.Set(1, omega*C10*R11)*(tmp2.Set(0, omega*C9*R8)+ tmp1.Set(0, omega*C9*R9)* tmp3.Set(1, omega*C7*R8))  ;
            Q3 = tmp1.Set(1, omega*C10*R11) * (tmp2.Set(0, omega*C8*R8)+ tmp3.Set(1, omega*C7*R8)*tmp1.Set(1, omega*C8*R9)) * tmp1.Set(1, omega*C9*R10);
            HfVal_ShaperV2 = (Q1+Q2+Q3);
            HfVal_ShaperV2.Reciprocal();
            //std::cout << HfVal_ShaperV2 ;
            //HfVal_ShaperV2.Set(1,0);
            //HfVal_ShaperV2.conjugate();

			Filter_Tf.emplace_back(HfVal_ShaperV2);
		}
		
        
    }



//----------------

	void Filter::RunTIAFilter(){
        
         //std::ofstream myfile;
        //myfile.open ("/afs/cern.ch/work/m/msedghi/private/tempOutputs/FileterTest.txt");

        
		Complx HfVal_tia;
		Complx d1,d2;
		double omega; // rad per ns = f_Ghz*2*Pi
        // current : uA
        // Voltage : mV
        //double TIA_ShaperGain=28;// 1.8*90.0;
		//double rf=5.0; // kOhm
		//double cf=0.25; // pF
        //double cgs=0.4; // pF
        //double cc=315.0 ; // pF // coupling capacitance
		double cd = SensorArea*C_per_cm2;
		double cin_=cgs+(cc*cd/(cd+cc)); // pF
		double i_norton_factor=1.0/(1.0+(cd/cc));
		//double co=0.4; // pF
		//double gin=3; // mS
		double Tau1=rf*cf;
		double Tau2=(cin_*co)/(gin*cf);
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
			d1.Set(1,omega*Tau1);
			d2.Set(1,omega*Tau2);
			HfVal_tia.Set(d1*d2);
			HfVal_tia.Reciprocal();
			HfVal_tia=HfVal_tia*rf*TIA_ShaperGain*i_norton_factor;
            
            //myfile << f_ghz << '\t' << HfVal_tia.mag() << "\n";
			Filter_Tf.emplace_back(HfVal_tia);
		}
        
        //myfile.close();
		
		//std::cout <<"Area: " << SensorArea << ", Cd: " << cd << ", " << "gain: " << TIA_ShaperGain << "\n"  ;
	}


	void Filter::RunShaperFilter(){

		Complx HfVal_Shap;
		Complx d3;
        double Shaper1Gain=1.0;; // gain [V/V]
		double omega; // rad per ns = f_Ghz*2*Pi
        //double Tau_sh= 0.9; // ns
		Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
			d3.Set(1,omega*Tau_sh);
			HfVal_Shap.Set(d3*d3);
			HfVal_Shap.Reciprocal();
			HfVal_Shap=HfVal_Shap*Shaper1Gain;
			Filter_Tf.emplace_back(HfVal_Shap);
		}
	}

    void Filter::Run1stPadeDelayFilter(){
        Complx HfVal;
		Complx n1,d1;
		//double CDF_Delay=2.0; // ns
        double omega; // rad per ns = f_Ghz*2*Pi
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
			n1.Set(2, -omega*CDF_Delay);
			d1.Set(2, omega*CDF_Delay);
			HfVal=n1/d1;
			Filter_Tf.emplace_back(HfVal);
		}
    }
    void Filter::RunIdealDelayFilter(){
        Complx HfVal;
		//double CDF_Delay=2.0; // ns
        double omega; // rad per ns = f_Ghz*2*Pi
        double re, im;
        Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
			re=cos(omega*CDF_Delay);
			im=-sin(omega*CDF_Delay);
			HfVal.Set(re,im);
			Filter_Tf.emplace_back(HfVal);
		}
    }

    void Filter::RunCDFShaper(){
    Complx HfVal_Shap;
		Complx d3;
        //double CFD_Gain=1.5; // gain [V/V]
		double omega; // rad per ns = f_Ghz*2*Pi
        //double Tau_CFDsh= 0.25; // ns
		Filter_Tf.clear();
		for (auto f_ghz: freq_GHz_) {
			omega=2*f_ghz*(FbcmFE::PI);
			d3.Set(1,omega*Tau_CFDsh);
			HfVal_Shap.Set(d3*d3);
			HfVal_Shap.Reciprocal();
			HfVal_Shap=HfVal_Shap*CFD_Gain;
			Filter_Tf.emplace_back(HfVal_Shap);
		}

    }
	
	
	void Filter::SetParameters( const edm::ParameterSet * FEParamPtr ){ 
	FrontEndParamPtr = FEParamPtr;
    edm::ParameterSet ASICParamPset; 
    ASICParamPset = FrontEndParamPtr->getParameter< edm::ParameterSet >("FE2022ASIC"); 
    
    C1 = ASICParamPset.getParameter< double >("C1"); // pF
    Cf0 = ASICParamPset.getParameter< double >("Cf0"); // pF
    Cf1 = ASICParamPset.getParameter< double >("Cf1"); // pF
    R12 = ASICParamPset.getParameter< double >("R12"); // kOhm
    G0 = ASICParamPset.getParameter< double >("G0"); // mS
    R0 = ASICParamPset.getParameter< double >("R0"); // kOhm
    C2 = ASICParamPset.getParameter< double >("C2"); // pF
    G1 = ASICParamPset.getParameter< double >("G1"); // mS
    R1 = ASICParamPset.getParameter< double >("R1"); // kOhm
    C3 = ASICParamPset.getParameter< double >("C3"); // pF
    E0 = ASICParamPset.getParameter< double >("E0"); // v/v
    R5 = ASICParamPset.getParameter< double >("R5"); // kOhm
    R6 = ASICParamPset.getParameter< double >("R6"); // kOhm
    C0 = ASICParamPset.getParameter< double >("C0"); // pF
    G2 = ASICParamPset.getParameter< double >("G2"); // mS
    R2 = ASICParamPset.getParameter< double >("R2"); // kOhm
    C4 = ASICParamPset.getParameter< double >("C4"); // pF
    G3 = ASICParamPset.getParameter< double >("G3"); // mS
    R3 = ASICParamPset.getParameter< double >("R3"); // kOhm
    C5 = ASICParamPset.getParameter< double >("C5"); // pF
    G4 = ASICParamPset.getParameter< double >("G4"); // mS
    R4 = ASICParamPset.getParameter< double >("R4"); // kOhm
    C6 = ASICParamPset.getParameter< double >("C6"); // pF
    E5 = ASICParamPset.getParameter< double >("E5"); // v/v
    R7 = ASICParamPset.getParameter< double >("R7"); // kOhm
    C11 = ASICParamPset.getParameter< double >("C11"); // pF
    R13 = ASICParamPset.getParameter< double >("R13"); // kOhm
    R8 = ASICParamPset.getParameter< double >("R8"); // kOhm
    R9 = ASICParamPset.getParameter< double >("R9"); // kOhm
    R10 = ASICParamPset.getParameter< double >("R10"); // kOhm
    R11 = ASICParamPset.getParameter< double >("R11"); // kOhm
    C7 = ASICParamPset.getParameter< double >("C7");  // pF
    C8 = ASICParamPset.getParameter< double >("C8"); // pF
    C9 = ASICParamPset.getParameter< double >("C9"); // pF
    C10 = ASICParamPset.getParameter< double >("C10"); // pF

    //std::cout << "R1: " << R1 << ", Cf0: " << Cf0 << "\n";
    
	TIA_ShaperGain = FrontEndParamPtr->getParameter< double >("TIA_Shaper_Gain"); // gain [V/V]
    
	rf = FrontEndParamPtr->getParameter< double >("Tia_Rf"); // kOhm
	cf = FrontEndParamPtr->getParameter< double >("Tia_Cf"); // pF
	cgs = FrontEndParamPtr->getParameter< double >("Tia_Cin_gs"); // pF
	cc = FrontEndParamPtr->getParameter< double >("SensorCouplingCapacitance"); // pF // coupling capacitance
	C_per_cm2 = FrontEndParamPtr->getParameter< double >("SensorCapPerCm2"); // pF/cm2
	co = FrontEndParamPtr->getParameter< double >("Tia_Co"); // pF
	gin = FrontEndParamPtr->getParameter< double >("Tia_gin"); // mS
	Tau_sh = FrontEndParamPtr->getParameter< double >("Shaper1_Tau"); // ns //Shaper1 Tau
	CDF_Delay = FrontEndParamPtr->getParameter< double >("CFD_Delay"); // ns
	CFD_Gain = FrontEndParamPtr->getParameter< double >("CfdShaper_Gain"); // gain [V/V]
	Tau_CFDsh = FrontEndParamPtr->getParameter< double >("CfdShaper_Tau"); // ns

// std::cout << "TIA_Shaper_Gain: " << TIA_ShaperGain << "\n"
// << "Tia_Rf: " << rf << "\n"
// << "Tia_Cf: " << cf << "\n"
// << "Tia_Cin_gs: " << cgs << "\n"
// << "SensorCouplingCapacitance: " << cc << "\n"
// << "SensorCapPerCm2: " << C_per_cm2 << "\n"
// << "Tia_Co: " << co << "\n"
// << "Tia_gin: " << gin << "\n"
// << "Shaper1_Tau: " << Tau_sh << "\n"
// << "CDF_Delay: " << CDF_Delay << "\n"
// << "CfdShaper_Gain: " << CFD_Gain << "\n"
// << "CfdShaper_Tau: " << Tau_CFDsh << "\n"
// << "SensorArea: " << SensorArea << "\n";

	}
	
}


