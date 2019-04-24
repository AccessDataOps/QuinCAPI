# This script will do the following:
# 1. Prompt for a case name
# 2. Create the case
# 3. Prompt for a target
# 4. Collect volatile data from that target
# 5. Rename the XML files with the results, for outside viewing
# 6. Import the collected volatile data into the case
#
# Make sure to update the APIkey, APIhostname, and ProjectData
# The account running this script must have full access to the path in ProjectData

import requests
import base64
import json
from requests.exceptions import ConnectionError
import os
import chardet
import time
from datetime import datetime
from shutil import copyfile

# UPDATE THESE
APIkey = "6400ddd5-6419-450a-b96c-a568f5ea309b" # Generated in Enterprise via Tools > Access API Key
APIhostname = "WIN-B3VKJBVM6RQ" # Machine (name or IP) running Enterprise and Quin-C Self Host Service
ProjectData = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData" # Default case data path, make sure to escape any backslashes

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

# Prompt for a case name
print()
print("Case data will be stored at '%s'" % ProjectData)
CaseName = input("Enter your desired case name: ")

# Create the case and get the CaseID
# TODO: Get the CaseID for an existing case
print()
print("Creating case '%s'..." % CaseName)
ProjectData = ProjectData + "\\" + CaseName
Reports = ProjectData + "\\Reports"
JobData = ProjectData + "\\JobData"

if not os.path.exists(Reports):
    os.makedirs(Reports)

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
print(status.reason)
print()
CaseID = resp.content.decode("utf-8")
print("Case ID: %s" % CaseID)
print("Project folder: %s" % ProjectData)

# Prompt you for a target IP
# TODO: Can we do comma separated values, hostname, IP range, host name, or import a list from  a TXT file?
# TODO: Check if target is listening
# TODO: Push the Agent
print()
targets = input("Enter the desired target's IP: ")

# Grab Processes, Services, Network Sockets
# TODO: include hidden processes, DLLs (including injected), Sockets, Handles, Services, Drivers, Users, and Network info
volatileDefinition = {
  "volatile": {
    "includeProcessTree": True,
    "processTreeOptions": {
      "includeSockets": True
    },
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
    print("Job %s is %s.  Will check again in 1 minute." % (JobID,data["state"]))
    time.sleep(60)
    resp = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/getjobstatus/"+str(JobID),headers = headers)
    data = json.loads(resp.content.decode(chardet.detect(resp.content)["encoding"]))

print("Job %s is %s." % (JobID,data["state"]))

# Parse the ResultFiles section of the output, and the target
resultfiles = json.loads(json.loads(json.loads(data["resultData"])["RealData"])["TaskStatusList"][0]["Results"][1]["Data"])["ResultFiles"]
target = json.loads(json.loads(json.loads(data["resultData"])["RealData"])["TaskStatusList"][0]["Results"][0]["Data"])["taskStatus"]["Connection"]

# Build a list of the result XML files
tasks = []
for i in range(0,len(resultfiles)):
    if (resultfiles[i]["Filename"] != "certificates.xml"): # We don't care about this file
        tasks.append({"Target": target, "Path": resultfiles[i]["Path"], "Filename": resultfiles[i]["Filename"]})

# Copy the result XML files to a nicer location and name
starttime = datetime.strptime(data["startDate"], '%Y-%m-%dT%H:%M:%S.%f')
for i in range(0,len(tasks)):
    src = tasks[i]["Path"]
    dst = "%s\\%s_%s_%s" % (Reports,tasks[i]["Target"],starttime.strftime("%Y%m%d %H%M%SUTC"),tasks[i]["Filename"])
    copyfile(src,dst)

print()
print("XML reports can be found in '%s'" % Reports)
print("These can be opened with Excel.")

# Import collected data into the case
print()
print("Adding volatile data to the case")
resp = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/"+str(CaseID)+"/importvolatile/"+str(JobID),headers=headers)
print(status.reason)


# Ability to schedule scans in the script. Run X times every X mins/secs/hours
# Would be cool if we could perform a delta of the scans automatically.
# Deleted the agent when done.,
