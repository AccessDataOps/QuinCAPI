import requests
import json
import chardet
import time
from datetime import datetime
import EntAPICommon
import os

JobID = 28
CaseID = 13

JobDataPath = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\memory test 1"
jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)

resultfiles = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Results"][2]["ResultFileLocation"]
for resultfile in resultfiles:
        if resultfile["FilePath"].lower().endswith(('.ad1', '.mem')):
                myfile = resultfile["FilePath"]
                break

targetname = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Details"]["Name"]
starttime = datetime.strptime(jobinfo["startDate"], '%Y-%m-%dT%H:%M:%S.%f') # Parse the job info timestamp to something Python understands
newtime = starttime.strftime("%Y%m%d%H%M%SUTC")
jobresults = os.path.dirname(myfile)

for file in os.listdir(jobresults):
        ext = os.path.splitext(file)[1]
        oldname = os.path.join(jobresults,file)
        newname = os.path.join(JobDataPath,targetname + "_" + newtime + "_memdump" + ext)
        os.rename(oldname, newname)
