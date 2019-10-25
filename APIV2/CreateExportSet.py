import base64
import json
import requests
import tkinter
import os
import sys
import uuid
from tkinter import filedialog
from tkinter import *

#This only has to be done once, the key is associated with the users permissions
Enterprisekey = 'a93b5851-242e-43c8-843a-b3880e2c5ad9'
#Servername or IP of where Quin-C is installed
servername = 'jakkuvm01'
defaultCaseId = 5
defaultLabelId = 1
defaultPath = f'\\\\{servername}\\c$\\temp'

#Check API running
headers = {'EnterpriseApiKey': Enterprisekey}
statuscheckresp = requests.get('http://'+servername+':4443/api/v2/enterpriseapi/statuscheck',headers = headers)
print("Checking Status of API... " + statuscheckresp.reason)
#TODO add in if not OK, exit here

top = tkinter.Tk()
top.title("Automate AD LAB 7.1. Create Export Set")
top.geometry("350x300")

def validation(S):
    return S.isdigit()
vcmd = (top.register(validation), '%S')
lbl = tkinter.Label(top, text = "Please enter case id:")
lbl.grid(column = 0, row=0)
caseText = tkinter.Entry(top, width = 30, validate='key', vcmd=vcmd)
caseText.insert(END, defaultCaseId)
caseText.grid(column = 0, row = 1)


lbl = tkinter.Label(top, text = "Please enter export label id:")
lbl.grid(column = 0, row=2)
labelText = tkinter.Entry(top, width = 30, validate='key', vcmd=vcmd)
labelText.insert(END, defaultLabelId)
labelText.grid(column = 0, row = 3)

lbl = tkinter.Label(top, text = "Please enter export UNC directory:")
lbl.grid(column = 0, row=4)
folder_path = tkinter.Entry(top, width = 30)
folder_path.insert(END, defaultPath)
folder_path.grid(column = 0, row = 5)

lblExport = Label(master=top,text="Export type", width = 50, height = 2, anchor = S)
lblExport.grid(row=9, column=0)
selectedType = StringVar(top)
selectedType.set("Native") # default value
typeMenu = OptionMenu(top, selectedType, "Ad1", "Native", "LoadFile", "ImageLoadFile", "ProductionSet") #, "BulkPrintJob")
typeMenu.grid(row=10, column=0)


def clickedSubmit():
    caseId = int(caseText.get())
    jobName = f'{caseId}_{str(uuid.uuid4())}'
    global jobId
    req = {'ExportBase': {'ExportPath':  folder_path.get(), 'JobName' : jobName, 'Label' : {'Id' : labelText.get()}}, 'exportType' : selectedType.get()}
    resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/jobs/' + str(caseId) + '/createexportset',json = req,headers=headers)
    jobId.set(resp.content)

jobId = StringVar()
lblSubmit = Label(master=top,textvariable=jobId, width = 50, height = 2, anchor = S)
lblSubmit.grid(row=11, column=0)
btnSubmit = tkinter.Button(top, text = "Submit", command = clickedSubmit)
btnSubmit.grid(row = 12, column = 0)

top.mainloop()