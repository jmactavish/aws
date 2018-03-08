import json
import os

def grabRunInstanceInfo(fileName):
	'filter out useful informations from the RunInstances field'
	with open(fileName) as logFile:
		log = json.load(logFile)
		eventsList = log['Records']
		for i in range(len(eventsList)):
			if eventsList[i]['eventName'] == 'RunInstances':
				runInstancesList = eventsList[i]
				for x in ["eventTime","eventName"]:
					print(runInstancesList[x])
				for y in ["instanceId","imageId","instanceType","privateIpAddress"]:
					print(runInstancesList["responseElements"]["instancesSet"]["items"][0][y])

fileList = []
for path, dir, fileNames in os.walk('s3CloudtrailBucketDir'):
	'list all json files recursively'
        for fileName in fileNames:
                if fileName.endswith(".json"):
                        file = os.path.join(path,fileName)
                        fileList.append(file)
for i in fileList:
	'same as "grep -r RunInstances *"'
        with open(i, 'r') as content:
                for line in content:
                        if 'RunInstances' in line:
				grabRunInstanceInfo(i)
