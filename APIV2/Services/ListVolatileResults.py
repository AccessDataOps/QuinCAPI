import requests
import base64
import json
import chardet
import time
from datetime import datetime
from CleanVolatileResponse import CleanResponse

APIkey = '6400ddd5-6419-450a-b96c-a568f5ea309b'
APIhostname = 'WIN-B3VKJBVM6RQ'
JobID = 27
CaseID = 39

headers = {'EnterpriseApiKey': APIkey}
resp = requests.get('http://'+APIhostname+':4443/api/v2/enterpriseapi/'+str(CaseID)+'/getjobstatus/'+str(JobID),headers = headers)
data = CleanResponse(resp.content)

if (data["state"] == "Completed"):
    print("Job %s in Case %s" % (JobID, CaseID))
    print("-"*35)
    starttime = datetime.strptime(data["startDate"], '%Y-%m-%dT%H:%M:%S.%f')
    endtime = datetime.strptime(data["endDate"], '%Y-%m-%dT%H:%M:%S.%f')
    print("Start Time: %s UTC" % starttime.strftime("%m/%d/%Y %H:%M:%S"))
    print("End Time: %s UTC" % endtime.strftime("%m/%d/%Y %H:%M:%S"))

    # Parse the ResultFiles section of the output, and the target
    resultfiles = data["resultData"]["RealData"]["TaskStatusList"][0]["Results"][1]["Data"]["ResultFiles"]
    target = data["resultData"]["RealData"]["TaskStatusList"][0]["Results"][0]["Data"]["taskStatus"]["Connection"]

    # Print the results
    print()
    print("Results")
    print("-"*35)
    for i in range(0,len(resultfiles)):
        if (resultfiles[i]["Filename"] != "certificates.xml"):
            print("Target: %s" % target)
            for key,value in resultfiles[i].items():
                print("%s: %s" % (key,value))
            print()

else:
    print("Job status is %s" % data["state"])