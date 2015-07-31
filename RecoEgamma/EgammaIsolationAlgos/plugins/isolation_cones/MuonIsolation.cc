#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "DataFormats/PatCandidates/interface/Muon.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "PhysicsTools/IsolationAlgos/interface/IsoDepositVetoFactory.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"

#include "PhysicsTools/IsolationAlgos/interface/CITKIsolationConeDefinitionBase.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"


#include <unordered_map>

namespace pat {
  typedef edm::Ptr<pat::PackedCandidate> PackedCandidatePtr;
}

class MuonIsolation : public citk::IsolationConeDefinitionBase {
public:
  MuonIsolation(const edm::ParameterSet& c) :
    citk::IsolationConeDefinitionBase(c),
    _miniAODVertexCodes(c.getParameter<std::vector<unsigned> >("miniAODVertexCodes")),
    _isolateAgainst(c.getParameter<std::string>("isolateAgainst")) {  }
  MuonIsolation(const MuonIsolation&) = delete;
  MuonIsolation& operator=(const MuonIsolation&) =delete;
  
  void setConsumes(edm::ConsumesCollector) {}

  bool isInIsolationCone(const reco::CandidatePtr& physob,
			 const reco::CandidatePtr& other) const override final;
  
  //! Destructor
  virtual ~MuonIsolation(){};
  
private:    
  const std::vector<unsigned> _miniAODVertexCodes;
  const std::string _isolateAgainst;
  edm::EDGetTokenT<reco::VertexCollection> _vtxToken;
};

DEFINE_EDM_PLUGIN(CITKIsolationConeDefinitionFactory,
		  MuonIsolation,
		  "MuonIsolation");

bool MuonIsolation::
isInIsolationCone(const reco::CandidatePtr& physob,
		  const reco::CandidatePtr& iso_obj  ) const {
  pat::PackedCandidatePtr aspacked(iso_obj);
  reco::PFCandidatePtr aspf(iso_obj);
  
  const float deltar2 = reco::deltaR2(*physob,*iso_obj);
  bool isMuon = false;  
  bool result = true;
  if( aspacked.isNonnull() && aspacked.get() ) {    
    if( aspacked->charge() != 0 ) {
      bool is_vertex_allowed = false;
      for( const unsigned vtxtype : _miniAODVertexCodes ) {
	if( vtxtype == aspacked->fromPV() ) {
	  is_vertex_allowed = true;
	  break;
	}
      }      
      result *= ( is_vertex_allowed );
    }
    if (fabs(aspacked -> pdgId()) == 13 ) isMuon = true;
    result *= (isMuon);
    result *= deltar2 < _coneSize2 ;
  } else if ( aspf.isNonnull() && aspf.get() ) { 
    if (fabs(aspf -> pdgId() == 13)) isMuon = true;
    result *= isMuon;   
    result *= deltar2 < _coneSize2;
  } else {
    throw cms::Exception("InvalidIsolationInput")
      << "The supplied candidate to be used as isolation "
      << "was neither a reco::PFCandidate nor a pat::PackedCandidate!";
  }
  return result;
}
