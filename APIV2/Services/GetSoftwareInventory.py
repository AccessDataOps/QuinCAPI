# Version: .4
# Date: 5/17/2019
#
# This script will do the following:
# 1. Prompt to create a new case or use an existing one
# 2. Prompt for a target
# 3. Collect software inventory from that target, according to the external definition
# 4. Rename the XML files with the results, for outside viewing
#
# IMPORTANT:
# EntAPICommon.py must reside in the same folder as this script.
# Make sure to update the APIkey, APIhostname, and ProjectData
# The account running this script must have full access to the path in ProjectData
# To use existing cases, Enterprise must be using MSSQL and the account running this script needs MSSQL access

import os
import time
from datetime import datetime
from shutil import copyfile
import EntAPICommon

# UPDATE THESE
APIkey = "84af3650-176a-4edf-bad8-25ad5b708f37" # Generated in Enterprise via Tools > Access API Key
APIhostname = "WIN-B3VKJBVM6RQ" # Machine (name or IP) running Enterprise and Quin-C Self Host Service
ProjectDataPath = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData" # Default case data path, make sure to escape any backslashes
CreateCaseDefinitionFile = "C:\\Users\\svc\\Desktop\\scripts\\Services\\createcaseDefinition.json" # File with the definition settings to use
SoftwareInventoryDefinitionFile = "C:\\Users\\svc\\Desktop\\scripts\\Services\\softwareinventoryDefinition.json" # File with the definition settings to use

# Connection test
if EntAPICommon.IsApiUp(APIhostname):
    print("OK")
else:
    print("Failed")
    print("Check the 'Quin-C Self Host Service' on %s" % APIhostname)
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
    # TODO: Get the CaseID for an existing case
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

    CaseID = EntAPICommon.CreateCase(APIkey, APIhostname, createcaseDefinition)
    print("Case ID: %s" % CaseID)
    print("Project folder: %s" % ProjectDataPath)
elif choice == '2':
    print()
    CaseID = input("Enter the desired case's Case ID: ")
    # TODO: Check if Case ID exist
    # TODO: Use case name to get case id
    # Get the project folder from MSSQL
    InstanceName = 'WIN-B3VKJBVM6RQ'
    DatabaseName = 'ADG'
    Query = 'SELECT CasePath FROM [ADG].[ADG7x1].[cmn_Cases] WHERE CaseID = %s' % CaseID
    results = EntAPICommon.QueryMSSQL(InstanceName, DatabaseName, Query)
    CasePath = results[0]["CasePath"]
    ReportsPath = os.path.dirname(CasePath) + "\\Reports"

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

# Grab the operation definition and update it with our targets, then kick off the job
softwareinventoryDefinition = EntAPICommon.FileToJSON(SoftwareInventoryDefinitionFile)
softwareinventoryDefinition["ips"]["targets"] = [str(targets)]
JobID = EntAPICommon.SoftwareInventoryJob(APIkey, APIhostname, CaseID, softwareinventoryDefinition)

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

# Place XML results in an easily accessible place
print()
print("Fetching result reports.")
print(EntAPICommon.CopyJobReports(APIkey, APIhostname, CaseID, JobID, ReportsPath))

os.system("pause")

# Ability to schedule scans in the script. Run X times every X mins/secs/hours
# Would be cool if we could perform a delta of the scans automatically.
# Deleted the agent when done.,