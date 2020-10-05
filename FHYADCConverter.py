#!/usr/bin/env python3
"""
FHYADCConverter.py: Program that reads XML metadata files of The Five Hundred Year Archive Data Provider, 
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

# Convert XML metadata record contents to (unqualified) Dublin Core and writes the updated metadata to a new XML metadata record.
def convert_to_DC(directoryPath, dcFileName, dictData, serverURL, idNum):
    # Set dictData to content of dictData item.
    dictData = dictData["item"]
    
    # Implement Data Provider Mapping Schema
    # Assign <dc:subject> to <qubitParentSlug>.
    new = "subject"
    old = "qubitParentSlug"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:description> to server URL concatendated with collection/" and <file>.
    new = "description"
    old = "file"
    try:
        dictData[new] = serverURL[0:30]
        dictData[new] += "collection/"
        dictData[new] += dictData.pop(old)
    except:
        pass
    
    # Assign <dc:source> to <scopeAndContent>.
    new = "source"
    old = "scopeAndContent"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
        
    # Assign <dc:contributor> to <eventActor>.
    new = "contributor"
    old = "eventActor"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:rights> to <reproductionConditions>.
    new = "rights"
    old = "reproductionConditions"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:type> to <radGeneralMaterialDesignation>.
    new = "type"
    old = "radGeneralMaterialDesignation"
    try:
        dictData[new] = dictData.pop(old)
    except:
        pass
    
    # Assign <dc:identifier> to URI of record. 
    identifier = serverURL
    dictData["identifier"] = identifier
    
    # Assign <dc:format> to Data Provider record format according to Internet Media Types [MIME].
    format = "text/xml"
    dictData["format"] = format
    
    # Assign <dc:date> to Data Provider functional requirements' date.
    date = str(datetime.now())
    dateSplit = date.split(" ")
    date = dateSplit[0]
    dictData["date"] = date
    
    # Assign <dc:title> to first title value.
    value = (dictData["title"][0])
    dictData["title"] = str(value)
    
    # Try to extract <dc:contributor> values.
    try:
        # Set authors to an empty list.
        authors = []
        # For each dic in in dictData at the contributor key.
        for dic in dictData["contributor"]:
            # Set dic to the value of dic at the #text key.
            dic = dic["#text"]
            # Append dic to authors.
            authors.append(dic)
        # Set dictData at the contributor key to authors.
        dictData["contributor"] = authors
    except:
        pass
    
    # Try to assign a default value to <dc:title> based on record collection.
    try:
        dictData["title"]
    except:
        dictData["title"] = "Item from The Five Hundred Year Archive"
    
    # Try to assign a default value to <dc:subject> based on record collection.
    try:
        dictData["subject"]
    except:
        dictData["subject"] = "Fhya-depot"
    
    # Try to assign a default value to <dc:description> based on record collection.
    try:
        dictData["description"]
    except:
        dictData["description"] = "An item from The Five Hundred Year Archive."
    
    # Try to assign a default value to <dc:creator> based on record collection.
    try:
        dictData["creator"]
    except:
        # Split the value of <dc:source> to get the creator names.
        # If the record is not number 54, split differently.
        if (idNum != 54):    
            splitString = ":"
            split = dictData["source"].split(splitString)
            splitString = " for"
            split = dictData["source"].split(splitString)
            dictData["creator"] = split[0][10:len(split[0])]    
        # Else the record is number 54, split differently.
        else:
            dictData["creator"] = dictData["source"][10:138]
    
    # Try to assign a default value to <dc:publisher> based on record collection.
    try:
        dictData["publisher"]
    except:
        # Split the value of <dc:source> to get the publisher names.
        # If the record is not number 54, split differently.
        if (idNum != 54):    
            splitString = ":"
            split = dictData["source"].split(splitString)
            splitString = " for"
            split = dictData["source"].split(splitString)
            dictData["publisher"] = split[0][10:len(split[0])]
        # Else the record is number 54, split differently.
        else:
            dictData["publisher"] = dictData["source"][10:138]
    
    # Try to assign a default value to <dc:type> based on record collection.
    try:
        dictData["type"]
    except:
        dictData["type"] = "Item"
    
    # Try to assign a default value to <dc:right> based on record collection.
    try:
        dictData["rights"]
    except:
        dictData["rights"] = "Creative Commons License: CC BY-NC-ND\nhttps://creativecommons.org/licenses/by-nc-nd/3.0/\nUnless otherwise stated the copyright of all material on the FHYA resides with the contributing institution/custodian."  
    
    for key in dictData:
        if (type(dictData[key]) == str) or (type(dictData[key]) == None):
                dictData[key] = list(dictData[key].split("•"))
    
    for key in dictData:
        valDict = dictData[key]
 
        if (type(valDict) == dict):
            n = valDict.values()
            dictData[key] = n 
            dictData[key] = " ".join(str(v) for v in dictData[key])
            dictData[key] = list(dictData[key].split("•"))

            for i in valDict.values():
                if type(i) == list:
                    dictData[key] = ' '.join([str(elem) for elem in i]) 
                    dictData[key] = list(dictData[key].split("•"))
        
        if (type(valDict) == list):
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
        path = "FHYA Depot/"
        for root, directories, filenames in os.walk(path):
            # For each index of the of the Data Provider directory.
            for i in range(1, 88):
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
                    # Replace data tags.
                    data = data.replace("<view","")
                    data = data.replace("</view>","")
                    data = data.replace("<event>","")
                    data = data.replace("</event>","")
                    # Set dictData to the dictionary constructed from the data.
                    dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                    # Set dcFileName to "metadata-" concatenated with the index and "-dc.xml".
                    dcFileName = "metadata-"+index+"-dc.xml"
                    # Set serverURL to the Data Provider server URL concatenated with the index.
                    serverURL = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+index
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
        print ("Usage: python3 FHYADCConverter.py")