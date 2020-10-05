#!/usr/bin/env python3
"""
FHYAOAIInterface.py: Program that acts as an OAI-PMH interface for The Five Hundred Year Archive Data Provider,
by reading in OAI-PMH requests and outputting OAI-PMH responses.
Author: Alex Priscu - PRSLAE003
University of Cape Town
Project: Data Provider Interfaces component of the metadata aggregation system – HERIPORT.
Date: 1 October 2020
"""

# Import relevant packages
import cgi
import os
import pprint
import simpledc
import xmltodict
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string

# HTTP Header, specifies the content type to be displayed on the browser screen.
print ("Content-type: text/xml\n")

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Set server URL.
serverURL = "http://emandulo.apc.uct.ac.za/metadata/FHYA%20Depot/"

# Try to get query from verb field.
try:
    query = form["verb"].value
    
    # If query is a GetRecord request.
    if (query == 'GetRecord'):
        
        # Assign set.
        set = "FHYA Depot"
        
        # Try to get identifier and metadataPrefix from form fields.
        try:
            identifier = form.getvalue ("identifier", "")
            metadataPrefix = form.getvalue ("metadataPrefix", "")
            
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if ((field != "identifier") and (field != "metadataPrefix") and (field != "verb")):
                    # Raise badArgument error.
                    raise
        
            # If identifier is repeating.
            if (type(identifier) is type([])):
                # Raise badArgument error.
                raise
            
            # If identifier is empty.
            if (identifier == ""):
                # Raise badArgument error.
                raise
            
            # If metadataPrefix is repeating.
            if (type(metadataPrefix) is type([])):
                # Raise badArgument error.
                raise
            
            # If metadataPrefix is empty.
            if (metadataPrefix == ""):
                # Raise badArgument error.
                raise
            
            # Set badChars to illegal syntax char list.
            badChars = ['\"','<','>','\'']
            # For each bad char.
            for ch in badChars:
                # If in identifier.
                if (ch in identifier):
                    # Raise badArgument error.
                    raise
                # If in metadataPrefix.
                if (ch in metadataPrefix):
                    # Raise badArgument error.
                    raise
        
        # Generate badArgument XML response.
        except:
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
            
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"GetRecord\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            # Set responseEnd.
            responseEnd = "\n</OAI-PMH>"
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
            
        # Else try to get the record file.
        else:
            try:
                splitString = "FHYA Depot/"
                split = identifier.split(splitString)
                # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
                dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                # Try to open the XML metadata record with UTF-8 encoding.
                dcFile = open(dcFilePath, "r", encoding="utf-8")
                # Set data to the file contents read.
                data = dcFile.read()
                 # Close the (unqualified) Dublin Core file.
                dcFile.close()
                
            # Generate idDoesNotExist XML response.
            except:
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                verbRequest += identifier+"\"\n           metadataPrefix=\""
                verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"idDoesNotExist\">The value of the identifier argument is unknown or illegal in this repository.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
            
            # Else check the metadataPrefix.
            else:
                try: 
                    # If metadataPrefix is not valid.
                    if (metadataPrefix != "oai_dc"):
                        # Raise cannotDisseminateFormat error.
                        raise
                
                # Generate cannotDisseminateFormat XML response.
                except:
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate.
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                    
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                    verbRequest += identifier+"\"\n           metadataPrefix=\""
                    verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    # Set responseEnd.
                    responseEnd = "\n</OAI-PMH>"
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)
                
                # Else generate XML response.
                else:
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate.
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                    
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                    verbRequest += identifier+"\"\n           metadataPrefix=\""
                    verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n  <GetRecord>\n   <record>"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    
                    # Get record date.
                    splitString = "<dc:date>"
                    split = data.split(splitString)
                    splitString = "</dc:date>"
                    split = split[1].split(splitString)
                    split = split[0].split(" ")
                    recordDate = split[0]
                    
                    # Split data to remove <dc:identifier>.
                    splitString = "<dc:identifier>"+identifier+"</dc:identifier>"
                    split = data.split(splitString)
                    
                    if (len(split) == 2):
                        part1 = split[0]
                        part1 = part1[39:len(part1)-3]
                        part2 = split[1]
                        data = part1+part2
                    
                    else:
                        part1 = split[0]
                        part1 = part1[39:len(part1)-1]
                        data = part1
                    
                    # Set data.
                    data = "    <metadata>\n      "+data+"    </metadata>"
                    # Set headerIdentifier.
                    headerIdentifier = "\n    <header>\n      <identifier>"+identifier+"</identifier>"
                    # Set headerDatestamp.
                    headerDatestamp = "\n      <datestamp>"+recordDate+"</datestamp>"
                    # Set headerSet.
                    headerSet = "\n      <setSpec>"+set+"</setSpec>\n    </header>\n"
                    
                    # Generate header.
                    header = []
                    # Append headerIdentifier.
                    header.append(headerIdentifier)
                    # Append headerDatestamp.
                    header.append(headerDatestamp)
                    # Append headerSet.
                    header.append(headerSet)
                    # Convert list header to be of type str.
                    strHead = ''.join([str(elem) for elem in header])
                    
                    # Generate record.
                    record = []
                    # Append strHead.
                    record.append(strHead)
                    # Append data.
                    record.append(data)
                    # Convert list record to be of type str.
                    strRec = ''.join([str(elem) for elem in record])
                    # Set responseEnd.
                    responseEnd = "\n  </record>\n </GetRecord>\n</OAI-PMH>"
                    # Append strRec.
                    response.append(strRec)
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)
                    
    # Else if query is a Identify request.  
    elif (query == 'Identify'):
        
        # Try to validate form fields.
        try:
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if (field != "verb"):
                    # Raise badArgument error.
                    raise
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
        
        # Generate badArgument XML response.
        except:
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
            
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"Identify\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            # Set responseEnd.
            responseEnd = "\n</OAI-PMH>"
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
        
        # Else generate XML response.
        else:
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"Identify\">"
            verbRequest += serverURL+"</request>\n  <Identify>\n"
            
            # Set repositoryName.
            repositoryName = "The Five Hundred Year Archive"
            # Set repositoryIdentifier.
            repositoryIdentifier = "http://emandulo.apc.uct.ac.za/"
            # Set earliestDatestamp.
            earliestDatestamp = str(datetime.now())
            
            # Set path to the Data Provider directory path.
            path = "FHYA Depot/"
            
            # Try to access each sub-folder XML metadata file in a Data Provider directory path.
            for root, directories, filenames in os.walk(path):
                # For each index of the of the Data Provider directory.
                for i in range(1, 88):
                    # Set identifier.
                    identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                                
                    splitString = "FHYA Depot/"
                    split = identifier.split(splitString)
                    # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
                    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                    
                    # Try to open the XML metadata record with UTF-8 encoding.
                    try:
                        dcFile = open(dcFilePath, "r", encoding="utf-8")
                        # Set data to the file contents read.
                        data = dcFile.read()
                        # Close the (unqualified) Dublin Core file.
                        dcFile.close()
                    # Unable to open the XML metadata record.
                    except Exception as e:
                        # Print error statement.
                        print(e)
                    
                    # Get record date.
                    splitString = "<dc:date>"
                    split = data.split(splitString)
                    splitString = "</dc:date>"
                    split = split[1].split(splitString)
                    split = split[0].split(" ")
                    recordDate = split[0]
                    
                    # If recordDate earlier than earliestDatestamp.
                    if ((recordDate <= earliestDatestamp)):
                        # Set earliestDatestamp to recordDate.
                        earliestDatestamp = recordDate
                # Break from for loop after all files have been read.   
                break
            
            # Set data.
            data = "    <repositoryName>"+repositoryName+"</repositoryName>"
            data += "\n    <baseURL>"+serverURL+"</baseURL>"
            data += "\n    <protocolVersion>2.0</protocolVersion>"
            data += "\n    <adminEmail>prsale003@myuct.ac.za</adminEmail>"
            data += "\n    <earliestDatestamp>"+earliestDatestamp+"</earliestDatestamp>"
            data += "\n    <deletedRecord>no</deletedRecord>"
            data += "\n    <granularity>YYYY-MM-DD</granularity>"
            
            data += "\n    <description>\n      <oai-identifier"
            data += "\n       xmlns:oai_dc=\"http://www.openarchives.org/OAI/2.0/oai-identifier\"\n       xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n       xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/oai-identifier\n          http://www.openarchives.org/OAI/2.0/oai-identifier.xsd\">"
            data += "\n       <scheme>oai</scheme>"
            data += "\n       <repositoryIdentifier>oai</repositoryIdentifier>"
            data += "\n       </oai-identifier>\n    </description>"
            
            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            
            # Generate record.
            record = []
            # Append data.
            record.append(data)
            # Convert list record to be of type str.
            strRec = ''.join([str(elem) for elem in record])
            # Set responseEnd.
            responseEnd = "\n  </Identify>\n</OAI-PMH>"
            # Append strRec.
            response.append(strRec)
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
    
    # Else if query is a ListIdentifiers request.     
    elif (query == 'ListIdentifiers'):
        
        # Set OAI-PMH keyword flags.
        fromFlag = False
        untilFlag = False
        metadataPrefixFlag = False
        setFlag = False
        resumptionTokenFlag = False
        
        # Set OAI-PMH keyword values.
        frm = ""
        until = ""
        metadataPrefix = ""
        set = ""
        resumptionToken = ""
        
        # Try to validate form fields.
        try:
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if ((field != "metadataPrefix") and (field != "verb") and (field != "set") and (field != "from") and (field != "until") and (field != "resumptionToken")):
                    # Raise badArgument error.
                    raise
            
            # Check if fields entered.
            for field in form:
                # If metadataPrefix entered.
                if (field == "metadataPrefix"):
                    # Set flag.
                    metadataPrefixFlag = True
                
                # If resumptionToken entered.
                if (field == "resumptionToken"):
                    # Set flag.
                    resumptionTokenFlag = True
                
                # If from entered.
                if (field == "from"):
                    # Set flag.
                    fromFlag = True
                
                # If until entered.
                if (field == "until"):
                    # Set flag.
                    untilFlag = True
                
                # If set entered.
                if (field == "set"):
                    # Set flag.
                    setFlag = True
                
            # If exclusive arguments entered together.
            if ((metadataPrefixFlag or fromFlag or untilFlag or setFlag) and resumptionTokenFlag):
                # Raise badArgument error.
                raise
                
            # If resumptionToken entered.
            if (resumptionTokenFlag):
                
                # Get resumptionToken form field values.
                resumptionToken = form.getvalue ("resumptionToken", "")
                # Split resumptionToken value
                resumptionTokenSplit = resumptionToken.split(',')
                
                # Set resumptionToken frm and until flags.
                resumptionTokenFromFlag = False
                resumptionTokenUntilFlag = False
                
                # Set resumptionToken frm and until values.
                resumptionTokenFrom = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                resumptionTokenUntil = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                
                # Set resumptionToken set flag.
                resumptionTokenSetFlag = False
                
                # Assign resumptionToken set value.
                resumptionTokenSet = "set"
                
                # Get resumptionTokenNextIndex value.
                resumptionTokenNextIndex = resumptionTokenSplit[0]
                
                # Get resumptionTokenExpirationDate value.
                resumptionTokenExpirationDate = resumptionTokenSplit[1][1:len(resumptionTokenSplit[1])]
                
                # Get resumptionTokenMetadataPrefix value.
                resumptionTokenMetadataPrefix = resumptionTokenSplit[2]
                
                # If more than 6 fields in resumptionToken value.
                if (len(resumptionTokenSplit) > 6):
                    # Raise badResumptionToken error.
                    raise
                
                # If 6 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 6):
                    
                    # Set resumptionToken flags.
                    resumptionTokenFromFlag = True
                    resumptionTokenUntilFlag = True
                    resumptionTokenSetFlag = True
                    
                    # Get resumptionToken values.
                    resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                    resumptionTokenSet = resumptionTokenSplit[5]
                
                # If 5 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 5):
                    # Get a resumptionToken field.
                    field = resumptionTokenSplit[3][0:1]

                    # If field prefix is f. 
                    if (field == 'f'):
                        # Set resumptionTokenFromFlag flag.
                        resumptionTokenFromFlag = True
                        # Get resumptionTokenFrom value.
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        # Get a resumptionToken field.
                        field = resumptionTokenSplit[4][0:1]

                        # If field prefix is u. 
                        if (field == 'u'):
                            # Set resumptionTokenUntilFlag flag.
                            resumptionTokenUntilFlag = True
                            # Get resumptionTokenUntil value.
                            resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                        
                        # Else field is set.
                        else:
                            # Set resumptionTokenSetFlag flag.
                            resumptionTokenSetFlag = True
                            # Get resumptionTokenSet value.
                            resumptionTokenSet = resumptionTokenSplit[4]
                    
                    # If field prefix is u.
                    if (field == 'u'):
                        # Set resumptionTokenUntilFlag flag.
                        resumptionTokenUntilFlag = True
                        # Get resumptionTokenUntil value.
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        # Set resumptionTokenSetFlag flag.
                        resumptionTokenSetFlag = True
                        # Get resumptionTokenSet value.
                        resumptionTokenSet = resumptionTokenSplit[4]
                
                # If 4 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 4):
                    # Get a resumptionToken field.
                    field = resumptionTokenSplit[3][0:1]
                    
                    # If field prefix is f.
                    if (field == 'f'):
                        # Set resumptionTokenFromFlag flag.
                        resumptionTokenFromFlag = True
                        # Get resumptionTokenFrom value.
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    
                    # Else if field prefix is u.
                    elif (field == 'u'):
                        # Set resumptionTokenUntilFlag flag.
                        resumptionTokenUntilFlag = True
                        # Get resumptionTokenUntil value.
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    
                    # Else field is set.
                    else:
                        # Set resumptionTokenSetFlag flag.
                        resumptionTokenSetFlag = True
                        # Get resumptionTokenSet value.
                        resumptionTokenSet = resumptionTokenSplit[3]
                
                # If resumptionTokenNextIndex is smaller than 1.
                if (int(resumptionTokenNextIndex) < 1):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenSplit second field is not prefixed with e.
                if (resumptionTokenSplit[1][0:1] != "e"):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenExpirationDate does not have a date format.
                if (resumptionTokenExpirationDate != datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenMetadataPrefix not valid.
                if (resumptionTokenMetadataPrefix != "oai_dc"):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionToken has a frm value.
                if (resumptionTokenFromFlag): 
                    # If resumptionTokenFrom does not have a date format.
                    if (resumptionTokenFrom != datetime.strptime(resumptionTokenFrom, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badResumptionToken error.
                        raise
                
                # If resumptionToken has a until value.
                if (resumptionTokenUntilFlag):
                    # If resumptionTokenUntil does not have a date format.
                    if (resumptionTokenUntil != datetime.strptime(resumptionTokenUntil, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badResumptionToken error.
                        raise
                
                if (resumptionTokenSetFlag):
                    if (resumptionTokenSet != "FHYA Depot"):
                        # Raise badResumptionToken error.
                        raise
                
                # Get resumptionToken expiration date object and current date object.
                resumptionTokenExpirationDateObject = datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%SZ')
                currentDate = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                currentDateObject = datetime.strptime(currentDate, '%Y-%m-%dT%H:%M:%SZ')
                
                # If resumptionToken expiration date object is less than current date object.
                if (resumptionTokenExpirationDateObject <= currentDateObject):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionToken frm field entered.
                if (resumptionTokenFromFlag):
                    # Set frm.
                    frm = resumptionTokenFrom
                    # Set flag.
                    fromFlag = True
                # Else resumptionToken frm field not entered.
                else:
                    # Set frm.
                    frm = "2020-01-01"
                
                # If resumptionToken until field entered.
                if (resumptionTokenUntilFlag):
                    # Set until.
                    until = resumptionTokenUntil
                    # Set flag.
                    untilFlag = True
                # Else resumptionToken until field not entered.
                else:
                    # Set until.
                    until = datetime.today().strftime('%Y-%m-%d')
                    
                # Set metadataPrefix.
                metadataPrefix = resumptionTokenMetadataPrefix
                
                # If resumptionToken set field entered.
                if (resumptionTokenSetFlag):
                    # Assign set.
                    set = resumptionTokenSet
                    # Set flag.
                    setFlag = True
                # Else resumptionToken set field not entered.
                else:
                    # Assign set.
                    set = "FHYA Depot"
                
                # Get frm and until date objects.
                frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                
                # If frm data object is greater than until date object.
                if (frmDateObject > untilDateObject):
                    # Raise badResumptionToken error.
                    raise
                
                # Set badChars to illegal syntax char list.
                badChars = ['\"','<','>','\'']
                # For each bad char.
                for ch in badChars:
                    # If in metadataPrefix.
                    if (ch in metadataPrefix):
                    # Raise badResumptionToken error.   
                        raise
                    # If in set.
                    if (ch in set):
                    # Raise badResumptionToken error.
                        raise
            # Else no resumptionToken entered.
            else:
                # Get OAI-PMH form field values.
                metadataPrefix = form.getvalue ("metadataPrefix", "")
                frm = form.getvalue ("from", "")
                until = form.getvalue ("until", "")
                set = form.getvalue ("set", "")

                # If metadataPrefix is of type list.
                if (type(metadataPrefix) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If metadataPrefix is empty.
                if (metadataPrefix == ""):
                    # Raise badArgument error.
                    raise
                
                # If frm is of type list.
                if (type(frm) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If frm is not empty.
                if (frm != ""):
                    # If frm does not have a date format.
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badArgument error.
                        raise
                    # Set flag.
                    fromFlag = True
                # Else frm is empty.
                else:
                    # Set frm.
                    frm = "2020-01-01"
                
                # If until is of type list.
                if (type(until) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If until is not empty.
                if (until != ""):
                    # If until does not have a date format.
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badArgument error.
                        raise
                    # Set flag.
                    untilFlag = True
                # Else until is empty.
                else:
                    # Set until.
                    until = datetime.today().strftime('%Y-%m-%d')
                
                # If set is of type list.
                if (type(set) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If set is empty.
                if (set == ""):
                    # Assign set.
                    set = "FHYA Depot"
                # Else set is not empty.   
                else:
                    # Set flag.
                    setFlag = True
                
                # If resumptionToken is not entered.
                if (metadataPrefixFlag):
                    
                    # Get frm and until date objects.
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    # If frm date is greater than until date.
                    if (frmDateObject > untilDateObject):
                        # Raise badArgument error.
                        raise
                    
                    # Set badChars to illegal syntax char list.
                    badChars = ['\"','<','>','\'']
                    # For each bad char.
                    for ch in badChars:
                        # If in metadataPrefix.
                        if (ch in metadataPrefix):
                            # Raise badArgument error.
                            raise
                        # If in set.
                        if (ch in set):
                            # Raise badArgument error.
                            raise
        # Generate XML response.
        except:
            # If only resumptionToken entered.
            if (resumptionTokenFlag and not metadataPrefixFlag):
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListIdentifiers\""
                verbRequest += " resumptionToken=\""+resumptionToken+"\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badResumptionToken\">The value of the resumptionToken argument is invalid or expired.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
            
            # Generate badArgument XML response.
            else:
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListIdentifiers\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
        
        # Generate XML response.
        else:
            # Try to validate metadataPrefix.
            try:
                # If metadataPrefix is not valid.
                if (metadataPrefix != "oai_dc"):
                    # Raise cannotDisseminateFormat error.
                    raise
            # Generate cannotDisseminateFormat XML response.
            except:
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.     
                verbRequest = "\n  <request verb=\"ListIdentifiers\""
                
                # If resumptionToken entered.
                if (resumptionTokenFlag):
                    # Set verbRequest. 
                    verbRequest += " resumptionToken=\""+resumptionToken+"\""
                # Else no resumptionToken entered.
                else:
                    # If frm field entered.
                    if (fromFlag):
                        # Set verbRequest. 
                        verbRequest += " from=\""+frm+"\""
                    
                    # If until field entered.
                    if (untilFlag):
                        # Set verbRequest. 
                        verbRequest += " until=\""+until+"\""
                    
                    # Set verbRequest. 
                    verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                    
                    # If set field entered.
                    if (setFlag):
                        # Set verbRequest. 
                        verbRequest += " set=\""+set+"\""
                
                # Set verbRequest. 
                verbRequest += ">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
            
            # Else try to validate set.
            else:
                try:
                    # If set not valid.
                    if (set != "FHYA Depot"):
                        # Raise noRecordsMatch error.
                        raise
                    
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate.
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                    
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"ListIdentifiers\""
                    
                    # Set path to the Data Provider directory path.
                    path = "FHYA Depot/"
                    # Set count.
                    count = 0
                    # Set startFile
                    startFile = 1
                    # Set startIndex.
                    startIndex = 1
                    # Set endIndex.
                    endIndex = 11
                    # Set complete.
                    complete = False
                    
                    # If resumptionToken entered.
                    if (resumptionTokenFlag):
                        # Set startIndex.
                        startIndex = int(resumptionTokenNextIndex)
                        
                        # Set endIndex and complete based on value.
                        if (endIndex < 87):
                            endIndex = startIndex+10
                        
                        if (endIndex > 87):
                            complete = True
                            endIndex = 88
                        
                        # Set verbRequest.
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                    # Else no resumptionToken entered.
                    else:
                        # If frm field entered.
                        if (fromFlag):
                            # Set verbRequest.
                            verbRequest += " from=\""+frm+"\""
                        
                        # If until field entered.
                        if (untilFlag):
                            # Set verbRequest.
                            verbRequest += " until=\""+until+"\""

                        # Set verbRequest.
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""

                        # If set field entered.
                        if (setFlag):
                            # Set verbRequest.
                            verbRequest += " set=\""+set+"\""
                    
                    # Set verbRequest.
                    verbRequest += ">"+serverURL+"</request>\n  <ListIdentifiers>\n"
                    
                    # Try to access each sub-folder XML metadata file in a Data Provider directory path.
                    for root, directories, filenames in os.walk(path):
                        # For each index of the of the Data Provider directory.
                        for i in range(startIndex, endIndex):
                            # Set identifier.
                            identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                            
                            # Generate response.
                            response = []
                            
                            # If first record.
                            if (startFile == 1):
                                # Append verbResponseHeader.
                                response.append(verbResponseHeader)
                                # Append verbResponseDate.
                                response.append(verbResponseDate)
                                #Append verbRequest.
                                response.append(verbRequest)
                
                            splitString = "FHYA Depot/"
                            split = identifier.split(splitString)
                            # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
                            dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                            
                            # Try to open the XML metadata record with UTF-8 encoding.
                            try:
                                dcFile = open(dcFilePath, "r", encoding="utf-8")
                                # Set data to the file contents read.
                                data = dcFile.read()
                                # Close the (unqualified) Dublin Core file.
                                dcFile.close()
                            # Unable to open the XML metadata record.
                            except Exception as e:
                                # Print error statement.
                                print(e)
                            
                            # Get record date.
                            splitString = "<dc:date>"
                            split = data.split(splitString)
                            splitString = "</dc:date>"
                            split = split[1].split(splitString)
                            split = split[0].split(" ")
                            recordDate = split[0]
                            
                            # Get record, frm and until date objects.
                            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
                            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                            
                            # If recordDateObject is greater than frmDateObject and less than untilDateObject.
                            if ((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                                # Increment count.
                                count += 1
                                
                                # Set headerIdentifier.
                                headerIdentifier = "   <header>\n      <identifier>"+identifier+"</identifier>"
                                # Set headerDatestamp.
                                headerDatestamp = "\n      <datestamp>"+recordDate+"</datestamp>"
                                # Set headerSetSpec.
                                headerSetSpec = "\n      <setSpec>"+set+"</setSpec>"
                                headerSetSpec +=  "\n   </header>"
                                
                                # Generate header.
                                header = []
                                # Append headerIdentifier.
                                header.append(headerIdentifier)
                                # Append headerDatestamp.
                                header.append(headerDatestamp)
                                # Append headerSetSpec.
                                header.append(headerSetSpec)
                                # Convert list header to be of type str.
                                strHead = ''.join([str(elem) for elem in header]) 
                                
                                # Generate record.
                                record = []
                                # Append strHead.
                                record.append(strHead)
                                # Convert list record to be of type str.
                                strRec = ''.join([str(elem) for elem in record]) 
                                # Append strRec.
                                response.append(strRec)
                                # Convert list response to be of type str.
                                strResp = ''.join([str(elem) for elem in response])
                                # Print response.
                                print(strResp)
                            
                            # Else skip record.
                            else:
                                pass
                            
                            # Increment startFile.
                            startFile += 1
                            
                        # If count is zero.
                        if (count == 0):
                            # Raise noRecordsMatch error.
                            raise
                        
                        # Set estimated completeListSize.
                        completeListSize = 87
                        # Set nextIndex.
                        nextIndex = endIndex
                        # Set expirationDate.
                        expirationDate = datetime.now() + timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
                        
                        # Set resumptionToken.
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\""
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " expirationDate="+"\""+expirationDate.strftime('%Y-%m-%dT%H:%M:%SZ')+"\""
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\">"
                        
                        # If response list is not complete.
                        if (complete == False):
                            
                            # Set tokenString.
                            tokenString = str(nextIndex)
                            tokenString += ",e"+expirationDate.strftime('%Y-%m-%dT%H:%M:%SZ')
                            tokenString += ","+metadataPrefix
                            
                            # If frm field entered.
                            if (fromFlag):
                                # Set tokenString.
                                tokenString += ",f"+frm
                            
                            # If until field entered.
                            if (untilFlag):
                                # Set tokenString.
                                tokenString += ",u"+until
                            
                            # If set field entered.
                            if (setFlag):
                                # Set tokenString.
                                tokenString += ","+set                    
                            
                            # Set resumptionToken.
                            resumptionToken += tokenString
                        
                        # Set resumptionToken.
                        resumptionToken += "</resumptionToken>\n"
                        # Set responseEnd.
                        responseEnd = "   "+resumptionToken
                        responseEnd += " </ListIdentifiers>\n</OAI-PMH>"
                        # Print response.
                        print(responseEnd)
                        # Break from for loop after all files have been read. 
                        break
                
                # Generate noRecordsMatch XML response.
                except:
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate.
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                            
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"ListIdentifiers\""
                    
                    # If resumptionToken entered.
                    if (resumptionTokenFlag):
                        # Set verbRequest.
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                    
                    # Else no resumptionToken entered. 
                    else:
                        # If frm field entered.
                        if (fromFlag):
                            # Set verbRequest.
                            verbRequest += " from=\""+frm+"\""
                        
                        # If until field entered.
                        if (untilFlag):
                            # Set verbRequest.
                            verbRequest += " until=\""+until+"\""
                        
                        # Set verbRequest.
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                        
                        # If set field entered.
                        if (setFlag):
                            # Set verbRequest.
                            verbRequest += " set=\""+set+"\""
                    
                    # Set verbRequest.
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"noRecordsMatch\">The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.</error>"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    # Set responseEnd.
                    responseEnd = "\n</OAI-PMH>"
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)
    
    # Else if query is a ListMetadataFormats request.    
    elif (query == 'ListMetadataFormats'):
        # Try to get identifier from form fields.
        try:
            identifier = form.getvalue ("identifier", "")
            
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if ((field != "verb") and (field != "identifier")):
                    # Raise badArgument error.
                    raise
            
            # If identifier is repeating. 
            if (type(identifier) is type([])):
                raise
            
            # Set badChars to illegal syntax char list.
            badChars = ['\"','<','>','\'']
            # For each bad char.
            for ch in badChars:
                # If in identifier.
                if (ch in identifier):
                    # Raise badArgument error.
                    raise
            
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
        
        # Generate badArgument XML response.
        except:   
            # Set verbResponseHeader.         
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
            
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"ListMetadataFormats\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
                        
            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            # Set responseEnd.
            responseEnd = "\n</OAI-PMH>"
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
        
        # Else generate XML response.
        else:
            # Try to get identifier from form vields.
            try:
                if (identifier == ""):
                    # Raise exception.
                    raise
            
            # Generate XML response without identifier.
            except:
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListMetadataFormats\">"
                verbRequest += serverURL+"</request>\n  <ListMetadataFormats>\n"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                
                # Set data.
                data = "    <metadataPrefix>oai_dc</metadataPrefix>\n     <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>\n     <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>"
                data = "   <metadataFormat>\n"+data+"\n   </metadataFormat>"
                
                # Generate record.
                record = []
                # Append data.
                record.append(data)
                # Convert list record to be of type str.
                strRec = ''.join([str(elem) for elem in record])
                # Set responseEnd.
                responseEnd = "\n  </ListMetadataFormats>\n</OAI-PMH>"
                # Append strRec.
                response.append(strRec)
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)  
            
            # Else try to get the record file.
            else:
                try:
                    splitString = "FHYA Depot/"
                    split = identifier.split(splitString)
                    # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
                    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                    # Try to open the XML metadata record with UTF-8 encoding.
                    dcFile = open(dcFilePath, "r", encoding="utf-8")
                    # Set data to the file contents read.
                    data = dcFile.read()
                    # Close the (unqualified) Dublin Core file.
                    dcFile.close()
                    
                # Generate idDoesNotExist XML response.
                except:
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"ListMetadataFormats\""
                    verbRequest += " identifier=\""+identifier+"\""
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"idDoesNotExist\">The value of the identifier argument is unknown or illegal in this repository.</error>"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    # Set responseEnd.
                    responseEnd = "\n</OAI-PMH>"
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)
                
                # Else generate XML response.
                else:
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"ListMetadataFormats\""
                    verbRequest += " identifier=\""+identifier+"\""
                    verbRequest += ">"+serverURL+"</request>\n  <ListMetadataFormats>\n"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    
                    # Set data.
                    data = "     <metadataPrefix>oai_dc</metadataPrefix>\n     <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>\n     <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>"
                    data = "   <metadataFormat>\n"+data+"\n   </metadataFormat>"
                    
                    # Generate record.
                    record = []
                    # Append data.
                    record.append(data)
                    # Convert list record to be of type str.
                    strRec = ''.join([str(elem) for elem in record])
                    # Set responseEnd.
                    responseEnd = "\n </ListMetadataFormats>\n</OAI-PMH>"
                    # Append strRec.
                    response.append(strRec)
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)         
    
    # Else if query is a ListRecords request.  
    elif (query == 'ListRecords'):
        
        # Set OAI-PMH keyword flags.
        fromFlag = False
        untilFlag = False
        metadataPrefixFlag = False
        setFlag = False
        resumptionTokenFlag = False
        
        # Set OAI-PMH keyword values.
        frm = ""
        until = ""
        metadataPrefix = ""
        set = ""
        resumptionToken = ""
        
        # Try to validate form fields.
        try:
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if ((field != "metadataPrefix") and (field != "verb") and (field != "set") and (field != "from") and (field != "until") and (field != "resumptionToken")):
                    # Raise badArgument error.
                    raise
            
            # Check if fields entered.
            for field in form:
                # If metadataPrefix entered.
                if (field == "metadataPrefix"):
                    # Set flag.
                    metadataPrefixFlag = True
                
                # If resumptionToken entered.
                if (field == "resumptionToken"):
                    # Set flag.
                    resumptionTokenFlag = True
                
                # If from entered.
                if (field == "from"):
                    # Set flag.
                    fromFlag = True
                
                # If until entered.
                if (field == "until"):
                    # Set flag.
                    untilFlag = True
                
                # If set entered.
                if (field == "set"):
                    # Set flag.
                    setFlag = True
                
            # If exclusive arguments entered together.
            if ((metadataPrefixFlag or fromFlag or untilFlag or setFlag) and resumptionTokenFlag):
                # Raise badArgument error.
                raise
                        
            # If resumptionToken entered.
            if (resumptionTokenFlag):
                
                # Get resumptionToken form field values.
                resumptionToken = form.getvalue ("resumptionToken", "")
                # Split resumptionToken value
                resumptionTokenSplit = resumptionToken.split(',')
                
                # Set resumptionToken frm and until flags.
                resumptionTokenFromFlag = False
                resumptionTokenUntilFlag = False
                
                # Set resumptionToken frm and until values.
                resumptionTokenFrom = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                resumptionTokenUntil = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                
                # Set resumptionToken set flag.
                resumptionTokenSetFlag = False
                
                # Assign resumptionToken set value.
                resumptionTokenSet = "set"
                
                # Get resumptionTokenNextIndex value.
                resumptionTokenNextIndex = resumptionTokenSplit[0]
                
                # Get resumptionTokenExpirationDate value.
                resumptionTokenExpirationDate = resumptionTokenSplit[1][1:len(resumptionTokenSplit[1])]
                
                # Get resumptionTokenMetadataPrefix value.
                resumptionTokenMetadataPrefix = resumptionTokenSplit[2]
                
                # If more than 6 fields in resumptionToken value.
                if (len(resumptionTokenSplit) > 6):
                    # Raise badResumptionToken error.
                    raise
                
                # If 6 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 6):
                    
                    # Set resumptionToken flags.
                    resumptionTokenFromFlag = True
                    resumptionTokenUntilFlag = True
                    resumptionTokenSetFlag = True
                    
                    # Get resumptionToken values.
                    resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                    resumptionTokenSet = resumptionTokenSplit[5]
                
                # If 5 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 5):
                    # Get a resumptionToken field.
                    field = resumptionTokenSplit[3][0:1]

                    # If field prefix is f. 
                    if (field == 'f'):
                        # Set resumptionTokenFromFlag flag.
                        resumptionTokenFromFlag = True
                        # Get resumptionTokenFrom value.
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        # Get a resumptionToken field.
                        field = resumptionTokenSplit[4][0:1]

                        # If field prefix is u. 
                        if (field == 'u'):
                            # Set resumptionTokenUntilFlag flag.
                            resumptionTokenUntilFlag = True
                            # Get resumptionTokenUntil value.
                            resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                        
                        # Else field is set.
                        else:
                            # Set resumptionTokenSetFlag flag.
                            resumptionTokenSetFlag = True
                            # Get resumptionTokenSet value.
                            resumptionTokenSet = resumptionTokenSplit[4]
                    
                    # If field prefix is u.
                    if (field == 'u'):
                        # Set resumptionTokenUntilFlag flag.
                        resumptionTokenUntilFlag = True
                        # Get resumptionTokenUntil value.
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        # Set resumptionTokenSetFlag flag.
                        resumptionTokenSetFlag = True
                        # Get resumptionTokenSet value.
                        resumptionTokenSet = resumptionTokenSplit[4]
                
                # If 4 fields in resumptionToken value.
                if (len(resumptionTokenSplit) == 4):
                    # Get a resumptionToken field.
                    field = resumptionTokenSplit[3][0:1]
                    
                    # If field prefix is f.
                    if (field == 'f'):
                        # Set resumptionTokenFromFlag flag.
                        resumptionTokenFromFlag = True
                        # Get resumptionTokenFrom value.
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    
                    # Else if field prefix is u.
                    elif (field == 'u'):
                        # Set resumptionTokenUntilFlag flag.
                        resumptionTokenUntilFlag = True
                        # Get resumptionTokenUntil value.
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    
                    # Else field is set.
                    else:
                        # Set resumptionTokenSetFlag flag.
                        resumptionTokenSetFlag = True
                        # Get resumptionTokenSet value.
                        resumptionTokenSet = resumptionTokenSplit[3]
                
                # If resumptionTokenNextIndex is smaller than 1.
                if (int(resumptionTokenNextIndex) < 1):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenSplit second field is not prefixed with e.
                if (resumptionTokenSplit[1][0:1] != "e"):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenExpirationDate does not have a date format.
                if (resumptionTokenExpirationDate != datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ')):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionTokenMetadataPrefix not valid.
                if (resumptionTokenMetadataPrefix != "oai_dc"):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionToken has a frm value.
                if (resumptionTokenFromFlag): 
                    # If resumptionTokenFrom does not have a date format.
                    if (resumptionTokenFrom != datetime.strptime(resumptionTokenFrom, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badResumptionToken error.
                        raise
                
                # If resumptionToken has a until value.
                if (resumptionTokenUntilFlag):
                    # If resumptionTokenUntil does not have a date format.
                    if (resumptionTokenUntil != datetime.strptime(resumptionTokenUntil, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badResumptionToken error.
                        raise
                
                if (resumptionTokenSetFlag):
                    if (resumptionTokenSet != "FHYA Depot"):
                        # Raise badResumptionToken error.
                        raise
                
                # Get resumptionToken expiration date object and current date object.
                resumptionTokenExpirationDateObject = datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%SZ')
                currentDate = datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                currentDateObject = datetime.strptime(currentDate, '%Y-%m-%dT%H:%M:%SZ')
                
                # If resumptionToken expiration date object is less than current date object.
                if (resumptionTokenExpirationDateObject <= currentDateObject):
                    # Raise badResumptionToken error.
                    raise
                
                # If resumptionToken frm field entered.
                if (resumptionTokenFromFlag):
                    # Set frm.
                    frm = resumptionTokenFrom
                    # Set flag.
                    fromFlag = True
                # Else resumptionToken frm field not entered.
                else:
                    # Set frm.
                    frm = "2020-01-01"
                
                # If resumptionToken until field entered.
                if (resumptionTokenUntilFlag):
                    # Set until.
                    until = resumptionTokenUntil
                    # Set flag.
                    untilFlag = True
                # Else resumptionToken until field not entered.
                else:
                    # Set until.
                    until = datetime.today().strftime('%Y-%m-%d')
                    
                # Set metadataPrefix.
                metadataPrefix = resumptionTokenMetadataPrefix
                
                # If resumptionToken set field entered.
                if (resumptionTokenSetFlag):
                    # Assign set.
                    set = resumptionTokenSet
                    # Set flag.
                    setFlag = True
                # Else resumptionToken set field not entered.
                else:
                    # Assign set.
                    set = "FHYA Depot"
                
                # Get frm and until date objects.
                frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                
                # If frm data object is greater than until date object.
                if (frmDateObject > untilDateObject):
                    # Raise badResumptionToken error.
                    raise
                
                # Set badChars to illegal syntax char list.
                badChars = ['\"','<','>','\'']
                # For each bad char.
                for ch in badChars:
                    # If in metadataPrefix.
                    if (ch in metadataPrefix):
                    # Raise badResumptionToken error.   
                        raise
                    # If in set.
                    if (ch in set):
                    # Raise badResumptionToken error.
                        raise
            # Else no resumptionToken entered.
            else:
                # Get OAI-PMH form field values.
                metadataPrefix = form.getvalue ("metadataPrefix", "")
                frm = form.getvalue ("from", "")
                until = form.getvalue ("until", "")
                set = form.getvalue ("set", "")

                # If metadataPrefix is of type list.
                if (type(metadataPrefix) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If metadataPrefix is empty.
                if (metadataPrefix == ""):
                    # Raise badArgument error.
                    raise
                
                # If frm is of type list.
                if (type(frm) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If frm is not empty.
                if (frm != ""):
                    # If frm does not have a date format.
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badArgument error.
                        raise
                    # Set flag.
                    fromFlag = True
                # Else frm is empty.
                else:
                    # Set frm.
                    frm = "2020-01-01"
                
                # If until is of type list.
                if (type(until) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If until is not empty.
                if (until != ""):
                    # If until does not have a date format.
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        # Raise badArgument error.
                        raise
                    # Set flag.
                    untilFlag = True
                # Else until is empty.
                else:
                    # Set until.
                    until = datetime.today().strftime('%Y-%m-%d')
                
                # If set is of type list.
                if (type(set) is type([])):
                    # Raise badArgument error.
                    raise
                
                # If set is empty.
                if (set == ""):
                    # Assign set.
                    set = "FHYA Depot"
                # Else set is not empty.   
                else:
                    # Set flag.
                    setFlag = True
                
                # If resumptionToken is not entered.
                if (metadataPrefixFlag):
                    
                    # Get frm and until date objects.
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    # If frm date is greater than until date.
                    if (frmDateObject > untilDateObject):
                        # Raise badArgument error.
                        raise
                    
                    # Set badChars to illegal syntax char list.
                    badChars = ['\"','<','>','\'']
                    # For each bad char.
                    for ch in badChars:
                        # If in metadataPrefix.
                        if (ch in metadataPrefix):
                            # Raise badArgument error.
                            raise
                        # If in set.
                        if (ch in set):
                            # Raise badArgument error.
                            raise
        
        # Generate XML response.
        except:
            # If only resumptionToken entered.
            if (resumptionTokenFlag and not metadataPrefixFlag):
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListRecords\""
                verbRequest += " resumptionToken=\""+resumptionToken+"\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badResumptionToken\">The value of the resumptionToken argument is invalid or expired.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
            
            # Generate badArgument XML response.
            else:
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListRecords\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
                
        # Generate XML response.    
        else:
            # Try to validate metadataPrefix.
            try:
                # If metadataPrefix is not valid.
                if (metadataPrefix != "oai_dc"):
                    # Raise cannotDisseminateFormat error.
                    raise
            
            # Generate cannotDisseminateFormat XML response.
            except:
                # Set verbResponseHeader.
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                
                # Set verbResponseDate.
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                verbResponseDate += "</responseDate>"
                
                # Set verbRequest.
                verbRequest = "\n  <request verb=\"ListRecords\""
                
                # If resumptionToken entered.
                if (resumptionTokenFlag):
                    # Set verbRequest.
                    verbRequest += " resumptionToken=\""+resumptionToken+"\""
                # Else no resumptionToken entered.
                else:
                    # If frm field entered.
                    if (fromFlag):
                        # Set verbRequest.
                        verbRequest += " from=\""+frm+"\""
                    
                    # If until field entered.
                    if (untilFlag):
                        # Set verbRequest.
                        verbRequest += " until=\""+until+"\""
                    
                    # If set field entered.
                    if (setFlag):
                        # Set verbRequest.
                        verbRequest += " set=\""+set+"\""
                    
                    # Set verbRequest.
                    verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                
                # Set verbRequest.
                verbRequest += ">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                
                # Generate response.
                response = []
                # Append verbResponseHeader.
                response.append(verbResponseHeader)
                # Append verbResponseDate.
                response.append(verbResponseDate)
                # Append verbRequest.
                response.append(verbRequest)
                # Set responseEnd.
                responseEnd = "\n</OAI-PMH>"
                # Append responseEnd.
                response.append(responseEnd)
                # Convert list response to be of type str.
                strResp = ''.join([str(elem) for elem in response])
                # Print response.
                print(strResp)
            
            # Else try to validate set.       
            else:
                try:
                    # If set not valid.
                    if (set != "FHYA Depot"):
                        # Raise noRecordsMatch error.
                        raise
                    
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                    
                    # Set verbRequest. 
                    verbRequest = "\n  <request verb=\"ListRecords\""
                    
                    # Set path to the Data Provider directory path.
                    path = "FHYA Depot/"
                    # Set count.
                    count = 0
                    # Set startFile
                    startFile = 1
                    # Set startIndex.
                    startIndex = 1
                    # Set endIndex.
                    endIndex = 11
                    # Set complete.
                    complete = False
                    
                    # If resumptionToken entered.
                    if (resumptionTokenFlag):
                        # Set startIndex.
                        startIndex = int(resumptionTokenNextIndex)
                        
                        # Set endIndex and complete based on value.
                        if (endIndex < 87):
                            endIndex = startIndex+10
                        
                        if (endIndex > 87):
                            complete = True
                            endIndex = 88
                        
                        # Set verbRequest.
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                    
                    # Else no resumptionToken entered.
                    else:
                        # If frm field entered.
                        if (fromFlag):
                            # Set verbRequest.
                            verbRequest += " from=\""+frm+"\""
                        
                        # If frm field entered.
                        if (untilFlag):
                            # Set verbRequest.
                            verbRequest += " until=\""+until+"\""

                        # If frm field entered.
                        if (setFlag):
                            # Set verbRequest.
                            verbRequest += " set=\""+set+"\""
                        
                        # Set verbRequest.
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                        
                    # Set verbRequest.
                    verbRequest += ">"+serverURL+"</request>\n  <ListRecords>\n"
                    
                    # Try to access each sub-folder XML metadata file in a Data Provider directory path.
                    for root, directories, filenames in os.walk(path):
                        # For each index of the of the Data Provider directory.
                        for i in range(startIndex, endIndex):
                            # Set identifier.
                            identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                            
                            # Generate response.
                            response = []
                            
                            # If first record.
                            if (startFile == 1):
                                # Append verbResponseHeader.
                                response.append(verbResponseHeader)
                                # Append verbResponseDate.
                                response.append(verbResponseDate)
                                #Append verbRequest.
                                response.append(verbRequest)
                            
                            splitString = "FHYA Depot/"
                            split = identifier.split(splitString)
                            # Set dcFilePath to the Data Provider sub-folder directory path concatenated with the (unqualified) Dublin Core file name.
                            dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                            
                            # Try to open the XML metadata record with UTF-8 encoding.
                            try:
                                with open(dcFilePath, encoding="utf-8") as dcFile:
                                    # Set data to the file contents read.
                                    data = dcFile.read()
                                    # Close the (unqualified) Dublin Core file.
                                    dcFile.close()
                            # Unable to open the XML metadata record.
                            except Exception as e:
                                # Print error statement.
                                print(e)
                            
                            # Get record date.
                            splitString = "<dc:date>"
                            split = data.split(splitString)
                            splitString = "</dc:date>"
                            split = split[1].split(splitString)
                            split = split[0].split(" ")
                            recordDate = split[0]
                            
                            # Get record, frm and until date objects.
                            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
                            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                            
                            # If recordDateObject is greater than frmDateObject and less than untilDateObject.
                            if ((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                                # Increment count.
                                count += 1
                                
                                # Set data.
                                data = "     <metadata>\n      "+data[39:len(data)]+"    </metadata>"
                                # Set about.
                                about = "\n     <about>"
                                # Set provenance.
                                provenance = "        xmlns=\"http://www.openarchives.org/OAI/2.0/provenance\"\n        xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n        xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/provenance\n        http://www.openarchives.org/OAI/2.0/provenance.xsd\">"
                                
                                # Set about.
                                about += "\n       <provenance>\n"+provenance+"\n      </provenance>"
                                about += "\n     </about>"
                                
                                # Set headerIdentifier.
                                headerIdentifier = "   <record>\n     <header>\n       <identifier>"+identifier+"</identifier>"
                                # Set headerDatestamp.
                                headerDatestamp = "\n       <datestamp>"+recordDate+"</datestamp>"
                                # Set headerSetSpec.
                                headerSetSpec = "\n       <setSpec>"+set+"</setSpec>"
                                headerSetSpec +=  "\n     </header>\n"
                                
                                # Generate header.
                                header = []
                                # Append headerIdentifier.
                                header.append(headerIdentifier)
                                # Append headerDatestamp.
                                header.append(headerDatestamp)
                                # Append headerSetSpec.
                                header.append(headerSetSpec)
                                # Convert list header to be of type str.
                                strHead = ''.join([str(elem) for elem in header])

                                # Generate record.
                                record = []
                                # Append strHead.
                                record.append(strHead)
                                # Append data.
                                record.append(data)
                                # Append about.
                                record.append(about)
                                record.append("\n   </record>")
                                # Convert list record to be of type str.
                                strRec = ''.join([str(elem) for elem in record])
                                # Append strRec.
                                response.append(strRec)
                                # Convert list response to be of type str.
                                strResp = ''.join([str(elem) for elem in response])
                                # Print response.
                                print(strResp)
                            
                            # Else skip record.
                            else:
                                pass
                            
                            # Increment startFile.
                            startFile += 1
                        
                        # If count is zero.
                        if (count == 0):
                            # Raise noRecordsMatch error.
                            raise
                        
                        # Set estimated completeListSize.
                        completeListSize = 87
                        # Set nextIndex.
                        nextIndex = endIndex
                        # Set expirationDate.
                        expirationDate = datetime.now() + timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
                        
                        # Set resumptionToken.
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\""
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " expirationDate="+"\""+expirationDate.strftime('%Y-%m-%dT%H:%M:%SZ')+"\""
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\">"
                        
                        # If response list is not complete.
                        if (complete == False):
                            
                            # Set tokenString.
                            tokenString = str(nextIndex)
                            tokenString += ",e"+expirationDate.strftime('%Y-%m-%dT%H:%M:%SZ')
                            tokenString += ","+metadataPrefix
                            
                            # If frm field entered.
                            if (fromFlag):
                                # Set tokenString.
                                tokenString += ",f"+frm
                            
                            # If until field entered.
                            if (untilFlag):
                                # Set tokenString.
                                tokenString += ",u"+until
                            
                            # If set field entered.
                            if (setFlag):
                                # Set tokenString.
                                tokenString += ","+set
                            
                            # Set resumptionToken.                  
                            resumptionToken += tokenString
                        
                        # Set resumptionToken.  
                        resumptionToken += "</resumptionToken>\n"
                        # Set responseEnd.  
                        responseEnd = "   "+resumptionToken
                        responseEnd += "  </ListRecords>\n</OAI-PMH>"
                        # Print response.
                        print(responseEnd)
                        # Break from for loop after all files have been read.
                        break
                    
                # Generate noRecordsMatch XML response.
                except:
                    # Set verbResponseHeader.
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    
                    # Set verbResponseDate.
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
                    verbResponseDate += "</responseDate>"
                    
                    # Set verbRequest.
                    verbRequest = "\n  <request verb=\"ListRecords\""
                    
                    # If resumptionToken entered.
                    if (resumptionTokenFlag):
                        # Set verbRequest.
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                    
                    # Else no resumptionToken entered.
                    else:
                        # If frm field entered.
                        if (fromFlag):
                            # Set verbRequest.
                            verbRequest += " from=\""+frm+"\""
                    
                        if (untilFlag):
                            # Set verbRequest.
                            verbRequest += " until=\""+until+"\""
                        
                        if (setFlag):
                            # Set verbRequest.
                            verbRequest += " set=\""+set+"\""
                        
                        # Set verbRequest.
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                    
                    # Set verbRequest.
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"noRecordsMatch\">The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.</error>"
                    
                    # Generate response.
                    response = []
                    # Append verbResponseHeader.
                    response.append(verbResponseHeader)
                    # Append verbResponseDate.
                    response.append(verbResponseDate)
                    # Append verbRequest.
                    response.append(verbRequest)
                    # Set responseEnd.
                    responseEnd = "\n</OAI-PMH>"
                    # Append responseEnd.
                    response.append(responseEnd)
                    # Convert list response to be of type str.
                    strResp = ''.join([str(elem) for elem in response])
                    # Print response.
                    print(strResp)
    
    # Else if query is a ListSets request.                
    elif (query == 'ListSets'):
        # Try to validate form fields.
        try:
            # For each form field, check if OAI-PMH valid.
            for field in form:
                if (field != "verb"):
                    # Raise badArgument error.
                    raise
                
        # Generate badArgument XML response.
        except:
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
            
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"ListSets\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            # Set responseEnd.
            responseEnd = "\n</OAI-PMH>"
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
        
        # Else generate XML response.
        else:
            # Set verbResponseHeader.
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            
            # Set verbResponseDate.
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
            verbResponseDate += "</responseDate>"
            
            # Set verbRequest.
            verbRequest = "\n  <request verb=\"ListSets\">"
            verbRequest += serverURL+"</request>\n <ListSets>\n"

            # Generate response.
            response = []
            # Append verbResponseHeader.
            response.append(verbResponseHeader)
            # Append verbResponseDate.
            response.append(verbResponseDate)
            # Append verbRequest.
            response.append(verbRequest)
            
            # Assign set.
            set = "FHYA Depot"
            
            # Set data.
            data = "  <set>\n    <setName>"+set+"</setName>\n    <setDescription>"
            data += "\n      <oai_dc:dc\n          xmlns:oai_dc=\"http://www.openarchives.org/OAI/2.0/oai_dc/\"\n          xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n          xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n          xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/oai_dc/\n          http://www.openarchives.org/OAI/2.0/oai_dc.xsd\">"
            data += "\n          <dc:description>This set contains metadata describing items from The Five Hundred Year Archive.</dc:description>"
            data += "\n       </oai_dc:dc>\n    </setDescription>\n  </set>"
            
            # Generate record.
            record = []
            # Append data.
            record.append(data)
            # Convert list record to be of type str.
            strRec = ''.join([str(elem) for elem in record])
            # Set responseEnd.
            responseEnd = "\n </ListSets>\n</OAI-PMH>"
            # Append strRec.
            response.append(strRec)
            # Append responseEnd.
            response.append(responseEnd)
            # Convert list response to be of type str.
            strResp = ''.join([str(elem) for elem in response])
            # Print response.
            print(strResp)
    
    # Else raise badVerb error.
    else:
        raise

# Generate badVerb XML response.
except:
    # Set verbResponseHeader.
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    
    # Set verbResponseDate.
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    verbResponseDate += "</responseDate>"
    
    # Set verbRequest.
    verbRequest = "\n  <request>"+serverURL+"</request>\n"
    verbRequest += "  <error code=\"badVerb\">Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated.</error>"
    
    # Generate response.
    response = []
    # Append verbResponseHeader.
    response.append(verbResponseHeader)
    # Append verbResponseDate.
    response.append(verbResponseDate)
    # Append verbRequest.
    response.append(verbRequest)
    # Set responseEnd.
    responseEnd = "\n</OAI-PMH>"
    # Append responseEnd.
    response.append(responseEnd)
    # Convert list response to be of type str.
    strResp = ''.join([str(elem) for elem in response])
    # Print response.
    print(strResp)