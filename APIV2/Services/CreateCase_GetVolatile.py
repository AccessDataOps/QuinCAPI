import requests
import base64
import json
from requests.exceptions import ConnectionError
import os
import chardet
import time
from datetime import datetime

# API connection info
APIkey = "6400ddd5-6419-450a-b96c-a568f5ea309b" # Generated in Enterprise via Tools > Access API Key
APIhostname = "WIN-B3VKJBVM6RQ" # Machine (name or IP) running Enterprise and Quin-C Self Host Service

headers = {'EnterpriseApiKey': APIkey}

# Connection test
print("Checking API status...")
try:
    status = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/statuscheck",headers = headers)
    print(status.reason)
except ConnectionError: # Nicer failure message than a full traceback
    print("Failed")
    print("Check the 'Quin-C Self Host Service' on %s" % APIhostname)
    raise SystemExit

# Default case data paths
ProjectData = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData"
JobData = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\JobData"

# Prompt for a case name
print()
CaseName = input("Enter your desired case name: ")

# Create the case and get the CaseID
# TODO: Get the CaseID for an existing case
print()
print("Creating case '%s'..." % CaseName)
ProjectData = ProjectData + "\\" + CaseName
JobData = JobData + "\\" + CaseName

if not os.path.exists(ProjectData):
    os.makedirs(ProjectData)

if not os.path.exists(JobData):
    os.makedirs(JobData)

createcaseDefinition = {
  "name": CaseName,
  "ftkCaseFolderPath": ProjectData,
  "responsiveFilePath": JobData,
  "processingMode": 2
}

resp = requests.post("http://" + APIhostname + ":4443/api/v2/enterpriseapi/createcase",createcaseDefinition,headers=headers)
print("Success")
CaseID = resp.content.decode("utf-8")
print("Case ID = %s" % CaseID)

# Prompt you for a target IP
# TODO: Can we do comma separated values, hostname, IP range, host name, or import a list from  a TXT file?
# TODO: Check if target is listening
# TODO: Push the Agent
print()
targets = input("Enter the desired target's IP: ")

# Grab Services
# TODO: include hidden processes, DLLs (including injected), Sockets, Handles, Services, Drivers, Users, and Network info
volatileDefinition = {
  "volatile": {
    "includeProcessTree": True,
    "includeServices": True
  },
  "ips": {
    "targets": [
      str(targets)
    ]
  }
}

resp = requests.post("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/volatile",json = volatileDefinition,headers=headers)
JobID = resp.content.decode("utf-8")

# Get the job's official start time
resp = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/getjobstatus/"+str(JobID),headers = headers)
data = json.loads(resp.content.decode(chardet.detect(resp.content)["encoding"]))
print()

# Poll the job status
while (data["state"] == "InProgress") or (data["state"] == "Submitted"):
    print("Job %s is %s.  Will check again in 3 minutes." % (JobID,data["state"]))
    time.sleep(180)
    resp = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/getjobstatus/"+str(JobID),headers = headers)
    data = json.loads(resp.content.decode(chardet.detect(resp.content)["encoding"]))

print("Job %s is %s." % (JobID,data["state"]))

# List the XML files containing the job results
if (data["state"] == "Completed"):
    print("Results:")
    result = json.loads(data["resultData"])
    realdata = json.loads(result["RealData"])
    for i in range(0,len(realdata["TaskStatusList"][0]["Results"])):
        print(realdata["TaskStatusList"][0]["Results"][1]["ResultFileLocation"][i]["FilePath"])

# TODO: Output to XLS in a tabular format by IP and or info.
# Import into ENT GUI so the cust had historical data.
print()
print("Adding volatile data to the case")
resp = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/importvolatile/"+str(JobID),headers=headers)
print(resp)
print(resp.content)

# Ability to schedule scans in the script. Run X times every X mins/secs/hours
# Would be cool if we could perform a delta of the scans automatically.
# Deleted the agent when done.,
