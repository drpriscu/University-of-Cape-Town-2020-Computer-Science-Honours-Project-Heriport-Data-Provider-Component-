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
import cgi

print("Content-Type: text/xml\n\n") # XML markup follows

# Takes in a dictionary of XML data and outputs a DC formatted XML file.
def convert(fileName,dictData):
    dictData = dictData['item'] 

    # Mapping
    new = "description"
    old = "summary"
    # Update dictionary
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass

    # Mapping
    new = "identifier"
    old = "id"
    # Update dictionary
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass

    # Map values in dicitonary to list type values
    for keys in dictData:
        if (type(dictData[keys]) == str) or (type(dictData[keys]) == None):
                dictData[keys] = list(dictData[keys].split("-"))

    # Remove dict type values in dicitonary to type of list values
    for x in dictData:
        valDict = dictData[x]
        
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[x] = n # List of value stored in dict value
            
            for i in valDict.values():
                if type(i) == list:
                    dictData[x] = ' '.join([str(elem) for elem in i]) 
                    dictData[x] = list(dictData[x].split("-"))
                            
        if (type(valDict) == list and type(valDict[0]) == dict):
            # Convert inner dict value to a list
            for i in range(0,len(valDict)):
                valDictNew = valDict[i]
                valDictNew['kw'] = "None"
                if type(valDict[i]) is not type(None):
                    dictData[x] = list(min(valDict[0].values()).split("-"))
    
        if (type(valDict) == list):
            valDict = str(valDict)
            
    # Convert dictionary to a DC XML string
    metadata = simpledc.tostring(dictData)
    record = []
    # Saving converted data to a XML file
    
    newFileName = "stories-dc/"+fileName
    newFile = open(newFileName, "w")
    newFile.write(metadata)
    newFile.close()
    print("Successfully created file: "+fileName)
    
    # Saving converted data to a listRecord XML file
    ''' newFile = open("dataProvider_DC_Records.xml", "a")
    newFile.write(metadata+"\n")
    newFile.close()
    print("Successfully created file: dataProvider_DC_Records.xml") '''
    
    record.append(metadata)
  

# List of file names in directory that need to be converted.
path = 'stories/'
# Iterate through each file to be converted.
for root, directories, filenames in os.walk(path):
    for i in range(1,2058):
        #for directory in directories:
        directory_path = os.path.join(root, str(i))
        print('stories/'+str(i))
        if directory_path == 'stories/'+str(i):
                # do something with directory_path
                filePath = directory_path +'/metadata.xml'
                # Convert the XML file to a dictionary.
                with open(filePath) as file:
                    dictData = dict(xmltodict.parse(file.read(), dict_constructor=dict))
                    fileName = "metadata-"+str(i)+"-dc.xml"
                    convert(fileName,dictData)

    print("Successfully converted files.")                
    break