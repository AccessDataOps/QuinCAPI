import requests

apihost = "WIN-B3VKJBVM6RQ"
apikey = "fe1245f3-f385-407e-9184-70f7b1720890"
casename = "API Script Case"
casepath = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData"

headers = {'EnterpriseApiKey': apikey}
createcase = {
"Name": casename,
"ProcessingMode":2,
"FTKCaseFolderPath": casepath
}

resp = requests.post('http://'+apihost+':4443/api/v2/enterpriseapi/core/createcase',createcase,headers=headers)
print('Created case %s' % resp.text)
