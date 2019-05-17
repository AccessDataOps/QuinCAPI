import requests
import json
import chardet
import time
from datetime import datetime
import EntAPICommon

APIkey = '84af3650-176a-4edf-bad8-25ad5b708f37'
APIhostname = 'WIN-B3VKJBVM6RQ'
JobID = 1
CaseID = 1
ProjectData = "\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData" # Default case data path, make sure to escape any backslashes
ReportsPath = ProjectData + "\\Reports"

print(EntAPICommon.CopyJobReports(APIkey, APIhostname, CaseID, JobID, ReportsPath))