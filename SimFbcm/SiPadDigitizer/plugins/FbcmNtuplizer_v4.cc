
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/DetSetVector.h"
//#include "DataFormats/...

#include "DataFormats/FbcmDigi/interface/SiPadDigiData.h"
#include "DataFormats/FbcmDetId/interface/FbcmDetId.h"

#include "Geometry/Records/interface/FbcmGeometryRecord.h"
#include "Geometry/FbcmGeometry/interface/FbcmGeometry.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TTree.h"
#include <string> 

#define MAX_SIMHIT_SIZE 100
#define MAX_DIGHIT_SIZE 100
#define MAX_BXSlot_SIZE 100
#define AREA_GROUP_LEN 8

#define TEST_IND 7

using namespace std;

class FbcmNtuplizer_v4 : public edm::EDAnalyzer {
public:
  explicit FbcmNtuplizer_v4(const edm::ParameterSet&);
  ~FbcmNtuplizer_v4();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;


  // ----------member data ---------------------------
  
  std::vector< edm::EDGetTokenT< edm::DetSetVector<SiPadDigiData> > > TokenTags_;
  edm::ESHandle<FbcmGeometry> theFbcmGeom;
  //const std::vector<edm::ParameterSet> sectors_;
  
  
  //std::map<std::string, TFileDirectory> tagDirectory;
  std::vector<TFileDirectory> tagDirectories;
  
  std::vector< TH1* > hNEvents;
  std::vector< TH1* > hNSensorGroups;
  
  std::vector< TTree* > theTree;
  std::vector< TTree* > FixedValuesTree;
  
  std::vector<std::string> instanceNames;
  
  float SensorArea;
  float SensorRho;
  
  int SensorGroupIndex; // collected for each hit. 
  int numberOfSensorGroups; // maximum number of SiGroupIndex used in the digi step. 
  int nbrOfDiesPerRing; 

  
  //int NumOfSensors;
  
  int nSimParticles;
  int BxSlotCnt; 
  int nValidDigiToAs;
  int nValidDigiToTs;
  
  
  int SimPdgIds[MAX_SIMHIT_SIZE];
  float SimPts[MAX_SIMHIT_SIZE];
  float SimCharges[MAX_SIMHIT_SIZE];
  float SimTofs[MAX_SIMHIT_SIZE];
  float SimTof_perBx[MAX_SIMHIT_SIZE];

  int DigiHitStatus[MAX_BXSlot_SIZE];
  int nDigiHits[MAX_BXSlot_SIZE]; 
  
  float DigiToAs[MAX_DIGHIT_SIZE] ;
  float DigiToTs[MAX_DIGHIT_SIZE];
  float PeakAmpl[MAX_DIGHIT_SIZE];
  
  
  int nTotalRhuDigi;
  int nInterstedRhuBins; 
  int DigiRHUs[MAX_DIGHIT_SIZE] ;
  
