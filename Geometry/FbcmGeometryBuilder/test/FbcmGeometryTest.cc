///-------------------------------------------
//  Author: Mohammad Sedghi, msedghi@cern.ch
//  Isfahan University of Technology
//  Date created: September 2020
///-------------------------------------------

#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESTransientHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "Geometry/FbcmGeometry/interface/FbcmGeometry.h"
#include "Geometry/Records/interface/FbcmGeometryRecord.h"
#include "DataFormats/FbcmDetId/interface/FbcmDetId.h" 

class FbcmGeometryTest : public edm::one::EDAnalyzer<> {
public:
  explicit FbcmGeometryTest(const edm::ParameterSet&) {}

  void beginJob() override {}
  void analyze(edm::Event const& iEvent, edm::EventSetup const&) override;
  void endJob() override {}
};

void FbcmGeometryTest::analyze(const edm::Event&, const edm::EventSetup& iEventSetup) {
  edm::LogVerbatim("Geometry") << "FbcmGeometryTest::analyze";
  std::cout << "Hello Mohammad from analyzer before calling ESProducer\n"; 
    
  edm::ESTransientHandle<FbcmGeometry> FbcmGeom;
  iEventSetup.get<FbcmGeometryRecord>().get(FbcmGeom);
  
   edm::ESHandle<FbcmGeometry> FbcmGeom2;
  iEventSetup.get<FbcmGeometryRecord>().get(FbcmGeom2);
  
  std::cout << "Check the delivery of FbcmGeom from ESProducer:\n"; 
  
  
  std::vector<FbcmSiPadGeom const*> allSiPadGeoms=FbcmGeom.product()->SiPads();
  std::vector<FbcmSiPadGeom const*> allSiPadGeoms2=FbcmGeom2->SiPads();
  
 /*  for (int sideId=1; sideId<3; sideId++){
	  for (int st=0 ; st<4 ; st++) {
		  
			  
		  FbcmDetId detId1(sideId,st,3,4); 
		  //std::cout << detId1;
		   FbcmStationGeom const* StationGeomPtr=FbcmGeom2->IdToStation(detId1);
		  // if (StationGeomPtr) {
			  // std::cout << StationGeomPtr->id();
			  // int aa=(*StationGeomPtr).NumOfDiesPerRing();
			  // std::cout << aa << " , HHHIII, " << StationGeomPtr->NumOfRings() << "\n";
		  // }
		  // else
			  // std::cout << "Nothing found\n";
		  if (StationGeomPtr) {
			  if (detId1.StationDetId() != StationGeomPtr->id())
				  std::cout << "Fatal Error\n";
			  else
				 std::cout << "OK for: " << StationGeomPtr->id();
		  }
		  else
			  std::cout << "Nothing found\n";
		  
	  }
  
  } */
  
  
   for (int sideId=1; sideId<3; sideId++){
	  for (int st=0 ; st<4 ; st++) {
		  for (int die=0 ; die<40 ; die++) {
			  
		  FbcmDetId detId1(sideId,st,die,0); 
		  //std::cout << detId1;
		   const FbcmSiliconDieGeom * DieGeomPtr=FbcmGeom2->IdToSiliconDie(detId1);
		   if (DieGeomPtr) {
			  if (detId1.SiliconDieDetId()() != DieGeomPtr->id())
				  std::cout << "Fatal Error\n";
			  else  { 
				  std::cout << "Pos:" << DieGeomPtr->surface().position()  << ",\t"; 
				  std::cout << "nRows: " << DieGeomPtr->NumOfRows() <<"\tnCols: " << DieGeomPtr->NumOfCols() ; 
				  std::cout << ",\tfor: " << DieGeomPtr->id();
			  }
		  }
		  else
			  std::cout << "Nothing found\n";
		  
		  
	  }
	  }
  
  }
  
  //FbcmGeom.product();
  
  	//for(const auto& SiPadGeomDet: allSiPadGeoms2) {
			//std::cout << SiPadGeomDet->id();
			 ////Cool! it is OK!
	//	}
  
 
}

DEFINE_FWK_MODULE(FbcmGeometryTest);