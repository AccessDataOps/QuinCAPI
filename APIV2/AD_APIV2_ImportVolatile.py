import requests
import base64
import json

targets = '192.168.9.205'
caseid = 2
jobid = 74

headers = {'EnterpriseApiKey': 'b4cfe8e6-3ee9-4663-8e84-516fa890de73'}
volatile = {'Volatile': { 'IncludeServices': True },'ips': {  'targets':[ str(targets) ] }}
resp = requests.get('http://192.168.9.205:4443/api/v2/enterpriseapi/'+str(caseid)+'/importvolatile/'+str(jobid),json = volatile,headers=headers)
print(resp)
print(resp.content)

