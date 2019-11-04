import base64
import json
import requests
import tkinter
import os
import sys
from tkinter import *

#This only has to be done once, the key is associated with the users permissions
Enterprisekey = 'a93b5851-242e-43c8-843a-b3880e2c5ad9'
#Servername or IP of where Quin-C is installed
servername = 'jakkuvm01'
defaultCaseId = 5

headers = {'EnterpriseApiKey': Enterprisekey}
statuscheckresp = requests.get('http://'+servername+':4443/api/v2/enterpriseapi/statuscheck',headers = headers)
print("Checking Status of API... " + statuscheckresp.reason)
#TODO add in if not OK, exit here

top = tkinter.Tk()
top.title("Automate AD LAB 7.1. Search Count Report")
top.geometry("400x300")

def validation(S):
    return S.isdigit()
vcmd = (top.register(validation), '%S')
lbl = tkinter.Label(top, text = "Please enter case id:")
lbl.grid(column = 0, row=0)
caseText = tkinter.Entry(top, width = 30, validate='key', vcmd=vcmd)
caseText.insert(END, defaultCaseId)
caseText.grid(column = 0, row = 1)

lbl = tkinter.Label(top, text = "Please enter name:")
lbl.grid(column = 1, row=0)
nameText = tkinter.Entry(top, width = 30)
nameText.grid(column = 1, row = 1)

assignLabels = BooleanVar()
labelButton = tkinter.Checkbutton(top, text = "Assign Labels", variable = assignLabels, height = 2, anchor = S)
labelButton.grid(column = 0, row = 2)

global btnAddTerm
global btnSubmit
global rowCount
global lstLabels
global lstTerms
global lblJob

lstLabels = []
lstTerms = []
lblJob = tkinter.Label(top, text = "Job ID: ", height = 2, anchor = S)
rowCount = 4

def clickedAdd():
    global rowCount
    global lstLabels
    global lstTerms
    global lblJob
    txt = tkinter.Entry(top, width = 30)
    txt.grid(column = 0, row = rowCount)
    txt2 = tkinter.Entry(top, width = 30)
    txt2.grid(column = 1, row = rowCount, padx=10, pady=2)
    lstLabels.append(txt)
    lstTerms.append(txt2)
    rowCount = rowCount + 1
    btnAddTerm.grid(column = 0, row = rowCount, sticky = E)
    btnSubmit.grid(column = 0, row = rowCount + 1, sticky = E)
    lblJob.grid_forget()

lbl = tkinter.Label(top, text = "Label")
lbl.grid(column =0, row=3, sticky = S)
lbl = tkinter.Label(top, text = "Term")
lbl.grid(column =1, row=3, sticky = S)
btnAddTerm = tkinter.Button(top, text = "Add", command = clickedAdd)


def clickedSubmit():
    global lblJob
    caseId = int(caseText.get())
    name = nameText.get()
    if not name:
        name = "Report Name"

    # Create list of Label-Term pairs
    terms = []
    for i in range(0, len(lstTerms)):
        lbl = str(lstLabels[i].get())
        trm = str(lstTerms[i].get())
        if lbl and trm:
            terms.append(
                {
                    "Label" : lbl,
                    "Term" : trm
                })

    req = {'Criteria' : {}, 'Name' : name, 'SearchTerms' : terms, 'AssignLabel' : str(assignLabels.get())}
    print(req)
    resp = requests.post('http://'+servername+':4443/api/v2/enterpriseapi/jobs/' + str(caseId) + '/createsearchcountreport',json = req,headers=headers)
    lblJob = tkinter.Label(top, text = "Job ID: " + str(resp.content), height = 2, anchor = S)
    lblJob.grid(column = 1, row = rowCount + 1, sticky = W)

btnSubmit = tkinter.Button(top, text = "Submit", command = clickedSubmit)

clickedAdd()
top.mainloop()