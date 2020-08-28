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

def convert(directoryPath, serverURL, dcFileName, dictData):
    dictData = dictData['item'] 

    new = "description"
    old = "summary"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    identifier = serverURL
    dictData["identifier"] = identifier
    
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    for keys in dictData:
        if (type(dictData[keys]) == str) or (type(dictData[keys]) == None):
                dictData[keys] = list(dictData[keys].split("+"))
                
    for x in dictData:
        valDict = dictData[x]
 
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[x] = n 
            dictData[x] = " ".join(str(v) for v in dictData[x])
            dictData[x] = list(dictData[x].split("+"))

            for i in valDict.values():
                if type(i) == list:
                    dictData[x] = ' '.join([str(elem) for elem in i]) 
                    dictData[x] = list(dictData[x].split("+"))
                   
        if (type(valDict) == list and type(valDict[0]) == dict):
            for i in range(0,len(valDict)):
                valDictNew = valDict[i]
                valDictNew['kw'] = "None"

                if type(valDict[i]) is not type(None):
                    dictData[x] = list(min(valDict[0].values()).split("+"))
    
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
        dcFile = open(dcFilePath, "w")
        dcFile.write(metadata)
        dcFile.close()
    except Exception as e:
                print(e)
    
    print("Successfully created file: "+dcFileName)

path = 'stories/'

for root, directories, filenames in os.walk(path):
    for i in range(1,2058):
        directoryPath = os.path.join(root, str(i))
        if (directoryPath == 'stories/'+str(i)):
                filePath = directoryPath +'/metadata.xml'
                with open(filePath) as file:
                    dictData = dict(xmltodict.parse(file.read(), dict_constructor=dict))
                    dcFileName = "metadata-"+str(i)+"-dc.xml"
                    serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
                    convert(directoryPath, serverURL, dcFileName, dictData)
    print("Successfully converted files.")                
    break