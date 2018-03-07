import json

def grabRunInstanceInfo(fileName):
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
				
with open('RunInstances.list','r') as fileNames:
	for a in fileNames:
		b = a.strip("\n")
		grabRunInstanceInfo(b)
