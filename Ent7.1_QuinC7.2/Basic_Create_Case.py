import requests

apihost = "WIN-B3VKJBVM6RQ"
apikey = "c45a22c3-8da7-49ee-929b-ab6185fa90e4"
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
