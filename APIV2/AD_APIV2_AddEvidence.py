import requests
import base64
import json

targets = '192.168.9.205'
caseid = 2
servername = '192.168.9.205'
Enterprisekey = 'b4cfe8e6-3ee9-4663-8e84-516fa890de73'
evidencepath = '\\\\192.168.9.205\\Data\\text'

headers = {'EnterpriseApiKey': Enterprisekey }
evidence = {'evidenceToCreate': { 'evidencePath': evidencepath }}
resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/'+str(caseid)+'/processdata',json = evidence,headers=headers)
print(resp)
print(resp.content)
#This is what a good response looks like:
#<Response [200]>
#b'[77]'