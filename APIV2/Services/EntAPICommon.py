# Version: .9, added CopyJobReports
# Date: 5/17/2019
# 
# DO NOT RUN THIS SCRIPT
# This script contains commonly used funtions for use other EnterpriseAPI scripts

import requests
import json
import re
from requests.exceptions import ConnectionError
import pyodbc
import socket
import os
import time
from datetime import datetime
from shutil import copyfile

# Clean and properly parse the response content from the 'getjobstatus' operation
# Returns a properly formatted Python dictionary
def CleanResponse(text):
    cleanResponse = str(text)
    cleanResponse = re.sub(r'\\*"','"',cleanResponse)
    cleanResponse = re.sub(r'\\r\\n\s*','',cleanResponse)
    cleanResponse = cleanResponse.replace('"{"','{"')
    cleanResponse = re.sub(r'(?<![0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})}"','}',cleanResponse, flags=re.IGNORECASE)
    cleanResponse = cleanResponse.replace('\\\\\\\\','\\')
    cleanResponse = re.sub(r'(?<!")\\\\\\\\',r'\\\\',cleanResponse)
    return json.loads(cleanResponse)

# Checks if the API is up
# Returns True or False
def IsApiUp(APIhostname):
    print("Checking API status on %s..." % APIhostname)
    try:
        response = requests.get("http://" + APIhostname + ":4443/api/v2/enterpriseapi/statuscheck")
        if (response.reason == "OK"):
            return True
        else:
            return False
    except ConnectionError: # Suppress full traceback
        return False

# Gets all info about a job
# Returns reponse content (job info) as a Python dictionary
def GetJobInfo(APIkey, APIhostname, CaseID, JobID):
    response = requests.get('http://' + APIhostname + ':4443/api/v2/enterpriseapi/'+str(CaseID)+'/getjobstatus/'+str(JobID),headers = {'EnterpriseApiKey': APIkey})
    return CleanResponse(response.text)

# Creates a new case
# Returns new Case ID
def CreateCase(APIkey, APIhostname, definition):
    response = requests.post('http://' + APIhostname + ':4443/api/v2/enterpriseapi/createcase',definition,headers = {'EnterpriseApiKey': APIkey})
    return response.content.decode("utf-8")

# Runs a volatile job
# Returns new Job ID
def VolatileJob(APIkey, APIhostname, CaseID, definition):
    response = requests.post('http://' + APIhostname + ':4443/api/v2/enterpriseapi/'+str(CaseID)+'/volatile',json = definition,headers = {'EnterpriseApiKey': APIkey})
    return response.content.decode("utf-8")

# Adds data from a volatile job to a case
# Returns status
def AddVolatile(APIkey, APIhostname, CaseID, JobID):
    response = requests.get('http://' + APIhostname + ':4443/api/v2/enterpriseapi/'+str(CaseID)+'/importvolatile/'+str(JobID),headers = {'EnterpriseApiKey': APIkey})
    return response.reason

# Detects evidence type based on a given path
# File or folder of natives = 0
# Folder of images = 1
# Image = 2
# Text = 3
# Returns evidence type as an integer
def DetectEvidenceType(path):
    # Check if path ends in an extension matching a supported image type
    if (re.search('(\.ad1|\.e01|\.ex01|\.l01|\.lx01|\.aff|\.vhd|\.nrg|\.s01\.001\.1|\.bin|\.cue|\.dd|\.dmg|\.ima|\.img|\.iso|\.raw|\.vmdk|\.vdi|\.mds|\.ccd|\.pxi|\.vc4|\.yaffs1|\.yaffs2)$', path.lower())):
        evidencetype = 2
    # Check if path is a non-image file
    elif (re.search('(\..{1,3})$', path)):
        evidencetype = 0
    else:
        containsimage = False
        # Check if path contains any files ending in an extension matching a supported image type
        for file in os.listdir(path):
            if (re.search('(\.ad1|\.e01|\.ex01|\.l01|\.lx01|\.aff|\.vhd|\.nrg|\.s01|\.001|\.1|\.bin|\.cue|\.dd|\.dmg|\.ima|\.img|\.iso|\.raw|\.vmdk|\.vdi|\.mds|\.ccd|\.pxi|\.vc4|\.yaffs1|\.yaffs2)$', file.lower())):
                containsimage = True
        if (containsimage == True):
            evidencetype = 1
        # Treat it as a folder of natives
        else:
            evidencetype = 0
    return evidencetype

