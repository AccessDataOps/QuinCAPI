# In Windows Explorer, drag-and-drop a set of files onto this script's icon
# This script will do the following:
# 1. Prompt for a Case ID
# 2. Attempt to identify the type of evidence dropped on the script
# 3. Process the evidence into the specified case
#
# Items dropped on this script must belong to ONE of the following categories:
# - The first segment of one image file
# - All segments of one image file
# - Any number of native files
#
# IMPORTANT:
# EntAPICommon.py must reside in the same folder as this script.
# Make sure to update the APIkey and APIhostname.
# Files dropped on this script must either be segments of the same image, or individual natives.

import sys
import os
import EntAPICommon

# UPDATE THESE
APIkey = "6400ddd5-6419-450a-b96c-a568f5ea309b" # Generated in Enterprise via Tools > Access API Key
APIhostname = "WIN-B3VKJBVM6RQ" # Machine (name or IP) running Enterprise and Quin-C Self Host Service

# Connection test
if EntAPICommon.IsApiUp(APIhostname):
    print("OK")
else:
    print("Failed")
    print("Check the 'Quin-C Self Host Service' on %s" % APIhostname)
    os.system("pause")
    raise SystemExit

# Grab a list of all the item dropped onto the script
items = []
for i in range(1,len(sys.argv)):
    items.append(sys.argv[i])
# Sort so, if files are image segments, first segment is at the top
items.sort()

CaseID = input("Which case (case ID) would you like to add evidence to? ")
print("Items to process: ")
for item in items:
    print(item)

print()
print("Please review the items listed before continuing.")
print("If more than one file is listed, they must either be segments of the same image or individual natives.")
os.system("pause")

# Only check the evidence type of the first file
# If we detect a first image segment, we'll treat everything as an image
# Otherwise, treat everything as natives
EvidenceType = EntAPICommon.DetectEvidenceType(items[0])

if (EvidenceType == 2):
    definition = {
        "evidenceToCreate": {
            "evidenceType": EvidenceType,
            "evidencePath": items[0]
        }
    }
    print("Started processing image '%s'" % items[0])
    print(EntAPICommon.AddEvidence(APIkey, APIhostname, CaseID, definition))
    print("View progress by opening case %s and going to View > Progress Window" % CaseID)
elif (EvidenceType == 0):
    for item in items: 
        definition = {
            "evidenceToCreate": {
                "evidenceType": EvidenceType,
                "evidencePath": item
            }
        }
        print("Started processing native '%s'" % item)
        print(EntAPICommon.AddEvidence(APIkey, APIhostname, CaseID, definition))
    print("View progress by opening case %s and going to View > Progress Window" % CaseID)
else:
    print("I do not know how to handle that evidence.")
os.system("pause")