  std::vector < int > tmpVect;
  std::vector < int > rhuInterestedHitBins_;
  //std::vector < int > rhuFullBxBinRange_;
  
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
FbcmNtuplizer_v4::FbcmNtuplizer_v4(const edm::ParameterSet& iConfig) :
  //TokenTag_(consumes< edm::DetSetVector<SiPadDigiData> >(iConfig.getParameter<edm::InputTag>("FbcmDigiTag"))),
  instanceNames(iConfig.getParameter< std::vector<std::string> >("InstanceNameTags")),
  numberOfSensorGroups(0)
{
    //edm::InputTag tag(hitsProducer_, SubdetName_);
  numberOfSensorGroups=0;
  Int_t bsize = 32000; //default
  
  
  edm::Service<TFileService> fs;
  //TFileDirectory subDir;  
  tagDirectories.clear();
  theTree.clear();
  FixedValuesTree.clear();
  hNEvents.clear();
  hNSensorGroups.clear();
  
  for(auto it = std::begin(instanceNames); it != std::end(instanceNames); ++it) {
    edm::InputTag tag("simFbcmDigis", it->c_str() );
    TokenTags_.emplace_back( consumes< edm::DetSetVector<SiPadDigiData> >( tag )  );   
      
    //tagDirectory[*it] = fs->mkdir( it->c_str() );
    //subDir = fs->mkdir( it->c_str() ) ;
    tagDirectories.emplace_back( fs->mkdir( it->c_str() ) );
    theTree.emplace_back( tagDirectories.back().make<TTree>( iConfig.getParameter< string >("TreeName").c_str() , "all hits" ));
    FixedValuesTree.emplace_back( tagDirectories.back().make<TTree>( "GeometryInfo" , "FixedValues" )   );
    hNEvents.emplace_back( tagDirectories.back().make<TH1I>("hNEvents" , "" , 1 , 0 , 1 )  );
    hNSensorGroups.emplace_back( tagDirectories.back().make<TH1I>("hNSensorGroups", "", 1, 0, 1)  );
    
    theTree.back()->Branch("SensorRho" , &SensorRho , "SensorRho/F", bsize );
    theTree.back()->Branch("SensorArea" , &SensorArea , "SensorArea/F" , bsize  );
  theTree.back()->Branch("nSimParticles" , &nSimParticles);
  theTree.back()->Branch("SensorGroupIndex" , &SensorGroupIndex); 
  theTree.back()->Branch("SimPdgId" , SimPdgIds , "SimPdgId[nSimParticles]/I" , bsize );
  theTree.back()->Branch("SimPt" , SimPts , "SimPt[nSimParticles]/F" , bsize );
  theTree.back()->Branch("SimCharge" , SimCharges , "SimCharge[nSimParticles]/F", bsize );
  theTree.back()->Branch("SimTof" , SimTofs , "SimTof[nSimParticles]/F", bsize ); 
  theTree.back()->Branch("SimTof_perBx" , SimTof_perBx , "SimTof_perBx[nSimParticles]/F", bsize ); 
  theTree.back()->Branch("BxSlotCnt" , &BxSlotCnt);
  theTree.back()->Branch("DigiHitStatus" , DigiHitStatus , "DigiHitStatus[BxSlotCnt]/I", bsize );
  theTree.back()->Branch("nDigiHits" , nDigiHits , "nDigiHits[BxSlotCnt]/I" , bsize ); 
  theTree.back()->Branch("nValidDigiToAs" , &nValidDigiToAs);
  theTree.back()->Branch("nValidDigiToTs" , &nValidDigiToTs);
  theTree.back()->Branch("DigiToA" , DigiToAs , "DigiToAs[nValidDigiToAs]/F" , bsize );
  theTree.back()->Branch("DigiToT" , DigiToTs , "DigiToTs[nValidDigiToTs]/F", bsize );
  theTree.back()->Branch("PeakAmplitude" , PeakAmpl , "PeakAmpl[nValidDigiToAs]/F" , bsize );
  theTree.back()->Branch("nTotalRhuDigi" , &nTotalRhuDigi);
  theTree.back()->Branch("nInterstedRhuBins" , &nInterstedRhuBins);
  theTree.back()->Branch("DigiRHU" , DigiRHUs , "DigiRHUs[nTotalRhuDigi]/I", bsize );
    
    
  }

   /*  for (const auto& v: tagDirectory) {

      cout << v.first << "\n" ;
  
    } */
  
  
  
  //theTree = tagDirectory[instanceNames[0]].make<TTree>( iConfig.getParameter< string >("TreeName").c_str() , "all hits" );
  //FixedValuesTree = tagDirectory[instanceNames[0]].make<TTree>( "GeometryInfo" , "FixedValues" );
  //hNEvents = tagDirectory[instanceNames[0]].make<TH1I>("hNEvents" , "" , 1 , 0 , 1 );
  //hNSensorGroups = tagDirectory[instanceNames[0]].make<TH1I>("hNSensorGroups", "", 1, 0, 1);
 

  //theTree->Branch("SensorRho" , &SensorRho , "SensorRho/f[8,22]", bsize ); // just to remmember: /f[8,22] causes misreading
  //theTree->Branch("SensorArea" , &SensorArea , "SensorArea/f[0.01,1.0]" , bsize  ); // just to remmember: /f[8,22] causes misreading
  
  
  
  tmpVect = iConfig.getParameter< std::vector<int>  >("RHU_InterestedHitBins");
  
  rhuInterestedHitBins_.clear();
  for (int i = tmpVect.front(); i <= tmpVect.back(); i++) 
      rhuInterestedHitBins_.emplace_back(i);
  
  //tmpVect = iConfig.getUntrackedParameter< std::vector<int> >("RHU_FullBxBinRange", {-2,1});
  //rhuFullBxBinRange_.clear();
  //for (int i = tmpVect.front(); i <= tmpVect.back(); i++) 
      //rhuFullBxBinRange_.emplace_back(i);

}


FbcmNtuplizer_v4::~FbcmNtuplizer_v4()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
FbcmNtuplizer_v4::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  using namespace edm;
  using namespace std;

