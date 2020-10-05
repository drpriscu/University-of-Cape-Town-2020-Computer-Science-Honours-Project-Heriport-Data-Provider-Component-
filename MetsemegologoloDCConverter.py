#!/usr/bin/env python3
"""
MetsemegologoloDCConverter.py: Program that reads XML metadata files of The Metsemegologolo Archive Data Provider, 
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
    # Set dictData to content of dictData object.
    dictData = dictData["object"]
    
    # Implement Data Provider Mapping Schema
    # Assign <dc:creator> to produced by value in <subject>.
    new = "creator"
    try:
        dictData[new] = dictData["relationship"][1]["subject"]["#text"]  
    except:
        pass
    
    # Assign <dc:publisher> to collected by value in <subject>.
    new = "publisher"
    try:
        dictData[new] = dictData["relationship"][2]["subject"]["#text"]  
    except:
        pass
    
    # Assign <dc:coverage> to <provenance>.
    new = "coverage"
    old = "provenance"
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
    
    # Try to assign a default value to <dc:title> based on record collection.
    try:
        dictData["title"]
    except:
        dictData["title"] = "Object from the Metsemegologolo Archive"
    
    # Try to assign a default value to <dc:subject> based on record collection.
    try:
        dictData["subject"]
    except:
        dictData["subject"] = "Metsemegologolo"
    
    # Try to assign a default value to <dc:description> based on record collection.
    try:
        dictData["description"]
    except:
        dictData["description"] = "An object from the Metsemegologolo Archive."
    
    # Try to assign a default value to <dc:creator> based on record collection.
    try:
        dictData["creator"]
    except:
        dictData["creator"] = "The Metsemegologolo Archive"
    
    # Try to assign a default value to <dc:publisher> based on record collection.
    try:
        dictData["publisher"]
    except:
        dictData["publisher"] = "The Metsemegologolo Archive"
    
    # Try to assign a default value to <dc:type> based on record collection.
    try:
        dictData["type"]
    except:
        dictData["type"] = "Object"
    
    # Try to assign a default value to <dc:right> based on Data Provider record rights.
    try:
        dictData["rights"]
    except:
        dictData["rights"] = "CC BY-SA"
    
    # Try to assign a default value to <dc:source> based on record collection.
    try:
        dictData["source"]
    except:
        dictData["source"] = "The Metsemegologolo Archive"
    
    # Try to assign a default value to <dc:contributor> based on record collection.
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
        path = "Metsemegologolo/"
        for root, directories, filenames in os.walk(path):
            # For each index of the of the Data Provider directory.
            for i in range(1, 2):
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
                    data = data.replace("<relationships","")
                    data = data.replace("</relationships>","")
                    # Set dictData to the dictionary constructed from the data.
                    dictData = dict(xmltodict.parse(data, dict_constructor=dict))
                    # Set dcFileName to "metadata-" concatenated with the index and "-dc.xml".
                    dcFileName = "metadata-"+index+"-dc.xml"
                    # Set serverURL to the Data Provider server URL concatenated with the index.
                    serverURL = "http://Metsemegologolo.apc.uct.ac.za/metadata/Metsemegologolo/"+index
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
        print ("Usage: python3 MetsemegologoloDCConverter.py")