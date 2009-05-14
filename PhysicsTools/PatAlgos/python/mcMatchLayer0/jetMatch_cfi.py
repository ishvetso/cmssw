import FWCore.ParameterSet.Config as cms

#
# Example for a configuration of the MC match
# for jets (cuts are NOT tuned!!)
# Using old TQAF cuts of january 2008
#
jetPartonMatch = cms.EDFilter("MCMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src = cms.InputTag("iterativeCone5CaloJets"),    # RECO objects to match
    matched = cms.InputTag("genParticles"), # mc-truth particle collection
    mcPdgId  = cms.vint32(1, 2, 3, 4, 5, 21), # one or more PDG ID (quarks except top; gluons)
    mcStatus = cms.vint32(3),                 # PYTHIA status code (3 = hard scattering)
    checkCharge = cms.bool(False),            # False = any value of the charge of MC and RECO is ok
    maxDeltaR = cms.double(0.4), # Minimum deltaR for the match
    maxDPtRel = cms.double(3.0), # Minimum deltaPt/Pt for the match
    resolveAmbiguities = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(False), # False = just match input in order; True = pick lowest deltaR pair first
)

jetGenJetMatch = cms.EDFilter("GenJetMatcher", # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src      = cms.InputTag("iterativeCone5CaloJets"),         ## RECO jets (any View<Jet> is ok)
    matched  = cms.InputTag("iterativeCone5GenJets"), ## GEN jets  (must be GenJetCollection)
    mcPdgId  = cms.vint32(),       # n/a
    mcStatus = cms.vint32(),       # n/a
    checkCharge = cms.bool(False), # n/a
    maxDeltaR = cms.double(0.4), # Minimum deltaR for the match
    maxDPtRel = cms.double(3.0), # Minimum deltaPt/Pt for the match
    resolveAmbiguities = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(False), # False = just match input in order; True = pick lowest deltaR pair first
)


