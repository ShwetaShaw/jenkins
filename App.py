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
        url = self.constructPollAPIURL(app.appName)
        print 'Poll API URL ', url
        response = requests.get(url);
        buildNumberPostfix = "-1";
        #print 'response', response.content
        versionToUse = app.initialVersion + buildNumberPostfix;
        if response:
            content = json.loads(response.content)
            #parameters = content['actions'][0]['parameters']
            actions = content['actions']
            for action in actions:
                #print 'action', action
                if action.get('parameters') == None:
                    continue
                parameters = action['parameters']
                #print 'parameters', parameters
                if parameters:
                    for parameter in parameters:
                        paramName = parameter['name']
                        if (paramName == 'version'):
                            lastSuccessBuildVersion = parameter['value']
                            #print 'version is ', lastSuccessBuildVersion
                            break
                    print 'lastSuccessBuildVersion version is ', lastSuccessBuildVersion
                    appVersion = app.initialVersion;
                    if lastSuccessBuildVersion and lastSuccessBuildVersion.startswith(appVersion):
                        lastIndex = lastSuccessBuildVersion.rfind("-");
                        if lastIndex > 1:
                            buildNumber = lastSuccessBuildVersion[lastIndex+1:]
                            #print "LAST", lastSuccessBuildVersion
                            #print "BUILD", buildNumber
                            buildNumber = int(buildNumber) + 1;
                            buildNumberPostfix = '-' + str(buildNumber)
                            #print 'buildNumber ', buildNumber
                            versionToUse = appVersion + buildNumberPostfix
                    break
        print 'version to use is for ', app.appName ,'is ', versionToUse
        return versionToUse

    def constructPollAPIURL(self, appname):
        url = jenkinProperty.jenkinsSchema + jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort;
        url = url + "/job/"+appname+"/lastStableBuild/api/json"
        return url

    def constructBuildAPIURL(self, appname, branch, version):
        url = jenkinProperty.jenkinsSchema + jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort;
        url = url + "/job/"+appname+"/buildWithParameters?token="+jenkinProperty.apiToken+"&version="+version+"&branch="+branch
        return url

    def constructDeployAPIURL(self, appname, version):
        url = jenkinProperty.jenkinsSchema + jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort;
        url = url + "/job/"+appname+"/buildWithParameters?token="+jenkinProperty.apiToken+"&version="+version
        return url

    def getDeployJobName(self, buildJobName):
        return buildJobName+"-deploy"

    def run(self):
        #print self.threadNo
        headers={"Jenkins-Crumb": jenkinProperty.jenkinCrumb}
        appsToDeploy = []
        for app in self.listOfApp:
            # print self.threadNo
            # print app.branchName
            # print "Start Building"
            version = self.getVersion(app)

            url = self.constructBuildAPIURL(app.appName, app.branchName, version)
            # print 'api url is ', url 
            requests.post(url, headers=headers)
            time.sleep(jenkinProperty.pollingTime)
            # print "Start Polling"
            url = "http://"+jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort+"/job/"+app.appName+"/lastBuild/api/json"
            response = requests.get(url, headers=headers)
            content = json.loads(response.content)
            # print "lastBuild response ", content
            building = content['building']
            result = content['result']
            # print "build ", building
            # print "result ", result
            global result1
            while building == True:
                global result1
                time.sleep(jenkinProperty.pollingTime)
                url = "http://"+jenkinProperty.userName+":"+jenkinProperty.password+"@"+jenkinProperty.jenkinsHost+":"+jenkinProperty.jenkinsPort+"/job/"+app.appName+"/lastBuild/api/json"
                response = requests.get(url)
                content = json.loads(response.content)
                building = content['building']
                result1 = content['result']

                # print "build ", building
                # print "result ", result1
            print "RESULT "+result1
            appDetails = []
            if result1 == 'SUCCESS':
                appDetails.append(version)
                appDetails.append(app.appName)
                appsToDeploy.append(appDetails)

        #Deploying
        i = 0
        for apps in appsToDeploy:
            print "Deploying"
            print self.getDeployJobName(apps[1])
            url = self.constructDeployAPIURL(self.getDeployJobName(apps[1]),apps[0])
            print url
            requests.post(url, headers=headers)
            i += 1


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

