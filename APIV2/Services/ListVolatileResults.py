import requests
import json
import chardet
import time
from datetime import datetime
import EntAPICommon

APIkey = '6400ddd5-6419-450a-b96c-a568f5ea309b'
APIhostname = 'WIN-B3VKJBVM6RQ'
JobID = 51
CaseID = 53

jobinfo = EntAPICommon.GetJobInfo(APIkey, APIhostname, CaseID, JobID)
print("state: %s" % jobinfo["state"])
print("startDate: %s" % jobinfo["startDate"])
print("endDate: %s" % jobinfo["endDate"])
# Get the Target and list of ResultFiles from the job info
# target = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Details"]["Name"]
# print(target)
# resultfiles = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Results"][1]["Data"]["ResultFiles"]
# print(resultfiles)