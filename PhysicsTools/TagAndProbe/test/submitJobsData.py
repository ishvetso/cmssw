import os
myVector = []
myVector.append("cmsRun fitterDataWithManyTemplates.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP90 WP=90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplates.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP80 WP=80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataManyTemplatesRangeSystematics.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root  idName=passingTrigWP90 WP=90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataManyTemplatesRangeSystematics.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root  idName=passingTrigWP80 WP=80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesBreitWigner.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP90 WP=90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesBreitWigner.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP80 WP=80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesExpBkg.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP90 WP=90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesExpBkg.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/data-total.root idName=passingTrigWP80 WP=80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesWP90Tag.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-WP90Tag.root  idName=passingTrigWP90 WP=90 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")
myVector.append("cmsRun fitterDataWithManyTemplatesWP90Tag.py inputFileName=/afs/cern.ch/work/i/ishvetso/TagAndProbe/trees/TnPTree_mc-WP90Tag.root  idName=passingTrigWP80 WP=80 outputDirectory=/afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/fit_results/")

count = 0
for i in myVector :
	f = file("jobs_data/job-" + str(count) + ".sh", "w+")
	f.write("cd /afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/ \n")
	f.write("eval `scramv1 runtime -sh` \n")
	f.write("cd /afs/cern.ch/work/i/ishvetso/TagAndProbe/CMSSW_7_4_15/src/PhysicsTools/TagAndProbe/test/ \n")
	f.write(i)
	f.close()
	os.system("chmod 744 jobs/job-" + str(count) + ".sh")
	bashstring = "bsub -R \"pool>30000\" -q 1nd -J  job-data-" + str(count) + " < jobs_data/job-" + str(count) + ".sh"
	os.system(bashstring)
	count += 1
