import requests
import json
import chardet
import time
from datetime import datetime
import EntAPICommon

JobID = 25
CaseID = 13

jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
resultfiles = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Results"][2]["ResultFileLocation"]
for resultfile in resultfiles:
    if resultfile["FilePath"].lower().endswith(('.ad1', '.mem')):
        myfile = resultfile["FilePath"]
        break
print(myfile)