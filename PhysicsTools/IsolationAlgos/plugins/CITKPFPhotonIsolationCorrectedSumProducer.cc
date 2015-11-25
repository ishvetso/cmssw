#ifndef PhysicsTools_IsolationAlgos_CITKIsolationCorrectedSumProducer_H
#define PhysicsTools_IsolationAlgos_CITKIsolationCorrectedSumProducer_H

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositFwd.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "PhysicsTools/IsolationAlgos/interface/EventDependentAbsVeto.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "PhysicsTools/IsolationAlgos/interface/CITKIsolationConeDefinitionBase.h"
#include "DataFormats/Common/interface/OwnVector.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"

#include <string>
#include <unordered_map>

namespace edm { class Event; }
namespace edm { class EventSetup; }

namespace reco {
  typedef edm::Ptr<reco::Photon> recoPhotonPtr;
}
double kappa (double eta){
  double value;
  if (std::abs(eta) < 2.) value = 4.5*10e-3;
  else value = 3.*10e-3;
  return value; 
}

double Area(double eta){
  double value;
  if (std::abs(eta) < 0.9 ) value = 0.17;
  else if ( 0.9 <= std::abs(eta) < 1.4442) value = 0.14;
  else if ( 1.566 < std::abs(eta) < 2.0 ) value = 0.11;
  else if ( 2.0 <= std::abs(eta) < 2.2 ) value = 0.14;
  else if ( std::abs(eta) >= 2.2 ) value = 0.22;
  else value = 0.;

  return value;
}

namespace citk {
  class PFIsolationCorrectedSumProducer : public edm::EDProducer {
    
  public:  
    PFIsolationCorrectedSumProducer(const edm::ParameterSet&);
    
    virtual ~PFIsolationCorrectedSumProducer() {}
    
    void beginLuminosityBlock(const edm::LuminosityBlock&,
			      const edm::EventSetup&) override final;

    void produce(edm::Event&, const edm::EventSetup&) override final;
    
  private:  
    // datamembers
    static constexpr unsigned kNPFTypes = 8;
    typedef std::unordered_map<std::string,int> TypeMap;
    typedef std::vector<std::unique_ptr<IsolationConeDefinitionBase> > IsoTypes;
    typedef edm::View<reco::Candidate> CandView;
    const TypeMap _typeMap;
    edm::EDGetTokenT<CandView> _to_isolate, _isolate_with;
    edm::EDGetTokenT<double> _rho;
    // indexed by pf candidate type
    std::array<IsoTypes,kNPFTypes> _isolation_types; 
    std::array<std::vector<std::string>,kNPFTypes> _product_names;
  };
}

typedef citk::PFIsolationCorrectedSumProducer CITKPFIsolationCorrectedSumProducer;

DEFINE_FWK_MODULE(CITKPFIsolationCorrectedSumProducer);

namespace citk {
  PFIsolationCorrectedSumProducer::PFIsolationCorrectedSumProducer(const edm::ParameterSet& c) :
    _typeMap( { {"h+",1},
	        {"h0",5},
		{"gamma",4},
		{"electron",2},
		{"muon",3},
		{"HFh",6},
		{"HFgamma",7} } ){
    _to_isolate = 
      consumes<CandView>(c.getParameter<edm::InputTag>("srcToIsolate"));
    _isolate_with = 
      consumes<CandView>(c.getParameter<edm::InputTag>("srcForIsolationCone"));
      _rho = consumes<double>(c.getParameter<edm::InputTag>("rho"));
    const std::vector<edm::ParameterSet>& isoDefs = 
      c.getParameterSetVector("isolationConeDefinitions");
    for( const auto& isodef : isoDefs ) {
      const std::string& name = 
	isodef.getParameter<std::string>("isolationAlgo");
      const float coneSize = isodef.getParameter<double>("coneSize");
      char buf[50];
      sprintf(buf,"DR%.2f",coneSize);
      std::string coneName(buf);
      auto decimal = coneName.find('.');
      if( decimal != std::string::npos ) coneName.erase(decimal,1);
      const std::string& isotype = 
	isodef.getParameter<std::string>("isolateAgainst");
      IsolationConeDefinitionBase* theisolator =
	CITKIsolationConeDefinitionFactory::get()->create(name,isodef);
      theisolator->setConsumes(consumesCollector());
      const auto thetype = _typeMap.find(isotype);
      if( thetype == _typeMap.end() ) {
	throw cms::Exception("InvalidIsolationType")
	  << "Isolation type: " << isotype << " is not available in the "
	  << "list of allowed isolations!.";
      }
      _isolation_types[thetype->second].emplace_back(theisolator);
      //std::cout << thetype->second << std::endl;
      const std::string dash("-");
      std::string pname = isotype+dash+coneName+dash+theisolator->additionalCode();
      _product_names[thetype->second].emplace_back(pname);
      produces<edm::ValueMap<float> >(pname);
    }
  }

