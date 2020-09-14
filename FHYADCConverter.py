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
from datetime import datetime

def remove_non_ascii(text):
    text = text.replace('–',"-")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

def convert(directoryPath, dcFileName, dictData, serverURL, idNum):
    dictData = dictData['item']     
    
    new = "description"
    old = "file"
    try:
        dictData[new] = serverURL[0:30]
        dictData[new] += "collection/"
        dictData[new] += dictData.pop(old)
    except:
        pass
    
    new = "subject"
    old = "qubitParentSlug"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    new = "type"
    old = "radGeneralMaterialDesignation"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    new = "contributor"
    old = "eventActor"
    try:
        dictData[new] = dictData.pop(old)    
    except:
        pass
    
    '''
    new = "identifier"
    old = "file"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    '''
    
    identifier = serverURL
    dictData["identifier"] = identifier
    
    new = "rights"
    old = "reproductionConditions"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    new = "source"
    old = "scopeAndContent"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    format = "Unqualified Dublin Core"
    dictData["format"] = format
    
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    value = (dictData["title"][0])
    dictData["title"] = str(value)
    
    authors = []
    try:
        for dic in dictData["contributor"]:
            dic = dic["#text"]
            #dictData["contributor"] = dic
            authors.append(dic)
            #authors += dic+", "
        dictData["contributor"] = authors
        #dictData["contributors"] = authors[0:len(authors)-2]
    except:
        pass
    
    try:
        dictData["title"]
    except:
        dictData["title"] = "Item from The Five Hundred Year Archive"
    
    try:
        dictData["subject"]
    except:
        dictData["subject"] = "fhya-depot"
    
    try:
        dictData["description"]
    except:
        dictData["description"] = "An item from The Five Hundred Year Archive."
    
    try:
        dictData["creators"]
    except:
        if(idNum != 54):    
            splitString = ":"
            split = dictData["source"].split(splitString)
            splitString = " for"
            split = dictData["source"].split(splitString)
            dictData["creators"] = split[0][10:len(split[0])]
        else:
            dictData["creators"] = dictData["source"][10:138]
            
    try:
        dictData["publishers"]
    except:
        if(idNum != 54):    
            splitString = ":"
            split = dictData["source"].split(splitString)
            splitString = " for"
            split = dictData["source"].split(splitString)
            dictData["publishers"] = split[0][10:len(split[0])]
        else:
            dictData["publishers"] = dictData["source"][10:138]
        
    try:
        dictData["type"]
    except:
        dictData["type"] = "Item"
    
    try:
        dictData["rights"]
    except:
        dictData["rights"] = "Creative Commons License: CC BY-NC-ND\nhttps://creativecommons.org/licenses/by-nc-nd/3.0/\nUnless otherwise stated the copyright of all material on the FHYA resides with the contributing institution/custodian."  
        
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
    
    print("Successfully created file: "+dcFileName)

path = 'FHYA Depot/'

for root, directories, filenames in os.walk(path):
    for i in range(1,88):
        idNum = i
        directoryPath = os.path.join(root, str(i))
        if (directoryPath == 'FHYA Depot/'+str(i)):
                filePath = directoryPath +'/metadata.xml'
                with open(filePath, encoding="utf-8") as file:
                    data = file.read()
                    data = data.replace("<view","")
                    data = data.replace("</view>","")
                    data = data.replace("<event>","")
                    data = data.replace("</event>","")
                    
                    dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                    dcFileName = "metadata-"+str(i)+"-dc.xml"
                    serverURL = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                    convert(directoryPath, dcFileName, dictData, serverURL, idNum)
    print("Successfully converted files.")                
    break