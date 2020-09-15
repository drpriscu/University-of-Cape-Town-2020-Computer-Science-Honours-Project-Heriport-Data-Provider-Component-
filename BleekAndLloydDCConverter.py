#!/usr/bin/env python3

import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import re
import string
import unicodedata
from datetime import datetime, timedelta

def remove_non_ascii(text):
    text = text.replace('–',"-")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

def convert(directoryPath, dcFileName, dictData, serverURL, idNum):
    dictData = dictData['item']
    
    wilhelmBleekNotebooks = False
    lucyLloydxamNotebooks = False
    lucyLloydkunNotebooks = False
    lucyLloydKoraNotebooks = False
    jemimaBleekNotebooks = False
    dorotheaBleekNotebooks = False
    
    if((idNum>=1) and (idNum<=128)):
        wilhelmBleekNotebooks = True
    
    if((idNum>=134) and (idNum<=940)):
        lucyLloydxamNotebooks = True
    
    if((idNum>=944) and (idNum<=1129)):
        lucyLloydkunNotebooks = True
    
    if((idNum>=1132) and (idNum<=1159)):
        lucyLloydKoraNotebooks = True
    
    if((idNum>=2023) and (idNum<=2024)):
        jemimaBleekNotebooks = True
    
    if((idNum>=2025) and (idNum<=2056)):
        dorotheaBleekNotebooks = True
    
    if(wilhelmBleekNotebooks):
        pass
        
    if(lucyLloydxamNotebooks):
        pass
    
    if(lucyLloydkunNotebooks):
        pass
    
    if(lucyLloydKoraNotebooks):
        pass

    if(jemimaBleekNotebooks):
        pass
    
    if(dorotheaBleekNotebooks):
        pass
    
    new = "description"
    old = "summary"
    try:
        dictData[new] = dictData.pop(old)
        dictData[new] += " "+dictData["comments"]+"."
    except:
        pass
    
    new = "subject"
    old = "collection"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    new = "type"
    old = "@type"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    new = "creator"
    old = "author"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    identifier = serverURL
    dictData["identifier"] = identifier
    
    rights = "CC-BY-NC-ND"
    dictData["rights"] = rights
    
    format = "Unqualified Dublin Core"
    dictData["format"] = format
    
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    '''
    creator = ""
    try:
        if (type(dictData["creator"]) == list):
            print (idNum)
            exit()
            for dic in dictData["creator"]:
                creator += dic+", "
            dictData["creator"] = creator[0:len(creator)-2]
    except:
        pass
    '''
    
    try:
        dictData["title"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["title"] = "Story from Wilhelm Bleek's notebooks"
        
        elif(lucyLloydxamNotebooks):
            dictData["title"] = "Story from Lucy Lloyd |xam notebooks"
        
        elif(lucyLloydkunNotebooks):
            dictData["title"] = "Story from Lucy Lloyd !kun notebooks"
        
        elif(lucyLloydKoraNotebooks):
            dictData["title"] = "Story from Lucy Lloyd Kora notebooks"

        elif(jemimaBleekNotebooks):
            dictData["title"] = "Story from Jemima Bleek notebooks"
        
        elif(dorotheaBleekNotebooks):
            dictData["title"] = "Story from Dorothea Bleek notebooks"
        
        else:
            dictData["title"] = "Story from The New Digital Bleek and Lloyd"
    
    try:
        dictData["subject"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["subject"] = "Wilhelm Bleek notebooks"
        
        elif(lucyLloydxamNotebooks):
            dictData["subject"] = "Lucy Lloyd |xam notebooks"
        
        elif(lucyLloydkunNotebooks):
            dictData["subject"] = "Lucy Lloyd !kun notebooks"
        
        elif(lucyLloydKoraNotebooks):
            dictData["subject"] = "Lucy Lloyd Kora notebooks"

        elif(jemimaBleekNotebooks):
            dictData["subject"] = "Jemima Bleek notebooks"
        
        elif(dorotheaBleekNotebooks):
            dictData["subject"] = "Dorothea Bleek notebooks"
        
        else:
            dictData["subject"] = "The New Digital Bleek and Lloyd"
    
    try:
        dictData["description"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["description"] = "A story from Wilhelm Bleek's notebooks."
        
        elif(lucyLloydxamNotebooks):
            dictData["description"] = "A story from Lucy Lloyd |xam notebooks."
        
        elif(lucyLloydkunNotebooks):
            dictData["description"] = "A story from Lucy Lloyd !kun notebooks."
        
        elif(lucyLloydKoraNotebooks):
            dictData["description"] = "A story from Lucy Lloyd Kora notebooks."

        elif(jemimaBleekNotebooks):
            dictData["description"] = "A story from Jemima Bleek notebooks."
        
        elif(dorotheaBleekNotebooks):
            dictData["description"] = "A story from Dorothea Bleek notebooks."
        
        else:
            dictData["description"] = "A story from The New Digital Bleek and Lloyd."
    
    try:
        dictData["creator"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["creator"] = "Wilhelm Bleek"
        
        elif(lucyLloydxamNotebooks):
            dictData["creator"] = "Lucy Lloyd"
        
        elif(lucyLloydkunNotebooks):
            dictData["creator"] = "Lucy Lloyd"
        
        elif(lucyLloydKoraNotebooks):
            dictData["creator"] = "Lucy Lloyd"

        elif(jemimaBleekNotebooks):
            dictData["creator"] = "Jemima Bleek"
        
        elif(dorotheaBleekNotebooks):
            dictData["creator"] = "Dorothea Bleek"
        
        else:
            dictData["creator"] = "The New Digital Bleek and Lloyd"
    
    try:
        dictData["publisher"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["publisher"] = "Wilhelm Bleek"
        
        elif(lucyLloydxamNotebooks):
            dictData["publisher"] = "Lucy Lloyd"
        
        elif(lucyLloydkunNotebooks):
            dictData["publisher"] = "Lucy Lloyd"
        
        elif(lucyLloydKoraNotebooks):
            dictData["publisher"] = "Lucy Lloyd"

        elif(jemimaBleekNotebooks):
            dictData["publisher"] = "Jemima Bleek"
        
        elif(dorotheaBleekNotebooks):
            dictData["publisher"] = "Dorothea Bleek"
        
        else:
            dictData["publisher"] = "The New Digital Bleek and Lloyd"
    
    try:
        dictData["type"]
    except:
        dictData["type"] = "Story"
    
    try:
        dictData["source"]
    except:
        if(wilhelmBleekNotebooks):
            dictData["source"] = "Wilhelm Bleek"
        
        elif(lucyLloydxamNotebooks):
            dictData["source"] = "Lucy Lloyd"
        
        elif(lucyLloydkunNotebooks):
            dictData["source"] = "Lucy Lloyd"
        
        elif(lucyLloydKoraNotebooks):
            dictData["source"] = "Lucy Lloyd"

        elif(jemimaBleekNotebooks):
            dictData["source"] = "Jemima Bleek"
        
        elif(dorotheaBleekNotebooks):
            dictData["source"] = "Dorothea Bleek"
        
        else:
            dictData["source"] = "The New Digital Bleek and Lloyd"
    
    try:
        dictData["contributor"]
    except:
        dictData["contributor"] = "The New Digital Bleek and Lloyd"
    
    for keys in dictData:
        if (type(dictData[keys]) == str) or (type(dictData[keys]) == None):
                dictData[keys] = list(dictData[keys].split("•"))
                
    for x in dictData:
        valDict = dictData[x]
 
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[x] = n 
            dictData[x] = " ".join(str(v) for v in dictData[x])
            dictData[x] = list(dictData[x].split("•"))

            for i in valDict.values():
                if type(i) == list:
                    dictData[x] = ' '.join([str(elem) for elem in i]) 
                    dictData[x] = list(dictData[x].split("•"))
                   
        if (type(valDict) == list and type(valDict[0]) == dict):
            for i in range(0,len(valDict)):
                valDictNew = valDict[i]
                valDictNew['kw'] = "None"

                if type(valDict[i]) is not type(None):
                    dictData[x] = list(min(valDict[0].values()).split("•"))
    
        if (type(valDict) == list):
            valDict = str(valDict)
      
    for x in dictData.keys():
        tempList = []
        if (dictData[x] != None):
            for i in dictData[x]:
                i = remove_non_ascii(str(i))
                tempList.append(i)
                dictData[x] = tempList
    
    metadata = simpledc.tostring(dictData)
    dcFilePath = directoryPath+"/"+dcFileName
    
    try:
        dcFile = open(dcFilePath, "w", encoding="utf-8")
        dcFile.write(metadata)
        dcFile.close()
    except Exception as e:
                print(e)
                
    print("Successfully created file: "+dcFileName)

path = 'stories/'

try:
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            idNum = i
            directoryPath = os.path.join(root, str(i))
            if (directoryPath == 'stories/'+str(i)):
                    filePath = directoryPath +'/metadata.xml'
                    with open(filePath, encoding="utf-8") as file:
                        data = file.read()
                        data = data.replace("<i>","")
                        data = data.replace("</i>","")

                        dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                        dcFileName = "metadata-"+str(i)+"-dc.xml"
                        serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
                        convert(directoryPath, dcFileName, dictData, serverURL, idNum)
        print("Successfully converted files.")                
        break
except Exception as e:
    print ("Error in converting files: ")
    print (e)