# Processes evidence (image or native)
# Returns status
def AddEvidence(APIkey, APIhostname, CaseID, definition):
    response = requests.post('http://'+APIhostname+':4443/api/v2/enterpriseapi/'+str(CaseID)+'/processdata',json = definition,headers = {'EnterpriseApiKey': APIkey})
    return response.reason

# Runs a SQL query against MSSQL
# Returns results as a list of dictionaries
def QueryMSSQL(InstanceName, DatabaseName, Query):
    connectstring = 'Driver={SQL Server};Server=%s;Database=%s;Trusted_Connection=yes;' % (InstanceName, DatabaseName)
    conn = pyodbc.connect(connectstring)
    cursor = conn.cursor()
    cursor.execute(Query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results

# Checks if a target is listening on a specified port
# Returns True or False
def IsPortListening(IP, Port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((IP,Port))
    sock.close()
    if result == 0:
        return True
    else:
        return False

# Runs a collection job, storing the results on the target
# Returns new Job ID
def CollectionOnAgent(APIkey, APIhostname, CaseID, definition):
    response = requests.post('http://' + APIhostname + ':4443/api/v2/enterpriseapi/'+str(CaseID)+'/collectiononagent',json = definition,headers = {'EnterpriseApiKey': APIkey})
    return response.content.decode("utf-8")

# JSON doesn't allow comments, so this strips comments out when reading in a JSON-formatted definition
# Returns JSON dictionary
def FileToJSON(DefinitionFile):
    with open(DefinitionFile, 'r') as file:
        filedata = file.read()
    strippedComments = re.sub(r'#.*\n','\n',filedata)
    return json.loads(strippedComments)

# Runs a software inventory job
# Returns new Job ID
def SoftwareInventoryJob(APIkey, APIhostname, CaseID, definition):
    response = requests.post('http://' + APIhostname + ':4443/api/v2/enterpriseapi/'+str(CaseID)+'/sofwareinventory',json = definition,headers = {'EnterpriseApiKey': APIkey})
    return response.content.decode("utf-8")

# Copies the XML files for a job into a more accessible location
# Returns string showing where the reports are
def CopyJobReports(APIkey, APIhostname, CaseID, JobID, ReportsPath):
    jobinfo = GetJobInfo(APIkey, APIhostname, CaseID, JobID)
    # Get the Target Name and list of ResultFiles from the job info
    target = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Details"]["Name"]
    resultfiles = jobinfo["resultData"]["RealData"]["TaskStatusList"][0]["Results"][1]["ResultFileLocation"]
    # Build a list of the result XML files
    tasks = []
    for i in range(0,len(resultfiles)):
        tasks.append({"Target": target, "Path": resultfiles[i]["FilePath"], "Filename": os.path.basename(resultfiles[i]["FilePath"])})
    # Copy the result XML files to a nicer location and name
    if not os.path.exists(ReportsPath):
            os.makedirs(ReportsPath)
    starttime = datetime.strptime(jobinfo["startDate"], '%Y-%m-%dT%H:%M:%S.%f') # Parse the job info timestamp to something Python understands
    for i in range(0,len(tasks)):
        src = tasks[i]["Path"]
        dst = "%s\\%s_%s_%s" % (ReportsPath,tasks[i]["Target"],starttime.strftime("%Y%m%d%H%M%SUTC"),tasks[i]["Filename"])
        copyfile(src,dst)
    return "The XML reports for job %s can be found in '%s'.\nThese can be opened with Excel." % (JobID, ReportsPath)