#!/user/bin/env python

intro = 'this script could recursively look for the [date, instanceId, specifications, IP, disk]  of created instances from gunzipped cloudtrail logs'

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
                                items = runInstancesList["responseElements"]["instancesSet"]["items"][0]
                                disks = runInstancesList['requestParameters']['blockDeviceMapping']['items']
                                if "tagSet" in items:
                                        print(items["tagSet"]["items"][0]["value"])
                                else:
                                	# some logs don't have instance tag in the "RunInstance" field since no tag was defined for those instances.
                                	# need to check their tags from other logs/behavior (just check the dictionary "instanceTags" which was just created)
                                        print(instanceTags[items["instanceId"]])
                                for x in ["eventTime","eventName"]:
                                        print(runInstancesList[x])
                                for y in ["instanceId","imageId","instanceType","privateIpAddress"]:
                                        print(items[y])
                                if "platform" in items:
                                        print(items["platform"])
                                for z in range(len(disks)):
                                        print(disks[z]['deviceName'])
                                        if 'ebs' in disks[z].keys():
                                                for a in ['volumeType','volumeSize']:
                                                        print(disks[z]['ebs'][a])
				print("terminate time: ")
				if items["instanceId"] in terminateFile:
					print(terminateTime[items["instanceId"]])
					print(terminateFile[items["instanceId"]])
					print('#########################################################')
				else:
					print('termination not recorded in this directory yet')
					print('#########################################################')

s3CloudtrailBucketDir = raw_input('paste your path of logs here: ')
print("\n")

# list all json files recursively
fileList = []
for path, dir, fileNames in os.walk(s3CloudtrailBucketDir):
        for fileName in fileNames:
                if fileName.endswith(".json"):
                        file = os.path.join(path,fileName)
                        fileList.append(file)

# find when the servers were terminated
terminateFile = {}
terminateTime = {}
for m in fileList:
	with open(m, 'r') as Logfile:
		LOG = json.load(Logfile)
		Eventslist = LOG['Records']	
                for n in range(len(Eventslist)):
                        if Eventslist[n]['eventName'] == 'TerminateInstances':
                                terminateInstancesList = Eventslist[n]
                                terminateFile[terminateInstancesList['requestParameters']['instancesSet']['items'][0]['instanceId']] = m
                                terminateTime[terminateInstancesList['requestParameters']['instancesSet']['items'][0]['instanceId']] = terminateInstancesList['eventTime']

# get server names from all logs and store them(values) in a dictionary with instance IDs(keys)
instanceTags = {}
for a in fileList:
        with open(a, 'r') as LogFile:
                Log = json.load(LogFile)
                EventsList = Log['Records']
                for b in range(len(EventsList)):
                        if EventsList[b]['eventName'] == 'CreateTags':
                                InstanceId = EventsList[b]['requestParameters']['resourcesSet']['items'][0]['resourceId']
                                instanceTags[InstanceId] = EventsList[b]['requestParameters']['tagSet']['items'][0]['value']

# same as "grep -r RunInstances *"
for i in fileList:
        with open(i, 'r') as content:
                for line in content:
                        if 'RunInstances' in line:
                                print(i)
                                grabRunInstanceInfo(i)
                                print("\n")

