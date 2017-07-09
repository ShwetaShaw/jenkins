import requests
import json
from threading import Thread
import threading
import jenkinProperty


class AppThread(Thread):

    def __init__(self, threadNo, listOfApp):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.listOfApp = listOfApp

    def run(self):
    	print self.threadNo
    	print jenkinProperty.jenkinCrumb


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

