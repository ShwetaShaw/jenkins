import requests
import json
from threading import Thread
import threading

noOfThread = 2

class AppThread(Thread):

    def __init__(self, threadNo, appName, branchName, appVersion, processType):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.appName = appName
        self.appVersion = appVersion
        self.branchName = branchName
        self.processType = processType

    def setAppName(self, appName):
    	self.appName = appName 

    def setBranchName(self, branchName):
    	self.branchName = branchName

    def setAppVersion(self, appVersion):
    	self.appVersion = appVersion 

    def setProcessType(self, processType):
    	self.processType = processType

    def displayThreadDetails(self):
		print "AppName : ", self.appName,  ", BranchName: ", self.branchName,  ", Version: ", self.appVersion, ", ProcessType: ", self.processType

 
    def run(self):
    	headers={"Jenkins-Crumb": "482a316e3c5d692a6de169bfd79a0a39"}
    	if self.processType == 'BUILD':
            print "Start building "+ self.appName
    	    url = "http://likhesh:likhesh@localhost:8080/job/"+self.appName+"/buildWithParameters?token=f3170516237a695411f696ad78fd0c&branchName="+self.branchName
            requests.post(url, headers=headers)
        if self.processType == 'POLL':
            print "Start polling "+ self.appName
            url = "http://likhesh:likhesh@localhost:8080/job/"+self.appName+"/lastBuild/api/json"
            response = requests.post(url, headers=headers)
            res = response.content
            length = len(res)
            buildLength = res.find("building")
            resultLength = res.find("result")
            building = res[buildLength + 10 : buildLength + 11]
            result = res[resultLength + 9 : resultLength + 10]
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


buildAndDeployThread1 = AppThread(1,"","","","")
buildAndDeployThread2 = AppThread(2,"","","","")
pollThread = AppThread(3,"","","","")

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

# for i in parallel:
# 	for j in i:
# 		if buildAndDeployThread1.isAlive() == 'FALSE':
# 			buildAndDeployThread1.setAppName(j.appName)
# 			buildAndDeployThread1.setAppVersion(j.appVersion)
# 			buildAndDeployThread1.setBranchName(j.branchName)
# 			buildAndDeployThread1.setProcessType()



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


# thread1 = MyThread(1,"tms-auth","release/3.0.0","3.0.0-SNAPSHOT","BUILD")
# thread2 = MyThread(1,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","BUILD")

# thread1.start()
# thread2.start()

# thread3 = MyThread(1,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","POLL")
# thread3.start()
