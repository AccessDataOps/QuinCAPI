
import base64
import json
import requests
import tkinter
import os
import sys

#ask for case name
#v2 api select a case to process in
#add in Monitoring https://github.com/gorakhargosh/watchdog/
defaultcasepath = '\\\\win2012\\Data\\Case\\'
#This only has to be done once, the key is associated with the users permissions
Enterprisekey = '83dbc8fa-045a-4b71-83ac-c209223afa90'
#Servername or IP of where Quin-C is installed
servername = '192.168.9.208'
#Check API running

headers = {'EnterpriseApiKey': Enterprisekey}
statuscheckresp = requests.get('http://'+servername+':4443/api/v2/enterpriseapi/statuscheck',headers = headers)
print("Checking Status of API... " + statuscheckresp.reason)
#TODO add in if not OK, exit here

casename = input("Enter the case name: ")
#CaseName is going to be the name of the folder
#casepath = input("Enter the case path: ")

#input validation for the path, this isn't needed unless you ask for the case path
#if(casepath.endswith("\\") == 0):
#    casepath = casepath + "\\"
casepath = defaultcasepath + casename
responsivepath = casepath +"\\responsive"
#The os call below uses the credentials the python script is running, not what AD is running
#if not os.path.exists(casepath):
#    os.makedirs(casepath)
#    os.makedirs(responsivepath)
#else:
#    sys.exit()

print(casepath)
#Place Evidence here, say ready when complete
evidence = input("Enter evidence path(s) - (separated by comma): ")
#Example \\myevidenceserver\evidence1, \\myevidenceserver\evidence2
#Parse

createcase = {"Name": casename, "ProcessingMode":2,"FTKCaseFolderPath": casepath,"ResponsiveFilePath": responsivepath}
resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/createcase',createcase,headers=headers)

print("Case Created Response... " + resp.reason)
caseid = resp.text
print("CaseID " + caseid)
#Pull caseid from resp.content
#wait until case is created...
#caseid = 2
evidencearray = evidence.split(",")
print(evidencearray)
for evidencepath in evidencearray:
    evidencepath = str(evidencepath)
    evidencepath = evidencepath.lstrip()
    print(evidencepath)
    evidence = {'evidenceToCreate': { 'evidencePath': evidencepath }, 'ProcessingOptions':{'PresetType': 1000 }}
    resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/'+str(caseid)+'/processdata',json = evidence,headers=headers)
    print(resp)
    print(resp.content)
    #This is what a good response looks like:
    #<Response [200]>
    #b'[77]'

    #Images in a folder?
    #text file from image
