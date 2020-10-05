#!/usr/bin/env python3
"""
DCConverterTester.py: Program that reads as input a Data Provider DC Converter and tests if the Converter can produce well-formed XML metadata,
that confroms to the (unqualified) Dublin Core schema.
Author: Alex Priscu - PRSLAE003
University of Cape Town
Project: Data Provider Interfaces component of the metadata aggregation system – HERIPORT.
Date: 1 October 2020
"""

# Import relevant packages
import os
import pprint
import sys
import unicodedata
import xmltodict

from datetime import datetime
from io import StringIO
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string

# Test that DC XML metadata record is well-formed and conforms to the (unqualified) Dublin Core schema a
def test(dcFileName):
    # Use global variable.
    global total
    
    # Set case flags.
    case1 = False
    case2 = False
    
    # Print statements.
    print ("_________________________________________________________________________________")
    print ("\n\nTesting: "+dcFileName)
    print("Case 1: Checking XML Well-Formedness")
    
    # Open (unqualified) Dublin Core schema file.
    with open("oai_dc.xsd", 'r') as schema_file:
        # Set schema_to_check to the file contents read.
        schema_to_check = schema_file.read()
    
    # Open the XML metadata record.
    with open(dcFileName, 'r') as xml_file:
        # Set xml_to_check to the file contents read.
        xml_to_check = xml_file.read()
    
    # Set xmlschema_doc.
    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    # Set xmlschema.
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    # Try to perform case 1 testing if XML is well-formed. 
    try:
        doc = etree.parse(StringIO(xml_to_check[39:len(xml_to_check)]))
        # Print statement.
        print ("PASS")
        # Set flag.
        case1 = True
    
    # Case 1 failed.
    except:
        # Print statements.
        print ("FAIL")
        print ("_________________________________________________________________________________")
    
    # Print statement.
    print("\nCase 2: Validate against Unqualified Dublin Core Schema")
    
    # Try to perform case 2 testing metadata validity against the imported Dublin Core schema file.
    try:
        xmlschema.assertValid(doc)
        # Print statement.
        print ("PASS")
        # Set flag.
        case2 = True
    
    # Case 2 failed.
    except:
        # Print statements.
        print ("FAIL")  
        print ("_________________________________________________________________________________")
    
    # If both cases passed.
    if (case1 and case2):
        # Increment total.
        total += 1
    # Print statement.
    print ("_________________________________________________________________________________")
    
# Read each DC XML metadata record of a Data Provider directory and call the test method to perfom Conformance testing on each converted XML metadata record. 
def read_records():
    # Use global variable.
    global total
    
    # Print statements.
    print ("_________________________________________________________________________________")
    print ("                  • Unqualified Dublin Core Conversion Tester •                  ")
    print ("_________________________________________________________________________________")
    
    # Get name of (unqualified) Dublin Core Converter script to run and test.
    script = input("Enter the name of the Unqualified Dublin Core Conversion Script: ")
    
    # Print statement.
    print ("_________________________________________________________________________________")
    
    # Try to run script.
    try:
        # Set flags.
        scriptBleekAndLloyd = False
        scriptFHYA = False
        scriptMetsemegologolo = False
        
        # Print statement.
        print("Importing: " + script)
        
        # If FHYA script entered.
        if (script == "FHYADCConverter.py"):
            # Set flag.
            scriptFHYA = True
            # Print statement.
            print("Running: " + script)
            # Import and run script.
            import FHYADCConverter
            FHYADCConverter.read_records()
        
        # Else if Bleek and Lloyd script entered.
        elif (script == "BleekAndLloydDCConverter.py"):
            # Set flag.
            scriptBleekAndLloyd = True
            # Print statement.
            print("Running: " + script)
            # Import and run script.
            import BleekAndLloydDCConverter
            BleekAndLloydDCConverter.read_records()
        
        # Else if Metsemegologolo script entered.
        elif (script == "MetsemegologoloDCConverter.py"):
            # Set flag.
            scriptMetsemegologolo = True
            # Print statement.
            print("Running: " + script)
            # Import and run script.
            import MetsemegologoloDCConverter
            MetsemegologoloDCConverter.read_records()
        
        # Else script name is invalid.
        else:
            # Raise error.
            raise
    
    # Script name not valid.    
    except:
        # Print error statement.
        print("Error: "+script+" not found.")
        # Exit Tester.
        exit()
    
    # Else script name valid.
    else:
        # Print statement.
        print ("Testing: " + script)
        # Set path.
        path = ""
        # Set endIndex.
        endIndex = 0
        
        # If FHYA script entered.
        if (scriptFHYA):
            # Set path to the Data Provider directory path.
            path = "FHYA Depot/"
            # Set endIndex to last collection index+1.
            endIndex = 88
        
        # Else if Bleek and Lloyd script entered.
        elif (scriptBleekAndLloyd):
             # Set path to the Data Provider directory path.
            path = "stories/"
            # Set endIndex to last collection index+1.
            endIndex = 2058
        
        # Else if Metsemegologolo script entered.
        elif (scriptMetsemegologolo):
            # Set path to the Data Provider directory path.
            path = "Metsemegologolo/"
            # Set endIndex to last collection index+1.
            endIndex = 2
        
        # Try to access each sub-folder XML metadata file in a Data Provider directory path.
        try:
            for root, directories, filenames in os.walk(path):
                # For each index of the of the Data Provider directory.
                for i in range(1, endIndex):
                    # Set index to string of current index.
                    index = str(i)
                    # Set directoryPath to the Data Provider sub-folder directory path.
                    directoryPath = os.path.join(root, index)  
                    # Set filePath to the Data Provider directory path concatenated with the index.
                    filePath = directoryPath +'/metadata-'+index+'-dc.xml'
                    # Run the test method.
                    test(filePath) 
                # Break from for loop after all files have been read and converted.         
                break
        
        # Unable test the XML metadata record.
        except Exception as e:
            # Print error statement.
            print ("Error in testing files: "+str(e))
        
        # Files tested.
        else:
            print("Report: "+str(total)+" out of "+str(endIndex-1)+" files converted successfully.")
            exit()
      
# Only run the functions if this module is run.
if __name__ == "__main__":
    # If number of args is 1.                                     
    if len(sys.argv) == 1:
        # Set total.
        total = 0
        # Run the read_records method.                                  
        read_records()
    # Else the number of args is invalid.                                         
    else:
        # Print usage statment.                                                    
        print ("Usage: python3 DCConverterTester.py")