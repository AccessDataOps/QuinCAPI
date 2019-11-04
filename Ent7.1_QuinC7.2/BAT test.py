import requests
import os
from requests.exceptions import ConnectionError

# Edit the variables below as needed
quincURL = 'http://localhost:4443' # Your Quin-C base URL.
apiKey = 'INSERT API KEY' # Your API key.
caseFolder = '//HOSTNAME/Share/Cases' # Default case data path, must already exist. USE FORWARD SLASHES

########## DON'T TOUCH BELOW ##########
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
caseFolder = os.path.normpath(caseFolder)
CaseName = input("Enter your desired case name: ")
definition = {
"Name": CaseName,
"ProcessingMode":2,
"FTKCaseFolderPath": caseFolder
}

resp = requests.post(quincURL + '/api/v2/enterpriseapi/core/createcase',definition,headers = {'EnterpriseApiKey': apiKey}, verify=False)
print('Created case %s' % resp.text)
os.system("pause")
