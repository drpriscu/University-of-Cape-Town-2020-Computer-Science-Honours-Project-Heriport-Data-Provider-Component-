#!/usr/bin/env python3
import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc

def convert(fileName,dictData):
    dictData = dictData['item'] 

    new = "description"
    old = "summary"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass

    new = "identifier"
    old = "id"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass

    for keys in dictData:
        if (type(dictData[keys]) == str) or (type(dictData[keys]) == None):
                dictData[keys] = list(dictData[keys].split("-"))
                
    for x in dictData:
        valDict = dictData[x]
        
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[x] = n 
            
            for i in valDict.values():
                if type(i) == list:
                    dictData[x] = ' '.join([str(elem) for elem in i]) 
                    dictData[x] = list(dictData[x].split("-"))
                            
        if (type(valDict) == list and type(valDict[0]) == dict):
            for i in range(0,len(valDict)):
                valDictNew = valDict[i]
                valDictNew['kw'] = "None"
                if type(valDict[i]) is not type(None):
                    dictData[x] = list(min(valDict[0].values()).split("-"))
    
        if (type(valDict) == list):
            valDict = str(valDict)
            
    metadata = simpledc.tostring(dictData)
    record = []
    
    newFileName = "stories-dc/"+fileName
    newFile = open(newFileName, "w")
    newFile.write(metadata)
    newFile.close()
    print("Successfully created file: "+fileName)
    record.append(metadata)

path = 'stories/'

for root, directories, filenames in os.walk(path):
    for i in range(1,2058):
        directory_path = os.path.join(root, str(i))
        print('stories/'+str(i))
        if directory_path == 'stories/'+str(i):
                filePath = directory_path +'/metadata.xml'
                with open(filePath) as file:
                    dictData = dict(xmltodict.parse(file.read(), dict_constructor=dict))
                    fileName = "metadata-"+str(i)+"-dc.xml"
                    convert(fileName,dictData)
    print("Successfully converted files.")                
    break