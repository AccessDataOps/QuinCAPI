import requests
import base64
import json

#Validates the API is running <Response [200]> is expected and means "OK"
headers = {'EnterpriseApiKey': 'b4cfe8e6-3ee9-4663-8e84-516fa890de73'}
resp = requests.get('http://192.168.9.205:4443/api/v2/enterpriseapi/statuccheck',headers = headers)
print(resp)
print(resp.content)