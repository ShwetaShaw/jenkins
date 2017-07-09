import requests
import json
from threading import Thread
import threading
import jenkinProperty
import time


class AppThread(Thread):

    def __init__(self, threadNo, listOfApp):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.listOfApp = listOfApp

    def getVersion(self, app):
    	url = "http://likhesh:likhesh@localhost:8080/job/"+app.appName+"/lastStableBuild/api/json"
        response = requests.get(url);
        content = json.loads(response.content)
        parameters = content['actions'][0]['parameters']
        for parameter in parameters:
            paramName = parameter['name']
            if (paramName == 'version'):
                lastSuccessBuildVersion = parameter['value']
                print 'version is ', lastSuccessBuildVersion
                break

        print 'final version is ', lastSuccessBuildVersion

        buildNumberPostfix = "-1";
        versionToUse = app.initialVersion + buildNumberPostfix;

        appVersion = app.initialVersion;
        if lastSuccessBuildVersion and lastSuccessBuildVersion.startswith(appVersion):
            lastIndex = lastSuccessBuildVersion.rfind("-");
            if lastIndex > 1:
	            buildNumber = lastSuccessBuildVersion[lastIndex+1:]
	            print "LAST", lastSuccessBuildVersion
	            print "BUILD", buildNumber
	            buildNumber = int(buildNumber) + 1;
	            buildNumberPostfix = '-' + str(buildNumber)
	            print 'buildNumber ', buildNumber
	            versionToUse = appVersion + buildNumberPostfix
        print versionToUse
        return versionToUse

    def constructBuildAPIURL(self, appname, branch, version):
    	url = jenkinProperty.jenkinsSchema + jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort;
    	url = url + "/job/"+appname+"/buildWithParameters?token="+jenkinProperty.apiToken+"&version="+version+"&branch="+branch
    	return url

    def run(self):
    	print self.threadNo

    	for app in self.listOfApp:
    		print self.threadNo
    		print app.branchName
	    	headers={"Jenkins-Crumb": jenkinProperty.jenkinCrumb}
	    	print "Start Building"
	    	version = self.getVersion(app)

	        url = self.constructBuildAPIURL(app.appName, app.branchName, version)
	        # "http://"+jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort+"/job/"+app.appName+"/buildWithParameters?token=KK044zgm0POwZK5zm4IMf2upUbIDnfy8&version="+app.initialVersion+"&branch="+app.branchName
	        print 'api url is ', url 
	        requests.post(url, headers=headers)
	        time.sleep(jenkinProperty.pollingTime)
	        print "Start Polling"
	        url = "http://"+jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort+"/job/"+app.appName+"/lastBuild/api/json"
	        response = requests.get(url, headers=headers)
	        content = json.loads(response.content)
	        # print "lastBuild response ", content
	        building = content['building']
	        result = content['result']
	        print "build ", building
	        print "result ", result

	        while building == True:
	            time.sleep(jenkinProperty.pollingTime)
	            url = "http://"+jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort+"/job/"+app.appName+"/lastBuild/api/json"
	            response = requests.get(url)
	            content = json.loads(response.content)
	            building = content['building']
	            result = content['result']

	            print "build ", building
	            print "result ", result


	        # print "final result ", result
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


with open('dep.json') as data_file:    
    data = json.load(data_file)

parallel = []

for majorkeys, subdict in data.iteritems():
	sequential = []
	for subkeys, value in subdict.iteritems():
		test = App(value["appName"], value["branchName"], value["initialVersion"])
		sequential.append(test)
	parallel.append(sequential)

temp = 0
for i in parallel:
	t = AppThread(temp,i)
	t.start()
	temp += 1

