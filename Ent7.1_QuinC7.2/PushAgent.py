# Version: .1
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
import stdiomask

# UPDATE THESE
PublicCertificate = "C:\\Program Files\\AccessData\\Certificates\\CERBERUS_public.crt" # Full path to Agent public certificate
RunAgentPushDefinitionJSON = "runagentpushDefinition.json" # JSON file with the operation definition settings to use

ScriptFolder = os.path.abspath(os.path.dirname(__file__))
RunAgentPushDefinitionFile = os.path.join(ScriptFolder, "Operation Definitions", RunAgentPushDefinitionJSON)

# Connection test
if not EntAPICommon.IsApiUp():
  os.system("pause")
  raise SystemExit

# Prompt for a target IP
targets = input("Enter the desired target's IP: ")
print()
print("Please enter the credentials for an account with Administrator permissions on '%s'" % targets)
domain = input("Domain: ")
username = input("Username: ")
password = stdiomask.getpass()

runagentpushDefinition = EntAPICommon.FileToJSON(RunAgentPushDefinitionFile)
runagentpushDefinition["ips"]["targets"] = [str(targets)]
runagentpushDefinition["agentPush"]["credentials"][0]["domain"] = domain
runagentpushDefinition["agentPush"]["credentials"][0]["username"] = username
runagentpushDefinition["agentPush"]["credentials"][0]["password"] = password


print(runagentpushDefinition)

print(EntAPICommon.PushAgent(11, runagentpushDefinition))


os.system("pause")