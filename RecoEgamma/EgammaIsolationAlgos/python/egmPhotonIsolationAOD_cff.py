import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.pfNoPileUpIso_cff import * 
from CommonTools.ParticleFlow.pfParticleSelection_cff import * 
from RecoEgamma.EgammaIsolationAlgos.egmPhotonIsolationMiniAOD_cff import IsoConeDefinitions
from RecoEgamma.EgammaIsolationAlgos.egmIsolationDefinitions_cff import pfNoPileUpCandidates
from CommonTools.ParticleFlow.pfNoPileUpIso_cff import pfPileUpIso, pfNoPileUpIso, pfNoPileUpIsoSequence


particleFlowTmpPtrs = cms.EDProducer("PFCandidateFwdPtrProducer",
src = cms.InputTag('particleFlow')
)

egmPhotonIsolation = cms.EDProducer( "CITKPFIsolationSumProducer",
                                     srcToIsolate = cms.InputTag("gedPhotons"),
                                     srcForIsolationCone = cms.InputTag('pfNoPileUpCandidates'),
                                     isolationConeDefinitions = IsoConeDefinitions
                                     )	

egmPhotonIsolationAODSequence = cms.Sequence(particleFlowTmpPtrs + pfNoPileUpIsoSequence + pfNoPileUpCandidates + egmPhotonIsolation)

