import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

APIhostname = "WIN-B3VKJBVM6RQ"
response = requests.get("https://" + APIhostname + ":4443/api/v2/enterpriseapi/statuscheck", verify=False)
print(response)