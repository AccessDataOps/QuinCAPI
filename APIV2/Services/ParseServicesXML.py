import xml.etree.ElementTree as ET
import csv
import os

xmlfile = '\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\4a6ca231-5230-48ea-8d3c-0108e0c0e1bb\\Jobs\\job_25\\2386c1fd-27a7-478b-9958-f115b0366c4d\\1\\services.xml'
element_tree = ET.parse(xmlfile)
root = element_tree.getroot()

if not os.path.exists("\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports"):
    os.makedirs("\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports")
servicesCSV = open('\\\\WIN-B3VKJBVM6RQ\\AccessData\\ProjectData\\v17\\Reports\\services.csv', 'w')

csvwriter = csv.writer(servicesCSV)
services_head = []

count = 0
for member in root.findall("Service"):
    service = []
    if count == 0:
        Name = member.find("Name").tag
        services_head.append(Name)
        StartedAs = member.find('StartedAs').tag
        services_head.append(StartedAs)
        State = member.find('State').tag
        services_head.append(State)
        RealState = member.find('RealState').tag
        services_head.append(RealState)
        StartMode = member.find('StartMode').tag
        services_head.append(StartMode)
        RealStartMode = member.find('RealStartMode').tag
        services_head.append(RealStartMode)
        RealType = member.find('RealType').tag
        services_head.append(RealType)
        Path = member.find('Path').tag
        services_head.append(Path)
        plist = member.find('plist').tag
        services_head.append(plist)
        MD5 = member.find('MD5').tag
        services_head.append(MD5)
        SHA1 = member.find('SHA1').tag
        services_head.append(SHA1)
        FuzzySize = member.find('FuzzySize').tag
        services_head.append(FuzzySize)
        Fuzzy = member.find('Fuzzy').tag
        services_head.append(Fuzzy)
        Fuzzy2X = member.find('Fuzzy2X').tag
        services_head.append(Fuzzy2X)
        KFFStatus = member.find('KFFStatus').tag
        services_head.append(KFFStatus)
        FromAgent = member.find('FromAgent').tag
        services_head.append(FromAgent)
        DispName = member.find('DispName').tag
        services_head.append(DispName)
        Desc = member.find('Desc').tag
        services_head.append(Desc)
        processid = member.find('processid').tag
        services_head.append(processid)
        csvwriter.writerow(services_head)
        count = count + 1

    Name = member.find('Name').text
    service.append(Name)
    StartedAs = member.find('StartedAs').text
    service.append(StartedAs)
    State = member.find('State').text
    service.append(State)
    RealState = member.find('RealState').text
    service.append(RealState)
    StartMode = member.find('StartMode').text
    service.append(StartMode)
    RealStartMode = member.find('RealStartMode').text
    service.append(RealStartMode)
    RealType = member.find('RealType').text
    service.append(RealType)
    Path = member.find('Path').text
    service.append(Path)
    plist = member.find('plist').text
    service.append(plist)
    MD5 = member.find('MD5').text
    service.append(MD5)
    SHA1 = member.find('SHA1').text
    service.append(SHA1)
    FuzzySize = member.find('FuzzySize').text
    service.append(FuzzySize)
    Fuzzy = member.find('Fuzzy').text
    service.append(Fuzzy)
    Fuzzy2X = member.find('Fuzzy2X').text
    service.append(Fuzzy2X)
    KFFStatus = member.find('KFFStatus').text
    service.append(KFFStatus)
    FromAgent = member.find('FromAgent').text
    service.append(FromAgent)
    DispName = member.find('DispName').text
    service.append(DispName)
    #Desc = member.find('Desc').text
    #service.append(Desc)
    processid = member.find('processid').text
    service.append(processid)
    csvwriter.writerow(service)
servicesCSV.close()