# Version: 1.1, changed JSON folder
# Date: 6/27/2019
#
# This script will do the following:
# 1. Prompt to create a new case or use an existing one
# 2. Prompt for a target
# 3. Collect volatile data from that target, according to the external definition
# 4. Rename the XML files with the results, for outside viewing
# 5. Import the collected volatile data into the case
#
# IMPORTANT:
# EntAPICommon.py must reside in the same folder as this script.
# Make sure to update variables at the top
# The account running this script must have full access to the path in ProjectData

import os
import time
from datetime import datetime
from shutil import copyfile
import EntAPICommon

# UPDATE THESE
ProjectDataPath = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData" # Default case data path, make sure to escape any backslashes
CreateCaseDefinitionJSON = "createcaseDefinition.json" # JSON file with the operation definition settings to use
VolatileDefinitionJSON = "volatileDefinition.json" # JSON file with the operation definition settings to use

ScriptFolder = os.path.abspath(os.path.dirname(__file__))
CreateCaseDefinitionFile = os.path.join(ScriptFolder, "Operation Definitions", CreateCaseDefinitionJSON)
VolatileDefinitionFile = os.path.join(scriptfolder, "Operation Definitions", VolatileDefinitionJSON)

# Connection test
if not EntAPICommon.IsApiUp():
  os.system("pause")
  raise SystemExit

# Prompt for case to process into
print()
choice = ''
while choice not in ['1','2']:
  print("Choose from the following:")
  print("1 - Create a new case")
  print("2 - Use an existing case")
  choice = input("Enter 1 or 2: ")
  if choice not in ['1','2']:
    print("Invalid selection!")

if choice == '1':
  # Prompt for a case name
  print()
  print("Case data will be stored at '%s'" % ProjectDataPath)
  CaseName = input("Enter your desired case name: ")

  # Create the case and get the CaseID
  print()
  print("Creating case '%s'..." % CaseName)
  ProjectDataPath = ProjectDataPath + "\\" + CaseName
  JobDataPath = ProjectDataPath + "\\JobData"
  ReportsPath = ProjectDataPath + "\\Reports"

  if not os.path.exists(ProjectDataPath):
    os.makedirs(ProjectDataPath)

  createcaseDefinition = EntAPICommon.FileToJSON(CreateCaseDefinitionFile)
  createcaseDefinition["name"] = CaseName
  createcaseDefinition["ftkCaseFolderPath"] = ProjectDataPath
  createcaseDefinition["responsiveFilePath"] = JobDataPath
  createcaseDefinition["processingMode"] = 2

  CaseID = EntAPICommon.CreateCase(createcaseDefinition)
  print("Case ID: %s" % CaseID)
  print("Project folder: %s" % ProjectDataPath)
elif choice == '2':
  print()
  CaseID = int(input("Enter the desired case's Case ID: "))
  # Get information about an existing case
  exists = 0
  cases= EntAPICommon.GetCaseList()
  for case in cases:
    if case["id"] == CaseID:
      exists = 1
      casename = case["name"]
      casepath = case["casePath"]
      break
  if exists == 0:
    print("No such case exists")
    os.system("pause")
    raise SystemExit
  else:
    print("Using case '%s'" % casename)
    print("Project folder: %s" % casepath)
    ReportsPath = os.path.dirname(casepath) + "\\Reports"

# Prompt you for a target IP
# TODO: Can we do comma separated values, hostname, IP range, host name, or import a list from  a TXT file?
# TODO: Push the Agent
print()
targets = input("Enter the desired target's IP: ")

# Check if 3999 is listening on target
if not EntAPICommon.IsPortListening(str(targets), 3999):
  os.system("pause")
  raise SystemExit

# Grab the operation definition and update it with our targets, then kick off the job
volatileDefinition = EntAPICommon.FileToJSON(VolatileDefinitionFile)
volatileDefinition["volatile"]["includeProcessTree"] = True
volatileDefinition["volatile"]["includeServices"] = True
volatileDefinition["ips"]["targets"] = [str(targets)]
JobID = EntAPICommon.VolatileJob(CaseID, volatileDefinition)

print()
# Poll the job status
jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
state = jobinfo["state"]

while (state in ["InProgress", "Submitted"]):
  print("Job %s is %s. Will check again in 1 minute." % (JobID,state))
  time.sleep(60)
  jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
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

# Place XML results in an easily accessible place
print()
print("Fetching result reports.")
print(EntAPICommon.CopyJobReports(CaseID, JobID, ReportsPath))

# Import collected data into the case
print()
print("Adding volatile data to the case")
print(EntAPICommon.AddVolatile(CaseID, JobID))

os.system("pause")

# Ability to schedule scans in the script. Run X times every X mins/secs/hours
# Would be cool if we could perform a delta of the scans automatically.
# Deleted the agent when done.,