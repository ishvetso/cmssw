import os
myVector = []
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-magraph-LO.root outputFileName=LO idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-magraph-LO.root outputFileName=LO idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-LO-pileup-Up.root outputFileName=pileup-Up idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-LO-pileup-Up.root outputFileName=pileup-Up idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-LO-pileup-Down.root outputFileName=pileup-Down idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-LO-pileup-Down.root outputFileName=pileup-Down idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-powheg.root outputFileName=powheg idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-powheg.root outputFileName=powheg idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-WP90Tag.root outputFileName=WP90Tag idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-WP90Tag.root outputFileName=WP90Tag idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-amcatNLO.root outputFileName=NLO-cutAndcount idName=passingTrigWP90 doCutAndCount=True outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitter.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-amcatNLO.root outputFileName=NLO-cutAndcount idName=passingTrigWP80 doCutAndCount=True outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterRangeSystematics.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-magraph-LO.root idName=passingTrigWP80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterRangeSystematics.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-magraph-LO.root idName=passingTrigWP90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")

count = 0
for i in myVector :
	f = file("jobs/job-" + str(count) + ".sh", "w+")
	f.write("cd /afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/ \n")
	f.write("eval `scramv1 runtime -sh` \n")
	f.write("cd /afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/ \n")
	f.write(i)
	f.close()
	os.system("chmod 744 jobs/job-" + str(count) + ".sh")
	bashstring = "bsub -R \"pool>30000\" -q 1nd -J  job" + str(count) + " < jobs/job-" + str(count) + ".sh"
	os.system(bashstring)
	count += 1
