# Version: 1.1, polls and reports processing progress
# Date: 8/28/2019
#
# In Windows Explorer, drag-and-drop a set of files onto this script's icon
# This script will do the following:
# 1. Prompt to create a new case or use an existing one
# 2. Attempt to identify the type of evidence dropped on the script
# 3. Process the evidence into the specified case
#
# Items dropped on this script must belong to ONE of the following categories:
# - The first segment of a forensic image file
# - Any number of native files
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
import sys
import ast
from commonVars import *

# UPDATE THESE
ProcessingProfileXML = "ForensicProcessing.xml" # XML file with the full processing options desired
CreateCaseDefinitionJSON = "createcaseDefinition.json" # JSON file with the operation definition settings to use

ProjectDataPath = os.path.normpath(ProjectDataPath)
ScriptFolder = os.path.abspath(os.path.dirname(__file__))
ProcessingProfileFile = os.path.join(ScriptFolder, "Processing Profiles", ProcessingProfileXML)
CreateCaseDefinitionFile = os.path.join(ScriptFolder, "Operation Definitions", CreateCaseDefinitionJSON)

if len(sys.argv) == 1:
  print("Usage:")
  print("In Windows Explorer, drag-and-drop a set of files to process onto this script's icon")
  print("Supported file types:")
  print("- First segment of a forensic image")
  print("- Any number of native files")
  print("- A folder of native files")
  print("Note: The Processing Engine must have access to all paths listed.")
  os.system("pause")
  raise SystemExit

# Connection test
if not EntAPICommon.IsApiUp():
  os.system("pause")
  raise SystemExit

# Make sure project path in UNC
if not EntAPICommon.IsUNC(ProjectDataPath):
  os.system("pause")
  raise SystemExit

# Grab a list of all the item dropped onto the script
print()
items = []
for i in range(1,len(sys.argv)):
  if EntAPICommon.IsUNC(sys.argv[i]):
    items.append(sys.argv[i])
  else:
    os.system("pause")
    raise SystemExit
# Sort for easier to read output
items.sort()

print("Items to process: ")
for item in items:
  print(item)

print()
print("Please review the items listed before continuing.")
print("Supported file types:")
print("- First segment of a forensic image")
print("- Individual native files")
print("- A folder of native files")
print("Note: The Processing Engine must have access to all paths listed.")
os.system("pause")

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
    CaseName = casename
    print("Using case '%s'" % CaseName)
    print("Project folder: %s" % casepath)
    ReportsPath = os.path.dirname(casepath) + "\\Reports"

# Iterate through all input paths
# If we detect a first image segment, we'll process its image
# Otherwise, treat everything as natives
print()
completeProcessingOptions = EntAPICommon.FileToString(ProcessingProfileFile)
for item in items:
  EvidenceType = EntAPICommon.DetectEvidenceType(item)
  if EvidenceType == 2:
    definition = {
      "evidenceToCreate": {
        "evidenceType": EvidenceType,
        "evidencePath": item
      },
      "completeProcessingOptions": completeProcessingOptions
    }
    print("Started processing image '%s'" % item)
    JobID = EntAPICommon.AddEvidence(CaseID, definition)

    # Clean up the Job ID
    JobID = ast.literal_eval(JobID)
    JobID = JobID[0]     

    print()
    # Poll the job status
    jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
    state = jobinfo["state"]

    while (state in ["InProgress", "Submitted"]):
      print("Job %s is %s. Will check again in 1 minute." % (JobID,state))
      time.sleep(60)
      jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
      state = jobinfo["state"]
    if state == "Completed":
      print("Processing job %s is %s." % (JobID,state))
    else:
      print("Processing job %s experienced an error and cannot proceed." % JobID)
      os.system("pause")
      raise SystemExit   
  elif EvidenceType == 0:
    definition = {
      "evidenceToCreate": {
        "evidenceType": EvidenceType,
        "evidencePath": item
      },
      "completeProcessingOptions": completeProcessingOptions
    }
    print("Started processing native '%s'" % item)
    JobID = EntAPICommon.AddEvidence(CaseID, definition)

    # Clean up the Job ID
    JobID = ast.literal_eval(JobID)
    JobID = JobID[0]    

    print()
    # Poll the job status
    jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
    state = jobinfo["state"]

    while (state in ["InProgress", "Submitted"]):
      print("Job %s is %s. Will check again in 1 minute." % (JobID,state))
      time.sleep(60)
      jobinfo = EntAPICommon.GetJobInfo(CaseID, JobID)
      state = jobinfo["state"]
    if state == "Completed":
      print("Processing job %s is %s." % (JobID,state))
    else:
      print("Processing job %s experienced an error and cannot proceed." % JobID)
      os.system("pause")
      raise SystemExit   
  else:
    print("I do not know how to handle '%s'." % item)

print("The processed evidence can now be reviewed in case '%s" % CaseName)
os.system("pause")
