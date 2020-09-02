# Alex Priscu
# Program that takes in an XML file and outputs a DC formatted XML file.
# Bleek and Lloyd Interface
# 27 July 2020

#!/usr/bin/env python3

# Imports
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

    #return ''.join('\\u%04x' % ord(c) for c in text)
    #return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    #return re.sub(f'[^{re.escape(string.printable)}]', ' ', text)
    #"<UTF_encoded>"
    #"</UTF_encoded>"
    #return re.sub(f'[^{re.escape(string.printable)}]', ' ', text)
    #removeCharacters = ["-"]
    #text = text.replace(removeCharacters,"puta")
    #text = re.sub(f'[^{re.escape(string.printable)}]', ' ', text)
    #return text.replace("puta","-")
    #removeCharacters = ["-", "_"]
    
    #text = text.replace(removeCharacters,"")
    
    #for character in removeCharacters:
        #text = text.replace(removeCharacters,"")
        
    #return re.sub(f'[^{re.escape(string.printable)}]', ' ', text)

def remove_non_ascii(text):
    text = text.replace('–',"-")
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    
# Takes in a dictionary of XML data and outputs a DC formatted XML file.
def convert(directoryPath, serverURL, dcFileName, dictData):
    dictData = dictData['item'] 

    # Mapping
    new = "description"
    old = "summary"
    # Update dictionary
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
    #dateSplit = date.split(" ")
    #date = dateSplit[0]
    dictData["date"] = date

    # Map values in dicitonary to list type values
    for keys in dictData:
        if (type(dictData[keys]) == str) or (type(dictData[keys]) == None):
                dictData[keys] = list(dictData[keys].split("+"))
    
    # Remove dict type values in dicitonary to type of list values
    for x in dictData:
        valDict = dictData[x]
        
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[x] = n # List of value stored in dict value
            dictData[x] = " ".join(str(v) for v in dictData[x])
            dictData[x] = list(dictData[x].split("+"))
            
            for i in valDict.values():
                if type(i) == list:
                    dictData[x] = ' '.join([str(elem) for elem in i]) 
                    dictData[x] = list(dictData[x].split("+"))
                            
        if (type(valDict) == list and type(valDict[0]) == dict):
            # Convert inner dict value to a list
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
        
    # Convert dictionary to a DC XML string
    metadata = simpledc.tostring(dictData)
    record = []
    # Saving converted data to a XML file
    
    dcFilePath = directoryPath+"/"+dcFileName
    dcFile = open(dcFilePath, "w", encoding="utf-8")
    dcFile.write(metadata)
    dcFile.close()
    print("Successfully created file: "+dcFileName)
    
    record.append(metadata)
    
    # Saving converted data to a listRecord XML file
    ''' newFile = open("dataProvider_DC_Records.xml", "a")
    newFile.write(metadata+"\n")
    newFile.close()
    print("Successfully created file: dataProvider_DC_Records.xml") '''
    
    
# List of file names in directory that need to be converted.
path = 'stories/'
# Iterate through each file to be converted.
for root, directories, filenames in os.walk(path):
    for i in range(1,2058):
        #for directory in directories:
        directoryPath = os.path.join(root, str(i))
        if (directoryPath == 'stories/'+str(i)):
                # do something with directoryPath
                filePath = directoryPath +'/metadata.xml'
                # Convert the XML file to a dictionary.
                with open(filePath, encoding="utf-8") as file:
                    data = file.read()
                    data = data.replace("<i>","")
                    data = data.replace("</i>","")

                    dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                    dcFileName = "metadata-"+str(i)+"-dc.xml"
                    serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
                    convert(directoryPath, serverURL, dcFileName, dictData)
    print("Successfully converted files.")                
    break