  void  PFIsolationCorrectedSumProducer::
  beginLuminosityBlock(const edm::LuminosityBlock&,
		       const edm::EventSetup& es) {
    for( const auto& isolators_for_type : _isolation_types ) {
      for( const auto& isolator : isolators_for_type ) {
	isolator->getEventSetupInfo(es);
      }
    }
  }

  void  PFIsolationCorrectedSumProducer::
  produce(edm::Event& ev, const edm::EventSetup& es) {
    typedef std::auto_ptr<edm::ValueMap<float> >  product_type;
    typedef std::vector<float> product_values;
    edm::Handle<CandView> to_isolate;
    edm::Handle<CandView> isolate_with;
    edm::Handle<double> rho;
    ev.getByToken(_to_isolate,to_isolate);
    ev.getByToken(_isolate_with,isolate_with);
    ev.getByToken(_rho,rho);
    // the list of value vectors indexed as "to_isolate"
    std::array<std::vector<product_values>,kNPFTypes> the_values;    
    // get extra event info and setup value cache
    unsigned i = 0;
    for( const auto& isolators_for_type : _isolation_types ) {
      the_values[i++].resize(isolators_for_type.size());
      for( const auto& isolator : isolators_for_type ) {
	isolator->getEventInfo(ev);
      }
    }
    reco::PFCandidate helper; // to translate pdg id to type    
    // loop over the candidates we are isolating and fill the values
    for( size_t c = 0; c < to_isolate->size(); ++c ) {
      auto cand_to_isolate = to_isolate->ptrAt(c);
      reco::recoPhotonPtr asPhotonPtr(cand_to_isolate); // need this for correction of photon isolation
      if (!asPhotonPtr) throw cms::Exception("InvalidIsolationType") << "this module is defined explicitly for photons." << std::endl;
      double photon_eta =  asPhotonPtr -> superCluster()->seed() -> eta();
      double photon_pt = asPhotonPtr -> pt();
      std::array<std::vector<float>,kNPFTypes> cand_values;      
      unsigned k = 0;
      for( const auto& isolators_for_type : _isolation_types ) {
	cand_values[k].resize(isolators_for_type.size());
	for( auto& value : cand_values[k] ) value = 0.0;
	++k;
      }
      for( size_t ic = 0; ic < isolate_with->size(); ++ic ) {
        auto isocand = isolate_with->ptrAt(ic);
	auto isotype = helper.translatePdgIdToType(isocand->pdgId());	
	const auto& isolations = _isolation_types[isotype];	
  //std::cout << "type : "<< isotype << " size : "<< isolations.size() << std::endl;
	for( unsigned i = 0; i < isolations.size(); ++ i  ) {
	  if( isolations[i]->isInIsolationCone(cand_to_isolate,isocand) ) {
	    cand_values[isotype][i] += isocand->pt();
	  }
	}
      }
      // add this candidate to isolation value list
      for( unsigned i = 0; i < kNPFTypes; ++i ) {
        //std::cout << "cand values size : " << cand_values[i].size() << std::endl;
	for( unsigned j = 0; j < cand_values[i].size(); ++j ) {
    //if this is not a photon isolation things remain as asual
	  if (i != 4) the_values[i][j].push_back(cand_values[i][j]);
    else {
      the_values[i][j].push_back(2.5 + cand_values[i][j] - (*rho)*Area(photon_eta) - kappa(photon_eta)*photon_pt );
    }
	}
      }
    }
    // fill and put all products
    for( unsigned i = 0; i < kNPFTypes; ++ i ) {
      for( unsigned j = 0; j < the_values[i].size(); ++j ) {
	product_type the_product( new edm::ValueMap<float> );
	edm::ValueMap<float>::Filler fillerprod(*the_product);
	fillerprod.insert(to_isolate, 
			  the_values[i][j].begin(),
			  the_values[i][j].end());
	fillerprod.fill();
	ev.put(the_product,_product_names[i][j]);
      }
    }
  }
}

#endif
