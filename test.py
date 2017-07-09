import requests
import json
from threading import Thread
import threading
import time

noOfThread = 2

class AppThread(Thread):

    def __init__(self, threadNo, appName, branchName, appVersion):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.appName = appName
        self.appVersion = appVersion
        self.branchName = branchName

    def setAppName(self, appName):
    	self.appName = appName 

    def setBranchName(self, branchName):
    	self.branchName = branchName

    def setAppVersion(self, appVersion):
    	self.appVersion = appVersion 

    def displayThreadDetails(self):
		print "AppName : ", self.appName,  ", BranchName: ", self.branchName,  ", Version: ", self.appVersion

 
    def run(self):
    	headers={"Jenkins-Crumb": "8caec0e2fd3b0793f98d83fc506a2f15"}
        print "Start building "+ self.appName
        url = "http://lrathod:lrathod@localhost:8080/job/"+self.appName+"/buildWithParameters?token=KK044zgm0POwZK5zm4IMf2upUbIDnfy8&version="+self.appVersion+"&branch="+self.branchName
        requests.post(url, headers=headers)
        #if self.processType == 'POLL':
        print "Start polling "+ self.appName
        url = "http://lrathod:lrathod@localhost:8080/job/"+self.appName+"/lastBuild/api/json"
        response = requests.post(url, headers=headers)
        content = json.loads(response.content)
        print "lastBuild response ", content
        building = content['building']
        result = content['result']
        time.sleep(5)
        print "build ", building
        print "result ", result

        while building == True:
            time.sleep(5)
            url = "http://lrathod:lrathod@localhost:8080/job/"+self.appName+"/lastBuild/api/json"
            response = requests.get(url)
            content = json.loads(response.content)
            building = content['building']
            result = content['result']

            print "build ", building
            print "result ", result


        print "final result ", result
            #while 
            #building = res[buildLength + 10 : buildLength + 11]
            #result = res[resultLength + 9 : resultLength + 10]
            # if building == "t":
            # 	threading.Timer(30.0, checkThreadState(building, result, self.url, headers)).start()
            # 	buildingFinished = checkThreadState(building, result,self.appName)
            # 	print "Building Finish :" + buildingFinished


       
         
class App(object):

	def __init__(self, appName, branchName, initialVersion):
		self.appName = appName
		self.branchName = branchName
		self.initialVersion = initialVersion

	def displayDetails(self):
		print "AppName : ", self.appName,  ", BranchName: ", self.branchName,  ", Version: ", self.initialVersion


buildAndDeployThread1 = AppThread(1,"","","")
buildAndDeployThread2 = AppThread(2,"","","")
pollThread = AppThread(3,"","","")

# thread2 = AppThread(2,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","BUILD")

with open('dep.json') as data_file:    
    data = json.load(data_file)

parallel = []

builtFlag = []

for majorkeys, subdict in data.iteritems():
	sequential = []
	for subkeys, value in subdict.iteritems():
		test = App(value["appName"], value["branchName"], value["initialVersion"])
		sequential.append(test)
		flag = []
		flag.append(test.appName)
		flag.append(False)
		builtFlag.append(flag)
	parallel.append(sequential)

for i in parallel:
	for j in i:
		if buildAndDeployThread1.isAlive() == 'FALSE':
			buildAndDeployThread1.setAppName(j.appName)
			buildAndDeployThread1.setAppVersion(j.appVersion)
			buildAndDeployThread1.setBranchName(j.branchName)



# def checkThreadState(building,result,url,header):
# 	print "Timer Running every 10 secs"
# 	print building
# 	print url
# 	response = requests.post(url, headers=header)
# 	print response
# 	res = response.content
# 	length = len(res)
# 	buildLength = res.find("building")
#    	building = res[buildLength + 10 : buildLength + 11]
#     print building
#     if building != "t":
#     	return true

# parallelApp[0][0].displayDetails()


thread1 = AppThread(1,"ext-catalog-ui","develop","3.0.1-1")
# thread2 = MyThread(1,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","BUILD")

thread1.start()
# thread2.start()

# thread3 = MyThread(1,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","POLL")
# thread3.start()
