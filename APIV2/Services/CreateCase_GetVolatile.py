# Version: .4, check target listening, report job failure, pause at the end
# Date: 4/29/2019
#
# This script will do the following:
# 1. Prompt for a case name
# 2. Create the case
# 3. Prompt for a target
# 4. Collect volatile data from that target
# 5. Rename the XML files with the results, for outside viewing
# 6. Import the collected volatile data into the case
#
# IMPORTANT:
# EntAPICommon.py must reside in the same folder as this script.
# Make sure to update the APIkey, APIhostname, and ProjectData
# The account running this script must have full access to the path in ProjectData

import os
import time
from datetime import datetime
from shutil import copyfile
import EntAPICommon

# UPDATE THESE
APIkey = "6400ddd5-6419-450a-b96c-a568f5ea309b" # Generated in Enterprise via Tools > Access API Key
APIhostname = "WIN-B3VKJBVM6RQ" # Machine (name or IP) running Enterprise and Quin-C Self Host Service
ProjectData = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData" # Default case data path, make sure to escape any backslashes

# Connection test
if EntAPICommon.IsApiUp(APIhostname):
    print("OK")
else:
    print("Failed")
    print("Check the 'Quin-C Self Host Service' on %s" % APIhostname)
    os.system("pause")
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

if not os.path.exists(ProjectData):
    os.makedirs(ProjectData)

if not os.path.exists(Reports):
    os.makedirs(Reports)

if not os.path.exists(JobData):
    os.makedirs(JobData)

createcaseDefinition = {
  "name": CaseName,
  "ftkCaseFolderPath": ProjectData,
  "responsiveFilePath": JobData,
  "processingMode": 2
}

CaseID = EntAPICommon.CreateCase(APIkey, APIhostname, createcaseDefinition)
print("Case ID: %s" % CaseID)
print("Project folder: %s" % ProjectData)

# Prompt you for a target IP
# TODO: Can we do comma separated values, hostname, IP range, host name, or import a list from  a TXT file?
# TODO: Push the Agent
print()
targets = input("Enter the desired target's IP: ")

# Check if 3999 is listening on target
if not EntAPICommon.IsPortListening(str(targets), 3999):
  print("Target isn't responding on port 3999. Check Agent service on '%s'" % str(targets))
  os.system("pause")
  raise SystemExit

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

JobID = EntAPICommon.VolatileJob(APIkey, APIhostname, CaseID, volatileDefinition)

print()
# Poll the job status
jobinfo = EntAPICommon.GetJobInfo(APIkey, APIhostname, CaseID, JobID)
state = jobinfo["state"]

while (state in ["InProgress", "Submitted"]):
  print("Job %s is %s. Will check again in 1 minute." % (JobID,state))
  time.sleep(60)
  jobinfo = EntAPICommon.GetJobInfo(APIkey, APIhostname, CaseID, JobID)
  state = jobinfo["state"]
try:
  RealState = jobinfo["resultData"]["RealData"]["State"]
except KeyError:
  print("Job %s experienced an error and cannot proceed." % JobID)
  os.system("pause")
  raise SystemExit
if RealState == "Finished":
  print("Job %s is %s." % (JobID,state))
else:
  print("Job %s experienced an error and cannot proceed." % JobID)
  os.system("pause")
  raise SystemExit

# Get the Target Name and list of ResultFiles from the job info
target = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Details"]["Name"]
resultfiles = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Results"][1]["Data"]["ResultFiles"]

# Build a list of the result XML files
tasks = []
for i in range(0,len(resultfiles)):
    if (resultfiles[i]["Filename"] != "certificates.xml"): # We don't care about this file
        tasks.append({"Target": target, "Path": resultfiles[i]["Path"], "Filename": resultfiles[i]["Filename"]})

# Copy the result XML files to a nicer location and name
starttime = datetime.strptime(jobinfo["startDate"], '%Y-%m-%dT%H:%M:%S.%f') # Parse the job info timestamp to something Python understands
for i in range(0,len(tasks)):
    src = tasks[i]["Path"]
    dst = "%s\\%s_%s_%s" % (Reports,tasks[i]["Target"],starttime.strftime("%Y%m%d%H%M%SUTC"),tasks[i]["Filename"])
    copyfile(src,dst)

print()
print("XML reports can be found in '%s'" % Reports)
print("These can be opened with Excel.")

# Import collected data into the case
print()
print("Adding volatile data to the case")
print(EntAPICommon.AddVolatile(APIkey, APIhostname, CaseID, JobID))

os.system("pause")

# Ability to schedule scans in the script. Run X times every X mins/secs/hours
# Would be cool if we could perform a delta of the scans automatically.
# Deleted the agent when done.,
