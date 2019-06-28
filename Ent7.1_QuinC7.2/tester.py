import requests
import json
import re
from requests.exceptions import ConnectionError
import pyodbc
import socket
import os
import time
from datetime import datetime
from shutil import copyfile

ProcessingProfileXML = "ForensicProcessing.xml"

ScriptFolder = os.path.abspath(os.path.dirname(__file__))
ProcessingProfileFolder = os.path.join(ScriptFolder, "Processing Profiles")
ProcessingProfileFile = os.path.join(ProcessingProfileFolder, ProcessingProfileXML)

# JSON doesn't allow comments, so this strips comments out when reading in a JSON-formatted definition
# Returns JSON dictionary
def FileToString(FilePath):
    with open(FilePath, 'r') as file:
        filedata = file.read()
    return filedata

print(FileToString(ProcessingProfileFile))