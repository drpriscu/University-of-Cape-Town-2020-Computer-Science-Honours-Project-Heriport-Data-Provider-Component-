#!/usr/bin/env python3

import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import unicodedata
from datetime import datetime

def remove_non_ascii(text):
    text = text.replace('–',"-")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

def convert(directoryPath, dcFileName, dictData, serverURL, idNum):
    dictData = dictData['object']
        
    new = "coverage"
    old = "provenance"
    try:
        dictData[new] = dictData.pop(old)    
    except:
        pass
    
    new = "creator"
    try:
        dictData[new] = dictData["relationship"][1]["subject"]["#text"]  
    except:
        pass
    
    new = "publisher"
    try:
        dictData[new] = dictData["relationship"][2]["subject"]["#text"]  
    except:
        pass
        
    identifier = serverURL
    dictData["identifier"] = identifier
    
    format = "Unqualified Dublin Core"
    dictData["format"] = format
    
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    try:
        dictData["title"]
    except:
        dictData["title"] = "Object from the Metsemegologolo Archive"
    
    try:
        dictData["subject"]
    except:
        dictData["subject"] = "Metsemegologolo"
    
    try:
        dictData["description"]
    except:
        dictData["description"] = "An object from the Metsemegologolo Archive."
    
    try:
        dictData["creator"]
    except:
        dictData["creator"] = "The Metsemegologolo Archive"
            
    try:
        dictData["publisher"]
    except:
        dictData["publisher"] = "The Metsemegologolo Archive"
     
    try:
        dictData["type"]
    except:
        dictData["type"] = "Object"
    
    try:
        dictData["rights"]
    except:
        dictData["rights"] = "CC BY-SA"
    
    try:
        dictData["source"]
    except:
        dictData["source"] = "The Metsemegologolo Archive"
    
    try:
        dictData["contributor"]
    except:
        dictData["contributor"] = "The Metsemegologolo Archive"
      
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
    
    print ("Successfully created file: "+dcFileName)

path = 'Metsemegologolo/'

try:
    for root, directories, filenames in os.walk(path):
        for i in range(1,2):
            idNum = i
            directoryPath = os.path.join(root, str(i))
            if (directoryPath == 'Metsemegologolo/'+str(i)):
                    filePath = directoryPath +'/metadata.xml'
                    with open(filePath, encoding="utf-8") as file:
                        data = file.read()
                        data = data.replace("<relationships","")
                        data = data.replace("</relationships>","")
                        
                        dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                        dcFileName = "metadata-"+str(i)+"-dc.xml"
                        serverURL = "http://Metsemegologolo.apc.uct.ac.za/metadata/Metsemegologolo/"+str(i)
                        convert(directoryPath, dcFileName, dictData, serverURL, idNum)
        print ("Successfully converted files.")                
        break
except Exception as e:
    print ("Error in converting files: ")
    print (e)