
import base64
import json
import requests
import tkinter
import os
import sys
from tkinter import filedialog
from tkinter import *

#This only has to be done once, the key is associated with the users permissions
Enterprisekey = 'a93b5851-242e-43c8-843a-b3880e2c5ad9'
#Servername or IP of where Quin-C is installed
servername = 'jakkuvm01'
#Check API running

headers = {'EnterpriseApiKey': Enterprisekey}
statuscheckresp = requests.get('http://'+servername+':4443/api/v2/enterpriseapi/statuscheck',headers = headers)
print("Checking Status of API... " + statuscheckresp.reason)
#TODO add in if not OK, exit here

top = tkinter.Tk()
top.title("Automate AD LAB 7.1. Create Export Set")
top.geometry("400x300")

def validation(S):
    return S.isdigit()
vcmd = (top.register(validation), '%S')
lbl = tkinter.Label(top, text = "Please enter case id:")
lbl.grid(column = 0, row=0)
caseText = tkinter.Entry(top, width = 30, validate='key', vcmd=vcmd)
caseText.grid(column = 0, row = 1)

lbl = tkinter.Label(top, text = "Please enter Job Name:")
lbl.grid(column = 0, row=2)
jobNameText = tkinter.Entry(top, width = 30)
jobNameText.grid(column = 0, row = 3)

def browseButtonClick():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

folder_path = StringVar()
lblFolder = Label(master=top,textvariable=folder_path, width = 50, height = 2, anchor = S)
lblFolder.grid(row=5, column=0)
buttonFolder = Button(text="Browse Export Folder", command=browseButtonClick)
buttonFolder.grid(row=6, column=0, pady = 2)

lblExport = Label(master=top,text="Export type", width = 50, height = 2, anchor = S)
lblExport.grid(row=7, column=0)
selectedType = StringVar(top)
selectedType.set("Ad1") # default value
typeMenu = OptionMenu(top, selectedType, "Ad1", "Native", "LoadFile", "ImageLoadFile", "ProductionSet", "BulkPrintJob")
typeMenu.grid(row=8, column=0)


def clickedSubmit():
    caseId = int(caseText.get())
    jobName = str(jobNameText.get())
    global jobId
    req = {'ExportBase': {'ExportPath':  folder_path.get(), 'JobName' : jobName}, 'exportType' : selectedType.get()}
    resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/jobs/' + str(caseId) + '/createexportset',json = req,headers=headers)
    jobId.set(resp.content)

jobId = StringVar()
lblSubmit = Label(master=top,textvariable=jobId, width = 50, height = 2, anchor = S)
lblSubmit.grid(row=9, column=0)
btnSubmit = tkinter.Button(top, text = "Submit", command = clickedSubmit)
btnSubmit.grid(row = 10, column = 0)

top.mainloop()