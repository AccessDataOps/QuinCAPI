
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
casename ="Testcase"
top = tkinter.Tk()
top.title("Automate AD LAB 7.1")
#Add in case name
top.geometry("400x300")
lbl = tkinter.Label(top, text = "Please enter your case name:")
lbl.grid(column =0, row=0)
txt = tkinter.Entry(top, width = 50)
txt.grid(column = 0, row = 1)
def clicked():
    casename = txt.get()
btn = tkinter.Button(top, text = "Enter", command = clicked)
btn.grid(column = 1, row = 1)
top.mainloop()

casename = input("Enter the case name: ")
#CaseName is going to be the name of the folder
#casepath = input("Enter the case path: ")

#input validation for the path, this isn't needed unless you ask for the case path
#if(casepath.endswith("\\") == 0):
#    casepath = casepath + "\\"
casepath = defaultcasepath + casename
responsivepath = casepath +"\\evidence"
#The os call below uses the credentials the python script is running, not what AD is running
if not os.path.exists(responsivepath):
    os.makedirs(responsivepath)


print(casepath)

#Parse

createcase = {"Name": casename, "ProcessingMode":2, "description": "Scott is asking questions...","FTKCaseFolderPath": casepath,"ResponsiveFilePath": responsivepath}
resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/createcase',createcase,headers=headers)

print("Case Created Response... " + resp.reason)
caseid = resp.text
print("CaseID " + caseid)
if not os.path.exists(responsivepath):
    os.makedirs(responsivepath)

#Pull caseid from resp.content
#wait until case is created...
#caseid = 2

#Place Evidence here, say ready when complete
#evidence = input("Enter evidence path(s) - (separated by comma): ")
#Example \\myevidenceserver\evidence1, \\myevidenceserver\evidence2
input("Place Evidence in this directory: " + responsivepath + ", Click Enter When Ready.")
print("Loading Folders of Evidence...")
print(os.listdir(responsivepath))

#Splits the evidence into an array
#evidencearray = evidence.split(",")
#print(evidencearray)

#for evidencepath in evidencearray:
for DirectoryName in os.listdir(responsivepath):
    #evidencepath = str(evidencepath)
    #evidencepath = evidencepath.lstrip()
    evidencepath = responsivepath + "\\" + DirectoryName
    print("Loading " + evidencepath)
    evidence = {'evidenceToCreate': { 'evidencePath': evidencepath }, 'ProcessingOptions':{'PresetType': 1000 }}
    resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/'+str(caseid)+'/processdata',json = evidence,headers=headers)
    print("Submit status " + resp.reason)
    print("JobID " + str(resp.content))
    #This is what a good response looks like:
    #OK
    #b'[77]'

    #Images in a folder?
    #text file from image
