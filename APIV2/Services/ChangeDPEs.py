# Version: .1
# Date: 5/1/2019
#
# To add a list of DPEs, drag-and-drop a TXT file with one DPE
# per line onto the icon for this script.
#
# This script can also be used to list current DPEs, remove
# specific DPEs, or remove all DPEs

import winreg
import sys
import os
import xml.etree.ElementTree as ET
from shutil import copyfile

def AddDPE(DPEname):
    # Add a new DPE
    print("Adding '%s' to the DPM Configuration" % DPEname)
    DPEdefinition = {
        'address': 'net.tcp://%s:34097/ProcessingEngine' % DPEname,
        'binding': 'netTcpBinding',
        'bindingConfiguration': 'TCPBinding',
        'contract': 'AccessData.EvidenceProcessing.BackendShared.IProcessingEngineService',
        'name': DPEname}
    ET.SubElement(DPEs, "endpoint", DPEdefinition)
    return

def RemoveDPE(DPEindex):
    # Remove a DPE
    print("Removing '%s' from the DPM Configuration" % DPEs[DPEindex].get("name"))
    DPEs.remove(DPEs[DPEindex])
    return

def ClearDPEs():
    # Removes all DPEs (use a temporary list to not alter what we're iterating on)
    for DPE in list(DPEs):
        print("Removing '%s' from the DPM Configuration" % DPE.get("name"))
        DPEs.remove(DPE)
    return

def WriteDPMConfig():
    # Backup the original config file first
    copyfile(ConfigFile, ConfigFile + ".old")
    tree.write(ConfigFile, encoding="utf-8", xml_declaration=True)
    # Do some string replacements because ElementTree moves around the xmlns attribute
    with open(ConfigFile, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('<configuration xmlns="urn:schemas-microsoft-com:asm.v1">', '<configuration>')
    filedata = filedata.replace('<assemblyBinding>', '<assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">')
    with open(ConfigFile, 'w') as file:
        file.write(filedata)
    return

# Find the DPM config file
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\ADProcessingManager")
ManagerFolder =  os.path.dirname(winreg.QueryValueEx(key, "ImagePath")[0].strip('\"'))
ConfigFile = os.path.join(ManagerFolder,"ProcessingManager.exe.config")

# Parse the XML in the config file
ET.register_namespace('', "urn:schemas-microsoft-com:asm.v1")
tree = ET.parse(ConfigFile)
root = tree.getroot()
DPEs = root[1][0]

if len(sys.argv) == 2:
    # Parse the list of new DPEs
    DPElist = []
    with open(sys.argv[1], 'r') as file:
        DPElist = file.read().splitlines()
    # Add the DPEs to the DPM config
    for DPE in DPElist:
        AddDPE(str(DPE))
    WriteDPMConfig()
else:
    print("To add a list of DPEs, close this window then drag-and-drop a TXT file with one DPE per line onto the icon for this script.")
    # Keep running until closed
    while True:
        print()
        choice = ''
        while choice not in ['1','2','3']:
            print("1 - List current DPEs")
            print("2 - Remove a DPE")
            print("3 - Remove all DPEs")
            choice = input("Choose 1, 2, or 3: ")
            if choice not in ['1','2','3']:
                print("Invalid selection!")
            print()
        if choice == '1':
            # List the current DPEs
            print("Your current Distributed Processing Engines are:")
            for DPE in DPEs:
                print(DPE.get("name"))
        elif choice == '2':
            # List the current DPEs
            print("Which Distributed Processing Engines would you like to remove?")
            for i in range(0, len(DPEs)):
                print("%s - %s" % (i, DPEs[i].get("name")))
            index = int(input("Enter the corresponding index: "))
            RemoveDPE(index)
            WriteDPMConfig()
        else:
            ClearDPEs()
            WriteDPMConfig()

os.system("pause")