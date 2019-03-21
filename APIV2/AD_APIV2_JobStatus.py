import requests
import base64
import json
import chardet

jobid = 76
caseid = 2

headers = {'EnterpriseApiKey': 'b4cfe8e6-3ee9-4663-8e84-516fa890de73'}
resp = requests.get('http://192.168.9.205:4443/api/v2/enterpriseapi/'+str(caseid)+'/getjobstatus/'+str(jobid),headers = headers)
print("Job Status for Job: " + str(jobid))
print(resp)
print("-"*20)
print(resp.content)
print(chardet.detect(resp.content)["encoding"])
data = json.loads(resp.content.decode(chardet.detect(resp.content)["encoding"]))
print(str(data).replace("\n",''))
print(json.dumps(data,indent=4, sort_keys=True))

#resp should reply with a <Response [200]>
#resp.content will return all the information about the job out, initially you will just see a processing status that doesn't update often