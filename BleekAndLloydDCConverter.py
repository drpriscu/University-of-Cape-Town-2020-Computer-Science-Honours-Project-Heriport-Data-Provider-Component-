#!/usr/bin/env python3
"""
BleekAndLloydDCConverter.py: Program that reads XML metadata files of The New Digital Bleek and Lloyd Archive Data Provider, 
converts the records to (unqualified) Dublin Core and outputs the converted XML metadata files.
Author: Alex Priscu - PRSLAE003
University of Cape Town
Project: Data Provider Interfaces component of the metadata aggregation system – HERIPORT.
Date: 1 October 2020
"""

# Import relevant packages
import os
import pprint
import simpledc
import sys
import unicodedata
import xmltodict

from datetime import datetime, timedelta
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string

# Remove non-ASCII characters from text.
def remove_non_ASCII(text):
    # Replace type hypher with standardised hyphen.
    text = text.replace('–',"-")
    # Return normalised text containing only ASCII characters.
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

# Convert XML metadata record contents to (unqualified) Dublin Core and write the converted metadata to a new XML metadata record.
def convert_to_DC(directoryPath, dcFileName, dictData, serverURL, idNum):
    # Set dictData to content of dictData item.
    dictData = dictData["item"]
    
    # Set New Digital Bleek and Lloyd Archive collection flags to False.
    wilhelmBleekNotebooks = False
    lucyLloydxamNotebooks = False
    lucyLloydkunNotebooks = False
    lucyLloydKoraNotebooks = False
    jemimaBleekNotebooks = False
    dorotheaBleekNotebooks = False
    
    # Set collection flags to True based on collection index ranges.
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
    
    # Implement Data Provider Mapping Schema
    # Assign <dc:subject> to <collection>.
    new = "subject"
    old = "collection"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:description> to <summary> and <comments>.
    new = "description"
    old = "summary"
    try:
        dictData[new] = dictData.pop(old)
        dictData[new] += " "+dictData["comments"]+"."
    except:
        pass
    
    # Assign <dc:creator> to <author>.
    new = "creator"
    old = "author"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:type> to <@type>.
    new = "type"
    old = "@type"
    try:
        dictData[new] = dictData.pop(old)
        if(dictData[new] != "story"):
            print(dictData[new])
    except:
        pass
    
    # Assign <dc:identifier> to URI of record. 
    identifier = serverURL
    dictData["identifier"] = identifier
    
    # Assign <dc:rights> to Data Provider record rights.
    rights = "CC-BY-NC-ND"
    dictData["rights"] = rights
    
    # Assign <dc:format> to Data Provider record format according to Internet Media Types [MIME].
    format = "text/xml"
    dictData["format"] = format
    
    # Assign <dc:date> to Data Provider functional requirements' date.
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    # Try to assign a default value to <dc:title> based on record collection.
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
    
    # Try to assign a default value to <dc:subject> based on record collection.
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
            dictData["subject"] = "The New Digital Bleek and Lloyd Archive"
    
    # Try to assign a default value to <dc:description> based on record collection.
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
            dictData["description"] = "A story from The New Digital Bleek and Lloyd Archive."
    
    # Try to assign a default value to <dc:creator> based on record collection.
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
            dictData["creator"] = "The New Digital Bleek and Lloyd Archive"
    
    # Try to assign a default value to <dc:publisher> based on record collection.
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
            dictData["publisher"] = "The New Digital Bleek and Lloyd Archive"
    
    # Try to assign a default value to <dc:type> based on record collection.
    try:
        dictData["type"]
    except:
        dictData["type"] = "Story"
    
    # Try to assign a default value to <dc:source> based on record collection.
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
            dictData["source"] = "The New Digital Bleek and Lloyd Archive"
    
    # Try to assign a default value to <dc:contributor> based on record collection.
    try:
        dictData["contributor"]
    except:
        dictData["contributor"] = "The New Digital Bleek and Lloyd Archive"
    
    # Format the data types of dictData to lists of str values.
    # For each key in dictData.
    for key in dictData:
        # If the dictData value at the key is of type str or None.
        if (type(dictData[key]) == str) or (type(dictData[key]) == None):
            # Set the dictData value at the key to be of type list.
            dictData[key] = list(dictData[key].split("•"))
    
    # For each key in dictData.             
    for key in dictData:
        # Set valDict to the dictData value at the key.
        valDict = dictData[key]
        
        # If valDict is of type dict.
        if (type(valDict) == dict):
            # Set n to list of valDict values.
            n = valDict.values()
            # Set dictData at the key to n.
            dictData[key] = n 
            # Convert the dictData value at the key to be of type list.
            dictData[key] = " ".join(str(v) for v in dictData[key])
            dictData[key] = list(dictData[key].split("•"))
            
            # For values in valDict.
            for i in valDict.values():
                # If value is of type list.
                if type(i) == list:
                    # Join elements of list.
                    dictData[key] = ' '.join([str(elem) for elem in i])
                    # 
                    dictData[key] = list(dictData[key].split("•"))
        
        # If valDict is of type list and contains a dict value.
        if (type(valDict) == list and type(valDict[0]) == dict):
            # For values in valDict.
            for i in range(0, len(valDict)):
                # Set valDictNew to valDict value.
                valDictNew = valDict[i]
                # Set valDictNew at kw key to None.
                valDictNew["kw"] = "None"
                # If valDict value is not of type None.
                if type(valDict[i]) is not type(None):
                    # Set the dictData value at the key to be of type list.
                    dictData[key] = list(min(valDict[0].values()).split("•"))

        # If valDict is of type list.
        if (type(valDict) == list):
            # Set valDict to type str.
            valDict = str(valDict)
    
    # For each key in dictData.
    for key in dictData.keys():
        # Create a temporary list.
        tempList = []
        # If the dictData value at the key is not empty.
        if (dictData[key] != None):
            # For each value dictData at the key.
            for i in dictData[key]:
                # Run the remove_non_ASCII method.
                i = remove_non_ASCII(str(i))
                # Store the value in the temporary list.
                tempList.append(i)
                # Set the dictData value at the key to the the temporary list.
                dictData[key] = tempList
    
    # Set metadata to dictData converted to an (unqualified) Dublin Core string.
    metadata = simpledc.tostring(dictData)
    # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
    dcFilePath = directoryPath+"/"+dcFileName
    
    # Try to create a file with UTF-8 encoding in the (unqualified) Dublin Core file path
    try:
        dcFile = open(dcFilePath, "w", encoding="utf-8")
        # Write the metadata to the (unqualified) Dublin Core file.
        dcFile.write(metadata)
        # Close the (unqualified) Dublin Core file.
        dcFile.close()
    # Unable to write to the XML metadata record.    
    except Exception as e:
        # Print error statement.
        print ("Error in writing file: "+str(e))
    # Print conversion statement.
    print("Successfully created file: "+dcFileName)

