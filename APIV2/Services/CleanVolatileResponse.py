# This function will clean and properly parse the response content from the 'getjobstatus' operation

import base64
import json
import re

def CleanResponse(content):
    cleanResponse = str(content).replace('\\\\r\\\\n','')
    cleanResponse = cleanResponse.replace("b'{",'{')
    cleanResponse = re.sub(r'\\*"','"',cleanResponse)
    cleanResponse = cleanResponse.replace('"{','{')
    cleanResponse = cleanResponse.replace('}"','}')
    cleanResponse = cleanResponse.replace("}'",'}')
    cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
    cleanResponse = cleanResponse.replace('"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','"\\\\\\\\')
    cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
    cleanResponse = cleanResponse.replace('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\','\\\\')
    return json.loads(cleanResponse)