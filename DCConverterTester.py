#!/usr/bin/env python3

import os
import sys
import xmltodict
import pprint
from lxml import etree
from io import StringIO
from xmlutils import Rules, dump_etree_helper, etree_to_string
import unicodedata
from datetime import datetime

total = 0

def check(dcFileName, data):
    global total
    case1 = False
    case2 = False
    print ("_________________________________________________________________________________")
    print ("\n\nTesting: "+dcFileName)
    print("Case 1: Checking XML Well-Formedness")
    
    with open("oai_dc.xsd", 'r') as schema_file:
        schema_to_check = schema_file.read()

    with open(dcFileName, 'r') as xml_file:
        xml_to_check = xml_file.read()
    
    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    try:
        doc = etree.parse(StringIO(xml_to_check[39:len(xml_to_check)]))
        print ("PASS")
        case1 = True

    except etree.XMLSyntaxError as err:
        print ("FAIL")
        print ("_________________________________________________________________________________")
        
    print("\nCase 2: Validate against Unqualified Dublin Core Schema")
    
    try:
        xmlschema.assertValid(doc)
        print ("PASS")
        case2 = True

    except etree.DocumentInvalid as err:
        print ("FAIL")  
        print ("_________________________________________________________________________________")
    
    if (case1 and case2):
        total += 1
    print ("_________________________________________________________________________________")
    
        

print ("_________________________________________________________________________________")
print ("                  • Unqualified Dublin Core Conversion Tester •                  ")
print ("_________________________________________________________________________________")
script = input("Enter the name of the Unqualified Dublin Core Conversion Script: ")
print ("_________________________________________________________________________________")
 
try:
    scriptBleekAndLloyd = False
    scriptFHYA = False
    scriptMetsemegologolo = False
    print("Importing: " + script)
    
    if (script == "FHYADCConverter.py"):
        scriptFHYA = True
        print("Running: " + script)
        import FHYADCConverter
    
    elif (script == "BleekAndLloydDCConverter.py"):
        scriptBleekAndLloyd = True
        print("Running: " + script)
        import BleekAndLloydDCConverter
    
    elif (script == "MetsemegologoloDCConverter.py"):
        scriptMetsemegologolo = True
        print("Running: " + script)
        import MetsemegologoloDCConverter
    
    else:
        raise
except:
    print("Error: "+script+" not found.")
    exit()

else:
    print ("Testing: " + script)
    path = ""
    endIndex = 0
    
    if (scriptFHYA):
        path = "FHYA Depot/"
        endIndex = 88
        
    elif (scriptBleekAndLloyd):
        path = "stories/"
        endIndex = 2058
    
    elif (scriptMetsemegologolo):
        path = "Metsemegologolo/"
        endIndex = 2
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,endIndex):   
            directoryPath = os.path.join(root, str(i))  
            if (directoryPath == path+str(i)):
                    filePath = directoryPath +'/metadata-'+str(i)+'-dc.xml'
                    with open(filePath, encoding="utf-8") as file:
                        data = file.read()
                        check(filePath, data)         
        break
    print("Report: "+str(total)+" out of "+str(endIndex-1)+" files converted successfully.")
    exit()
    
