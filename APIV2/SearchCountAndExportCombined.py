import base64
import json
import requests
import tkinter
import os
import sys
import time
import uuid
from tkinter import filedialog
from tkinter import *

#This only has to be done once, the key is associated with the users permissions
Enterprisekey = 'a93b5851-242e-43c8-843a-b3880e2c5ad9'
#Servername or IP of where Quin-C is installed
servername = 'jakkuvm01'
defaultCaseId = 5
defaultPath = f'\\\\{servername}\\c$\\temp'

headers = {'EnterpriseApiKey': Enterprisekey}
statuscheckresp = requests.get('http://'+servername+':4443/api/v2/enterpriseapi/statuscheck',headers = headers)
print("Checking Status of API... " + statuscheckresp.reason)
#TODO add in if not OK, exit here

top = tkinter.Tk()
top.title("Automate AD LAB 7.1. Search Count Report & Export")
top.geometry("400x350")

def validation(S):
    return S.isdigit()
vcmd = (top.register(validation), '%S')
lbl = tkinter.Label(top, text = "Please enter case id:")
lbl.grid(column = 0, row=0)
caseText = tkinter.Entry(top, width = 30, validate='key', vcmd=vcmd)
caseText.insert(END, defaultCaseId)
caseText.grid(column = 0, row = 1)

def csvButtonClick():
    global csvPath
    filename = filedialog.askopenfilename(title = "Select CSV file with terms", filetypes = [("csv files","*.csv")])
    csvPath.set(filename)
    print(filename)

csvPath = StringVar()
lblCSV = Label(master = top,textvariable = csvPath, width = 50, height = 2, anchor = S)
lblCSV.grid(row=2, column=0)
buttonCSV = Button(text="Browse CSV with terms", command=csvButtonClick)
buttonCSV.grid(row=3, column=0, pady = 2)

lbl = tkinter.Label(top, text = "Please enter export UNC directory:", height = 2, anchor = S)
lbl.grid(column = 0, row=4)
folderPath = tkinter.Entry(top, width = 30)
folderPath.insert(END, defaultPath)
folderPath.grid(column = 0, row = 5)

lblExport = Label(master=top,text="Export type", width = 50, height = 2, anchor = S)
lblExport.grid(row=6, column=0)
selectedType = StringVar(top)
selectedType.set("Ad1") # default value
typeMenu = OptionMenu(top, selectedType, "Ad1", "Native", "LoadFile", "ImageLoadFile", "ProductionSet") #, "BulkPrintJob")
typeMenu.grid(row=7, column=0)

lblStatus = tkinter.Text(top, width = 40, height = 40, state=DISABLED)
lblStatus.grid(column = 0, row = 9, sticky = N)

def clickedSubmit():
    global lblStatus
    lblStatus.configure(state='normal')
    lblStatus.delete('1.0', END)
    lblStatus.configure(state='disabled')
    caseId = int(caseText.get())
    csvFilePath = str(csvPath.get())
    exportFolder = str(folderPath.get())
    with open(csvFilePath, 'r', encoding='utf-8-sig') as file:
        data = file.read().replace('\n', ',')
    terms = list(filter(None, map(str.strip, data.split(','))))
    lblTerms = []
    for term in terms:
        lblTerms.append({'Label' : term, 'Term' : term})
    name = "Report Name"
    jobName = f'{caseId}_{str(uuid.uuid4())}'

    reqSearch = {'Criteria' : {}, 'Name' : name, 'SearchTerms' : lblTerms, 'AssignLabel' : 'true'}
    respSearch = requests.post(f'http://{servername}:4443/api/v2/enterpriseapi/jobs/{caseId}/createsearchcountreport', json = reqSearch, headers=headers)
    jobSearch = int(respSearch.content)
    
    while True:
        statusResp = requests.get(f'http://{servername}:4443/api/v2/enterpriseapi/core/{caseId}/getjobstatus/{jobSearch}',headers = headers)
        jsonResp = json.loads(statusResp.content)
        state = jsonResp['state']
        lblStatus.configure(state='normal')
        lblStatus.insert('1.0', f'SearchCount Job {jobSearch}: {state}\n')
        lblStatus.configure(state='disabled')
        top.update()
        if state != 'Submitted' and state != 'InProgress':
            break
        time.sleep(1)

    lblStatus.configure(state='normal')
    lblStatus.insert('1.0', f'\n')
    lblStatus.configure(state='disabled')

    labelIds = []
    for term in terms:
        lbl = {'Name' : term}
        # Returns label id in case it already exists
        respLabel = requests.post(f'http://{servername}:4443/api/v2/enterpriseapi/core/{caseId}/createlabel', json = lbl, headers=headers)
        jsonResp = json.loads(respLabel.content)
        labelId = jsonResp['labelId']
        labelIds.append((labelId, term))
    
    lblStatus.configure(state='normal')
    lblStatus.insert('1.0', f'\nLabelIds: {labelIds}\n')
    lblStatus.configure(state='disabled')
    
    for lblId, lblName in labelIds:
        req = {'ExportBase': {'ExportPath':  exportFolder, 'JobName' : jobName, 'Label' : {'Id' : str(lblId)}}, 'exportType' : selectedType.get()}
        respExport = requests.post(f'http://{servername}:4443/api/v2/enterpriseapi/jobs/{caseId}/createexportset', json = req, headers=headers)
        jobExport = int(json.loads(respExport.content)['jobId'])
        while True:
            statusResp = requests.get(f'http://{servername}:4443/api/v2/enterpriseapi/core/{caseId}/getjobstatus/{jobExport}',headers = headers)
            jsonResp = json.loads(statusResp.content)
            state = jsonResp['state']
            lblStatus.configure(state='normal')
            lblStatus.insert('1.0', f'Export Job for label {lblName}. {jobSearch}: {state}\n')
            lblStatus.configure(state='disabled')
            top.update()
            if state != 'Submitted' and state != 'InProgress':
                break
            time.sleep(1)
    
    lblStatus.configure(state='normal')
    lblStatus.insert('1.0', f'Done\n\n')
    lblStatus.configure(state='disabled')

btnSubmit = tkinter.Button(top, text = "Submit", command = clickedSubmit)
btnSubmit.grid(column = 0, row = 8)
top.mainloop()