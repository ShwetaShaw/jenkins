import requests
import json
from threading import Thread

class MyThread(Thread):
 
    def __init__(self, threadNo, appName, branchName, appVersion, processType):
        Thread.__init__(self)
        self.threadNo = threadNo
        self.appName = appName
        self.appVersion = appVersion
        self.branchName = branchName
        self.processType = processType
 
    def run(self):
    	headers={"Jenkins-Crumb": "482a316e3c5d692a6de169bfd79a0a39"}
    	if self.processType == 'BUILD':
            print "Start building"+ self.appName
    	    url = "http://likhesh:likhesh@localhost:8080/job/"+self.appName+"/buildWithParameters?token=f3170516237a695411f696ad78fd0c&branchName="+self.branchName
            requests.post(url, headers=headers)
         
class App:

   def __init__(self, appName, appVersion, initialVersion):
      self.appName = appName
      self.appVersion = appVersion
      self.initialVersion = initialVersion

   def displayDetails(self):
      print "Name : ", self.appName,  ", Version: ", self.appVersion


sequentialApp1 = []
sequentialApp2 = []
parallelApp = []
app1 = App("tms-auth", "release/3.0.0","3.0.0-SNAPSHOT")
sequentialApp1.append(app1)
app2 = App("tms-ui", "release/3.0.0","3.0.0-SNAPSHOT")
sequentialApp1.append(app2)
app3 = App("ext-catalog","develop","1.3.4-SNAPSHOT")
sequentialApp2.append(app3)
app4 = App("ext-catalog-ui","develop","1.3.4-SNAPSHOT")
sequentialApp2.append(app4)

parallelApp.append(sequentialApp1)
parallelApp.append(sequentialApp2)

# parallelApp[0][0].displayDetails()


thread1 = MyThread(1,"tms-auth","release/3.0.0","3.0.0-SNAPSHOT","BUILD")
thread2 = MyThread(1,"tms-ui","release/3.0.0","3.0.0-SNAPSHOT","BUILD")

thread1.start()
thread2.start()

# i = 0
# for applist in parallelApp:
# 	url = "http://likhesh:likhesh@localhost:8080/job/"+applist[i].appName+"/buildWithParameters?token=f3170516237a695411f696ad78fd0c&branchName="+applist[i].appVersion
# 	requests.post(url, headers=headers)
# 	i += 1

# for applist in parallelApp:
# 	url = "http://likhesh:likhesh@localhost:8080/job/"+applist[i].appName+"/lastBuild/api/json"
# 	response = requests.post(url, headers=headers)

	









# headers={"Jenkins-Crumb": "482a316e3c5d692a6de169bfd79a0a39"}
# requests.post("http://likhesh:likhesh@localhost:8080/job/tms-auth/buildWithParameters?token=f3170516237a695411f696ad78fd0c&branchName=release/3.0.0&repoName=tms/authentication.git", headers=headers)

