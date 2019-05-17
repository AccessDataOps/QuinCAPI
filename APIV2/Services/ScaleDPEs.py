# Version: .1
# Date: 5/9/2019
#
# Adds or removes a DPE to/from the DPM
# Script must be run on the machine running the DPM
# 
# Usage
# Add a DPE:      ScaleDPEs.py -a <Hostname/IP>
# Remove a DPE:   ScaleDPEs.py -r <Hostname/IP>
#
# Can be called remotely via WMIC, potentially allowing a DPE to add itself
# wmic /node:DPMip /user:"domain\user" /password:"password" process call create "scriptPathOnDPM -a myIP"

import winreg
import sys
import os
import xml.etree.ElementTree as ET
from shutil import copyfile
import socket

def ShowUsage():
    print("Usage")
    print("Add a DPE:\t%s -a <Hostname/IP>" % os.path.basename(__file__))
    print("Remove a DPE:\t%s -r <Hostname/IP>" % os.path.basename(__file__))
    return

def AddDPE(host):
    # Add a new DPE
    if host in DPElist:
        print("Endpoint '%s' already exists" % host)
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,34097))
    sock.close()
    if result == 0:
        print("Adding '%s' to the DPM Configuration" % host)
        DPEdefinition = {
            'address': 'net.tcp://%s:34097/ProcessingEngine' % host,
            'binding': 'netTcpBinding',
            'bindingConfiguration': 'TCPBinding',
            'contract': 'AccessData.EvidenceProcessing.BackendShared.IProcessingEngineService',
            'name': host}
        ET.SubElement(DPEtree, "endpoint", DPEdefinition)
    else:
        print("Can't reach Processing Engine Service on '%s'" % host)
    return

def RemoveDPE(host):
    # Remove a DPE
    if host not in DPElist:
        print("Endpoint '%s' does not exist" % host)
        return
    for DPE in list(DPEtree):
        if DPE.get("name") == host:
            print("Removing '%s' from the DPM Configuration" % host)
            DPEtree.remove(DPE)
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
    try:
        with open(ConfigFile, 'w') as file:
            file.write(filedata)
        print("Complete")
    except PermissionError:
        print("Couldn't write configuration. Try again later.")
    return

# Find the DPM config file
key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\ADProcessingManager")
ManagerFolder =  os.path.dirname(winreg.QueryValueEx(key, "ImagePath")[0].strip('\"'))
ConfigFile = os.path.join(ManagerFolder,"ProcessingManager.exe.config")

# Parse the XML in the config file
ET.register_namespace('', "urn:schemas-microsoft-com:asm.v1")
tree = ET.parse(ConfigFile)
root = tree.getroot()
DPEtree = root[1][0]
DPElist = [DPE.get("name") for DPE in DPEtree]

if len(sys.argv) == 1:
    ShowUsage()
elif len(sys.argv) != 3:
    print("Invalid number of arguments.")
    ShowUsage()
elif sys.argv[1] not in ['-a', '-r']:
    print("Invalid argument %s." % sys.argv[1])
    ShowUsage()
else:
    if sys.argv[1] == '-a':
        AddDPE(str(sys.argv[2]))
    elif sys.argv[1] == '-r':
        RemoveDPE(str(sys.argv[2]))
    WriteDPMConfig()