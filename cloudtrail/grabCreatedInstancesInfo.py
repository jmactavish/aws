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

s3CloudtrailBucketDir = raw_input('paste your path of logs here: ')
fileList = []
for path, dir, fileNames in os.walk(s3CloudtrailBucketDir):
        # list all json files recursively
        for fileName in fileNames:
                if fileName.endswith(".json"):
                        file = os.path.join(path,fileName)
                        fileList.append(file)
for i in fileList:
        # same as "grep -r RunInstances *"
        with open(i, 'r') as content:
                for line in content:
                        if 'RunInstances' in line:
                                print(i)
                                grabRunInstanceInfo(i)
                                print("\n")