  for(long unsigned int i=0; i < tagDirectories.size(); i++){
   
    //   edm::InputTag tag("simFbcmDigis", instanceNames[i]);
    //TokenTag_ = consumes< edm::DetSetVector<SiPadDigiData> > (tag); // does not works here! consumes should be called in the constroctor
   
   //std::cout << "here is reach out. \n"; 
   
  hNEvents[i]->Fill( 0.5 );

  edm::Handle< edm::DetSetVector<SiPadDigiData> > handle;
  
  iEvent.getByToken(TokenTags_[i] ,handle);
  // iEvent.getByLabel(tag, handle);
  
  //int SiDieId;
  for (edm::DetSetVector<SiPadDigiData>::const_iterator itDetSet = handle->begin() ;  itDetSet < handle->end() ; ++itDetSet) {
    // each Det in fbcmDets: multiple Data, but we have only one data
    if( itDetSet->size() != 1 )
      cout << "size == " << itDetSet->size() << endl; 
    for (std::vector<SiPadDigiData>::const_iterator Digidata_it = itDetSet->begin() ; Digidata_it < itDetSet->end() ; ++Digidata_it) {
      //const SiPadDigiData Digidata= *(Digidata_it);
      //SiDieId=Digidata_it->SiliconDieIndex() ;
      //SensorGroupIndex = SiDieId % nbrOfDiesPerRing;
      SensorGroupIndex = Digidata_it->SiGroupIndex();
      
      if ( SensorGroupIndex > numberOfSensorGroups )
          numberOfSensorGroups=SensorGroupIndex;
 
      SensorRho=Digidata_it->Radius() ;
      SensorArea=Digidata_it->Area() ;

      nSimParticles = 0 ; 
      for(auto sim : Digidata_it->CahrgePsimVector()) {
	SimPdgIds[nSimParticles] = sim.second.ParticleType() ;
	SimPts[nSimParticles] = sim.second.Pabs() ;
	SimTofs[nSimParticles] = sim.second.Tof() ;
	SimCharges[nSimParticles] = sim.first;
	SimTof_perBx[nSimParticles] = sim.second.Tof() - 25.0 * sim.second.BunchCrossing() ;
	//SimHitTime = sim.second.time() - 25.0 * sim.second.BunchCrossing() ;
	nSimParticles++;
      }
 
      nValidDigiToAs=0;
      nValidDigiToTs=0;
	  nTotalRhuDigi=0;
      nInterstedRhuBins=0;
      
      BxSlotCnt=0; // just to make sure starting from non-zero index if in the case of using BxSlotNo < 0. 
      for(auto hit : Digidata_it->BxSlotHitAnalysisVector() ) {	  
            DigiHitStatus[BxSlotCnt] = hit.Bx_HitStatusInt(); 
            nDigiHits[BxSlotCnt] = hit.nbrOfRecognizedHitsInBx(); 
            BxSlotCnt++; 
                    
            for (auto ToaTot : hit.TotToaVectort()) {
                
              if ( (ToaTot.ToAToAStatusInt() == ToAStatus::FullyWithinBx || ToaTot.ToAToAStatusInt() == ToAStatus::WithinBx_LastsAfter ) ) 
              {
                  {
                      DigiToAs[nValidDigiToAs] = ToaTot.ToA();
                      PeakAmpl[nValidDigiToAs] = ToaTot.PeakAmplitude();
                      nValidDigiToAs++;
                  }
                if (ToaTot.IsToTValid())
                  DigiToTs[nValidDigiToTs++] = ToaTot.ToT();
              
                DigiRHUs[nTotalRhuDigi++] = ToaTot.SubBxBinNumber();
                if (std::find(rhuInterestedHitBins_.begin(), rhuInterestedHitBins_.end(),ToaTot.SubBxBinNumber())!=rhuInterestedHitBins_.end())
                    nInterstedRhuBins++;
              
              }

            }
		
      }
 

      theTree[i]->Fill();

    }
  }
  
  
     }
  
}


