import requests
import json
import chardet
import time
from datetime import datetime
import EntAPICommon
import re

APIkey = '84af3650-176a-4edf-bad8-25ad5b708f37'
APIhostname = 'WIN-B3VKJBVM6RQ'
JobID = 40
CaseID = 15

jobinfo = EntAPICommon.GetSoftwareInvertoryJobInfo(APIkey, APIhostname, CaseID, JobID)

cleanResponse = str(jobinfo)
cleanResponse = re.sub(r'\\*"','"',cleanResponse)
cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\','\\')
cleanResponse = cleanResponse.replace("b'{",'{')
cleanResponse = cleanResponse.replace('\\\\r\\\\n','')
cleanResponse = re.sub(r'\s*"','"',cleanResponse)
cleanResponse = cleanResponse.replace('"{"','{"')
cleanResponse = re.sub(r'(?<![0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12})}"','}',cleanResponse, flags=re.IGNORECASE)
cleanResponse = cleanResponse.replace("}'",'}')
#cleanResponse = re.sub(r'{[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}}','matched"',cleanResponse , flags=re.IGNORECASE)
#cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
#cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
#cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
#cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\','\\')
print(cleanResponse)
print()
print(json.loads(cleanResponse))