# Read each XML metadata record of a Data Provider directory and call the convert_to_DC method to convert and store converted XML metadata record. 
def read_records():
    # Try to access each sub-folder XML metadata file in a Data Provider directory path.
    try:
        # Set path to the Data Provider directory path.
        path = "stories/"
        for root, directories, filenames in os.walk(path):
            # For each index of the of the Data Provider directory.
            for i in range(1, 2058):
                # Set index to string of current index.
                index = str(i)
                # Set directoryPath to the Data Provider sub-folder directory path.
                directoryPath = os.path.join(root, index)
                # Set filePath to the Data Provider directory path concatenated with the index.
                filePath = directoryPath +"/metadata.xml"
                # Open the XML metadata record with UTF-8 encoding.
                with open(filePath, encoding="utf-8") as file:
                    # Set data to the file contents read.
                    data = file.read()
                    # Replace data html tags.
                    data = data.replace("<i>","")
                    data = data.replace("</i>","")
                    # Set dictData to the dictionary constructed from the data.
                    dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                    # Set dcFileName to "metadata-" concatenated with the index and "-dc.xml".
                    dcFileName = "metadata-"+index+"-dc.xml"
                    # Set serverURL to the Data Provider server URL concatenated with the index.
                    serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+index
                    # Close the (unqualified) Dublin Core file.
                    file.close()
                    # Run the convert_to_DC method.
                    convert_to_DC(directoryPath, dcFileName, dictData, serverURL, i)
            # Print conversion statement.
            print ("Successfully converted files.")
            # Break from for loop after all files have been read and converted.              
            break
    # Unable to open the XML metadata record.
    except Exception as e:
        # Print error statement.
        print ("Error in converting files: "+str(e))

# Only run the functions if this module is run.
if __name__ == "__main__":
    # If number of args is 1.                                     
    if len(sys.argv) == 1:
        # Run the read_records method.                                  
        read_records()
    # Else the number of args is invalid.                                         
    else:
        # Print usage statment.                                                    
        print ("Usage: python3 BleekAndLloydDCConverter.py")