// ------------ method called once each job just before starting event loop  ------------
void 
FbcmNtuplizer_v4::beginJob()
{
  
}

// ------------ method called once each job just after ending the event loop  ------------
void FbcmNtuplizer_v4::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------

void FbcmNtuplizer_v4::beginRun(edm::Run const&, edm::EventSetup const& iSetup) {
  
  
  //std::cout << rhuInterestedHitBins_.front() << ", " << rhuInterestedHitBins_.back() << "\n" ; 
  //std::cout << rhuFullBxBinRange_.front() << ", " << rhuFullBxBinRange_.back() << "\n" ; 
  
    //for (auto v : rhuInterestedHitBins_) 
      //std::cout << v << ", ";
    //std::cout << "\n"; 
    //for (auto v : rhuFullBxBinRange_) 
      //std::cout << v << ", "; 
  
  iSetup.get<FbcmGeometryRecord>().get(theFbcmGeom); 
  const std::vector<const FbcmStationGeom*> AllStatitons = theFbcmGeom->Stations();
  const std::vector<FbcmSiPadGeom const*> allSiPadGeoms = theFbcmGeom->SiPads();
  nbrOfDiesPerRing = AllStatitons[0]->NumOfDiesPerRing(); 
  
    
  for(long unsigned int i=0; i < tagDirectories.size(); i++){
      
      //std::cout << instanceNames[i] << "\n";
      
  int SiDieId=0;
  int SiDieGroupIndex=0;
  float padX, padY , padRho;

  FixedValuesTree[i]->Branch("SiDieGroupIndex" , &SiDieGroupIndex );
  FixedValuesTree[i]->Branch("SensorX" , &padX );
  FixedValuesTree[i]->Branch("SensorY" , &padY );
  FixedValuesTree[i]->Branch("SensorRho" , &padRho );

  for(const auto& siPad : allSiPadGeoms)
    {
      std::pair<float, float> SiPadDimension = siPad->SiPadTopology().pitch();

      padX = SiPadDimension.first;
      padY = SiPadDimension.second;
      // we could also store only the Area instead of padX and padY
      padRho = siPad->surface().position().perp(); 
	  
      SiDieId=siPad->id().SiliconDie();
      SiDieGroupIndex = SiDieId % nbrOfDiesPerRing;
	  
        //std::cout << SiDieId <<", " << SiDieGroupIndex <<"\n"; 
      
      FixedValuesTree[i]->Fill();
    }
    
  }
}



// ------------ method called when ending the processing of a run  ------------

  void 
  FbcmNtuplizer_v4::endRun(edm::Run const&, edm::EventSetup const&)
  {
      numberOfSensorGroups++; // becuse indecies begin from zero
      
      //hNSensorGroups->Fill(0.5, nbrOfDiesPerRing); 
      for(long unsigned int i=0; i < tagDirectories.size(); i++){
      hNSensorGroups[i]->Fill(0.5, numberOfSensorGroups); 
      }
  }


// ------------ method called when starting to processes a luminosity block  ------------
/*
  void 
  FbcmNtuplizer_v4::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
  void 
  FbcmNtuplizer_v4::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FbcmNtuplizer_v4::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  //  edm::ParameterSetDescription desc;
  //desc.setUnknown();
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FbcmNtuplizer_v4);
