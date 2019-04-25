# A collection of commonly referenced funtions for use with the EnterpriseAPI calls
import requests
import json
import re
from requests.exceptions import ConnectionError

# Clean and properly parse the response content from the 'getjobstatus' operation
# Returns a properly formatted Python dictionary
def CleanResponse(content):
    cleanResponse = str(content).replace('\\\\r\\\\n','')
    cleanResponse = cleanResponse.replace("b'{",'{')
    cleanResponse = re.sub(r'\\*"','"',cleanResponse)
    cleanResponse = cleanResponse.replace('"{','{')
    cleanResponse = cleanResponse.replace('}"','}')
    cleanResponse = cleanResponse.replace("}'",'}')
    cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
    cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
    cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
    cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
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
    return CleanResponse(response.content)

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