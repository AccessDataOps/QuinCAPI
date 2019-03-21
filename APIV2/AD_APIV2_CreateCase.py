import requests
import base64
import json

casename = "TestOneX"
casepath = "\\\\192.168.9.205\\case"
responsivepath = "\\\\192.168.9.205\\case\\responsive"

headers = {'EnterpriseApiKey': 'b4cfe8e6-3ee9-4663-8e84-516fa890de73'}
createcase = {"Name": casename, "ProcessingMode":2,"FTKCaseFolderPath": casepath,"ResponsiveFilePath": responsivepath}
resp = requests.post('http://192.168.9.205:4443/api/v2/enterpriseapi/createcase',createcase,headers=headers)
print(resp)
print(resp.content)
