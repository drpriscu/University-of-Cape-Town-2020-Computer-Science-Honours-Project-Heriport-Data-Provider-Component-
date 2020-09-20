#!/usr/bin/env python3

import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import cgi
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

print ("Content-type: text/xml\n")
form = cgi.FieldStorage()
serverURL = "http://emandulo.apc.uct.ac.za/metadata/FHYA%20Depot/"

try:
    query = form["verb"].value

    if (query == 'GetRecord'):
        set = "FHYA Depot"
        try:
            identifier = form.getvalue ("identifier", "")
            metadataPrefix = form.getvalue ("metadataPrefix", "")
            
            for field in form:
                if ((field != "identifier") and (field != "metadataPrefix") and (field != "verb")):
                    raise
            
            if (type(identifier) is type([])):
                raise
            if (identifier == ""):
                raise
            
            if (type(metadataPrefix) is type([])):
                raise
            if (metadataPrefix == ""):
                raise
            
            badChars = ['\"','<','>','\'']
            for ch in badChars:
                if (ch in identifier):
                    raise
                if (ch in metadataPrefix):
                    raise

        except:        
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            verbRequest = "\n  <request verb=\"GetRecord\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            responseEnd = "\n</OAI-PMH>"
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
        
        else:
            try:
                splitString = "FHYA Depot/"
                split = identifier.split(splitString)
                dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                dcFile = open(dcFilePath, "r", encoding="utf-8")
                data = dcFile.read()
                dcFile.close()
                
            except:
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                
                verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                verbRequest += identifier+"\"\n           metadataPrefix=\""
                verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"idDoesNotExist\">The value of the identifier argument is unknown or illegal in this repository.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
            
            else:
                try:    
                    if(metadataPrefix != "oai_dc"):
                        raise
                except:
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                    
                    verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                    verbRequest += identifier+"\"\n           metadataPrefix=\""
                    verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                    
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                    
                    responseEnd = "\n</OAI-PMH>"
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)
                
                else:
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                    
                    verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
                    verbRequest += identifier+"\"\n           metadataPrefix=\""
                    verbRequest += metadataPrefix+"\">"+serverURL+"</request>\n  <GetRecord>\n   <record>"
                    
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                        
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
                    
                    data = "    <metadata>\n      "+data+"    </metadata>"
                    headerIdentifier = "\n    <header>\n      <identifier>"+identifier+"</identifier>"
                    headerDatestamp = "\n      <datestamp>"+str(datetime.now())+"</datestamp>"
                    headerSet = "\n      <setSpec>"+set+"</setSpec>\n    </header>\n"
                    
                    header = []
                    header.append(headerIdentifier)
                    header.append(headerDatestamp)
                    header.append(headerSet)
                    strHead = ''.join([str(elem) for elem in header]) 

                    record = []
                    record.append(strHead)
                    record.append(data)
                    strRec = ''.join([str(elem) for elem in record]) 

                    responseEnd = "\n  </record>\n </GetRecord>\n</OAI-PMH>"
                    response.append(strRec)
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)
        
    elif (query == 'Identify'):
        try:   
            for field in form:
                if (field != "verb"):
                    raise
                
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
        
        except:
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            verbRequest = "\n  <request verb=\"Identify\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            responseEnd = "\n</OAI-PMH>"
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
        
        else:   
            verbRequest = "\n  <request verb=\"Identify\">"
            verbRequest += serverURL+"</request>\n  <Identify>\n"
            
            repositoryName = "The Five Hundred Year Archive"
            repositoryIdentifier = "http://emandulo.apc.uct.ac.za/"
            earliestDatestamp = str(datetime.now())
                    
            path = 'FHYA Depot/'
            
            for root, directories, filenames in os.walk(path):
                for i in range(1,88):
                    identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                                
                    splitString = "FHYA Depot/"
                    split = identifier.split(splitString)
                    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                    
                    try:
                        dcFile = open(dcFilePath, "r", encoding="utf-8")
                        data = dcFile.read()
                        dcFile.close()
                    except Exception as e:
                        print(e)
                    
                    splitString = "<dc:date>"
                    split = data.split(splitString)
                    splitString = "</dc:date>"
                    split = split[1].split(splitString)
                    split = split[0].split(" ")
                    recordDate = split[0]
                            
                    if((recordDate <= earliestDatestamp)):
                        earliestDatestamp = recordDate
                break
            
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
            
            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            record = []
            record.append(data)
            strRec = ''.join([str(elem) for elem in record])
            
            responseEnd = "\n  </Identify>\n</OAI-PMH>"
            response.append(strRec)
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
            
    elif (query == 'ListIdentifiers'):
        fromFlag = False
        untilFlag = False
        metadataPrefixFlag = False
        setFlag = False
        resumptionTokenFlag = False
        
        frm = ""
        until = ""
        metadataPrefix = ""
        set = ""
        resumptionToken = ""
        
        try:
            for field in form:
                if ((field != "metadataPrefix") and (field != "verb") and (field != "set") and (field != "from") and (field != "until") and (field != "resumptionToken")):
                    raise
                        
            for field in form:
                if (field == "metadataPrefix"):
                    metadataPrefixFlag = True
                
                if (field == "resumptionToken"):
                    resumptionTokenFlag = True
                
            if (metadataPrefixFlag and resumptionTokenFlag):
                raise
            
            if (resumptionTokenFlag):
                resumptionToken = form.getvalue ("resumptionToken", "")
                resumptionTokenSplit = resumptionToken.split(',')
                
                resumptionTokenFromFlag = False
                resumptionTokenUntilFlag = False
                
                resumptionTokenFrom = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                resumptionTokenUntil = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                
                resumptionTokenSetFlag = False
                resumptionTokenSet = "set"
                
                resumptionTokenNextIndex = resumptionTokenSplit[0]
                resumptionTokenExpirationDate = resumptionTokenSplit[1][1:len(resumptionTokenSplit[1])]
                resumptionTokenMetadataPrefix = resumptionTokenSplit[2]
                
                if (len(resumptionTokenSplit) == 6):
                    resumptionTokenFromFlag = True
                    resumptionTokenUntilFlag = True
                    resumptionTokenSetFlag = True
                    resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                    resumptionTokenSet = resumptionTokenSplit[5]
                
                if (len(resumptionTokenSplit) == 5):
                    field = resumptionTokenSplit[3][0:1]

                    if (field == 'f'):
                        resumptionTokenFromFlag = True
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        field = resumptionTokenSplit[4][0:1]

                        if (field == 'u'):
                            resumptionTokenUntilFlag = True
                            resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                        else:
                            resumptionTokenSetFlag = True
                            resumptionTokenSet = resumptionTokenSplit[4]

                    if (field == 'u'):
                        resumptionTokenUntilFlag = True
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        resumptionTokenSetFlag = True
                        resumptionTokenSet = resumptionTokenSplit[4]
                
                if (len(resumptionTokenSplit) == 4):
                    field = resumptionTokenSplit[3][0:1]
                    
                    if (field == 'f'):
                        resumptionTokenFromFlag = True
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        
                    elif (field == 'u'):
                        resumptionTokenUntilFlag = True
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    else:
                        resumptionTokenSetFlag = True
                        resumptionTokenSet = resumptionTokenSplit[3]
             
                if (resumptionTokenExpirationDate != datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')):
                    raise
                
                if (resumptionTokenMetadataPrefix != "oai_dc"):
                    raise
                
                if (resumptionTokenFromFlag): 
                    if (resumptionTokenFrom != datetime.strptime(resumptionTokenFrom, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                
                if (resumptionTokenUntilFlag): 
                    if (resumptionTokenUntil != datetime.strptime(resumptionTokenUntil, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                
                if (resumptionTokenSetFlag):
                    if (resumptionTokenSet != "FHYA Depot"):
                        raise
                
                resumptionTokenExpirationDatebject = datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%S')
                currentDate = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                currentDateObject = datetime.strptime(currentDate, '%Y-%m-%dT%H:%M:%S')
                                
                if (resumptionTokenExpirationDatebject <= currentDateObject):
                    raise
                
                if (resumptionTokenFromFlag):
                    frm = resumptionTokenFrom
                    
                if (resumptionTokenUntilFlag):
                    until = resumptionTokenUntil
                
                metadataPrefix = resumptionTokenMetadataPrefix
                
                if (resumptionTokenSetFlag):
                    set = resumptionTokenSet
                
                if (type(metadataPrefix) is type([])):
                    raise
                
                if (metadataPrefix == ""):
                    raise
                
                if (type(frm) is type([])):
                    raise
                if (frm != ""):
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    fromFlag = True
                else:
                    frm = "2020-01-01"
                    
                if (type(until) is type([])):
                    raise
                if (until != ""):
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    untilFlag = True
                else:
                    until = datetime.today().strftime('%Y-%m-%d')
                
                if (type(set) is type([])):
                    raise
                if (set == ""):
                    set = "FHYA Depot"
                else:
                    setFlag = True
                    
                if (metadataPrefixFlag):
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    if (frmDateObject > untilDateObject):
                        raise
                    
                    badChars = ['\"','<','>','\'']
                    for ch in badChars:
                        if (ch in metadataPrefix):
                            raise
                        if (ch in set):
                            raise
                        
            else:
                metadataPrefix = form.getvalue ("metadataPrefix", "")
                frm = form.getvalue ("from", "")
                until = form.getvalue ("until", "")
                set = form.getvalue ("set", "")
            
                if (type(metadataPrefix) is type([])):
                    raise
                if (metadataPrefix == ""):
                    raise
                
                if (type(frm) is type([])):
                    raise
                if (frm != ""):
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    fromFlag = True
                else:
                    frm = "2020-01-01"
                    
                if (type(until) is type([])):
                    raise
                if (until != ""):
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    untilFlag = True
                else:
                    until = datetime.today().strftime('%Y-%m-%d')
                
                if (type(set) is type([])):
                    raise
                if (set == ""):
                    set = "FHYA Depot"
                else:
                    setFlag = True
                    
                if (metadataPrefixFlag):
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    if (frmDateObject > untilDateObject):
                        raise
                    
                    badChars = ['\"','<','>','\'']
                    for ch in badChars:
                        if (ch in metadataPrefix):
                            raise
                        if (ch in set):
                            raise

        except:          
            if (resumptionTokenFlag and not metadataPrefixFlag):
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                verbRequest = "\n  <request verb=\"ListIdentifiers\""
                verbRequest += " resumptionToken=\""+resumptionToken+"\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badResumptionToken\">The value of the resumptionToken argument is invalid or expired.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
            
            else:
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                
                verbRequest = "\n  <request verb=\"ListIdentifiers\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
             
        else:
            try:
                if (metadataPrefix != "oai_dc"):
                    raise
            except:
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                        
                verbRequest = "\n  <request verb=\"ListIdentifiers\""
                
                if (resumptionTokenFlag):
                    verbRequest += " resumptionToken=\""+resumptionToken+"\""
                else:
                    if (fromFlag):
                        verbRequest += " from=\""+frm+"\""
                    
                    if (untilFlag):
                        verbRequest += " until=\""+until+"\""
                    
                    verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                    
                    if (setFlag):
                        verbRequest += " set=\""+set+"\""
                    
                verbRequest += ">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
            
            else:
                try:
                    if (set != "FHYA Depot"):
                        raise
                    
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                            
                    verbRequest = "\n  <request verb=\"ListIdentifiers\""
                    
                    path = 'FHYA Depot/'
                    count = 0
                    startFile = 1
                    startIndex = 1
                    endIndex = 11
                    complete = False
                    
                    if (resumptionTokenFlag):
                        startIndex = int(resumptionTokenNextIndex)
                        
                        if (endIndex < 87):
                            endIndex = startIndex+10
                        
                        if (endIndex > 87):
                            complete = True
                            endIndex = 88
                    
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                    else:
                        if (fromFlag):
                            verbRequest += " from=\""+frm+"\""
                        
                        if (untilFlag):
                            verbRequest += " until=\""+until+"\""
                    
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                    
                        if (setFlag):
                            verbRequest += " set=\""+set+"\""
                    
                    verbRequest += ">"+serverURL+"</request>\n  <ListIdentifiers>\n"

                    for root, directories, filenames in os.walk(path):
                        for i in range(startIndex, endIndex):
                            identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                            
                            response = []
                            
                            if (startFile == 1):
                                response.append(verbResponseHeader)
                                response.append(verbResponseDate)
                                response.append(verbRequest)
                
                            splitString = "FHYA Depot/"
                            split = identifier.split(splitString)
                            dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                            
                            try:
                                dcFile = open(dcFilePath, "r", encoding="utf-8")
                                data = dcFile.read()
                                dcFile.close()
                            except Exception as e:
                                print(e)
                            
                            splitString = "<dc:date>"
                            split = data.split(splitString)
                            splitString = "</dc:date>"
                            split = split[1].split(splitString)
                            split = split[0].split(" ")
                            recordDate = split[0]
                            
                            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
                            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                            
                            if ((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                                count += 1
                                headerIdentifier = "   <header>\n      <identifier>"+identifier+"</identifier>"
                                headerDatestamp = "\n      <datestamp>"+recordDate+"</datestamp>"
                                headerSetSpec = "\n      <setSpec>"+set+"</setSpec>"
                            
                                headerSetSpec +=  "\n   </header>"
                                
                                header = []
                                header.append(headerIdentifier)
                                header.append(headerDatestamp)
                                header.append(headerSetSpec)
                                strHead = ''.join([str(elem) for elem in header]) 

                                record = []
                                record.append(strHead)
                                strRec = ''.join([str(elem) for elem in record]) 
                                
                                response.append(strRec)
                                strResp = ''.join([str(elem) for elem in response]) 
                                print(strResp)
                            
                            else:
                                pass
                            
                            startFile += 1
                        
                        if (count == 0):
                            raise
                
                        completeListSize = 87
                        nextIndex = endIndex
                        expirationDate = datetime.now() + timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\""
                        
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " expirationDate="+"\""+expirationDate.strftime('%Y-%m-%dT%H:%M:%S')+"\""
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\">"
                        
                        if (complete == False):
                            tokenString = str(nextIndex)
                            tokenString += ",e"+expirationDate.strftime('%Y-%m-%dT%H:%M:%S')
                            
                            tokenString += ","+metadataPrefix
                        
                            if (fromFlag):
                                tokenString += ",f"+frm

                            if (untilFlag):
                                tokenString += ",u"+until
                            
                            if (setFlag):
                                tokenString += ","+set                    
                            resumptionToken += tokenString
                        
                        resumptionToken += "</resumptionToken>\n"
                        responseEnd = "   "+resumptionToken
                        
                        responseEnd += " </ListIdentifiers>\n</OAI-PMH>"
                        print(responseEnd)
                        break
                    
                except:
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                            
                    verbRequest = "\n  <request verb=\"ListIdentifiers\""
                    
                    if (resumptionTokenFlag):
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                        
                    else:    
                        if (fromFlag):
                            verbRequest += " from=\""+frm+"\""
                    
                        if (untilFlag):
                            verbRequest += " until=\""+until+"\""
                        
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                        
                        if (setFlag):
                            verbRequest += " set=\""+set+"\""
                    
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"noRecordsMatch\">The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.</error>"
                    
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                    
                    responseEnd = "\n</OAI-PMH>"
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)
        
    elif (query == 'ListMetadataFormats'):
        try:
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            for field in form:
                if ((field != "verb") and (field != "identifier")):
                    raise
            
            identifier = form.getvalue ("identifier", "")
            if (type(identifier) is type([])):
                raise
            badChars = ['\"','<','>','\'']
            for ch in badChars:
                if (ch in identifier):
                    raise
        
        except:            
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            verbRequest = "\n  <request verb=\"ListMetadataFormats\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            responseEnd = "\n</OAI-PMH>"
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
        
        else:
            try:
                identifierFlag = False
                if (identifier == ""):
                    raise
                else:
                    identifierFlag = True
        
            except:
                verbRequest = "\n  <request verb=\"ListMetadataFormats\">"
                verbRequest += serverURL+"</request>\n  <ListMetadataFormats>\n"
            
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                data = "    <metadataPrefix>oai_dc</metadataPrefix>\n     <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>\n     <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>"
                data = "   <metadataFormat>\n"+data+"\n   </metadataFormat>"
                
                record = []
                record.append(data)
                strRec = ''.join([str(elem) for elem in record])
                
                responseEnd = "\n  </ListMetadataFormats>\n</OAI-PMH>"
                response.append(strRec)
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)  
            
            else:   
                try:
                    splitString = "FHYA Depot/"
                    split = identifier.split(splitString)
                    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                    dcFile = open(dcFilePath, "r", encoding="utf-8")
                    data = dcFile.read()
                    dcFile.close()
                
                except:
                    verbRequest = "\n  <request verb=\"ListMetadataFormats\""
                    
                    if (identifierFlag):
                        verbRequest += " identifier=\""+identifier+"\""
                    
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"idDoesNotExist\">The value of the identifier argument is unknown or illegal in this repository.</error>"
            
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                    
                    responseEnd = "\n</OAI-PMH>"
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)
                    
                else:
                    verbRequest = "\n  <request verb=\"ListMetadataFormats\""
                    
                    if (identifierFlag):
                        verbRequest += " identifier=\""+identifier+"\""
                        
                    verbRequest += ">"+serverURL+"</request>\n  <ListMetadataFormats>\n"
                
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                    
                    data = "     <metadataPrefix>oai_dc</metadataPrefix>\n     <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>\n     <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>"
                    data = "   <metadataFormat>\n"+data+"\n   </metadataFormat>"
                    
                    record = []
                    record.append(data)
                    strRec = ''.join([str(elem) for elem in record])
                    
                    responseEnd = "\n </ListMetadataFormats>\n</OAI-PMH>"
                    response.append(strRec)
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)         

    elif (query == 'ListRecords'):
        fromFlag = False
        untilFlag = False
        setFlag = False
        resumptionTokenFlag = False
        metadataPrefixFlag = False
        
        frm = ""
        until = ""
        set = ""
        resumptionToken = ""
        metadataPrefix = ""
        
        try:
            for field in form:
                if ((field != "metadataPrefix") and (field != "verb") and (field != "set") and (field != "from") and (field != "until") and (field != "resumptionToken")):
                    raise
                        
            for field in form:
                if (field == "metadataPrefix"):
                    metadataPrefixFlag = True
                
                if (field == "resumptionToken"):
                    resumptionTokenFlag = True
                
            if (metadataPrefixFlag and resumptionTokenFlag):
                raise
            
            if (resumptionTokenFlag):
                resumptionToken = form.getvalue ("resumptionToken", "")
                resumptionTokenSplit = resumptionToken.split(',')
                
                resumptionTokenFromFlag = False
                resumptionTokenUntilFlag = False
                
                resumptionTokenFrom = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                resumptionTokenUntil = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                
                resumptionTokenSetFlag = False
                resumptionTokenSet = "set"
                
                resumptionTokenNextIndex = resumptionTokenSplit[0]
                resumptionTokenExpirationDate = resumptionTokenSplit[1][1:len(resumptionTokenSplit[1])]
                resumptionTokenMetadataPrefix = resumptionTokenSplit[2]
                
                if (len(resumptionTokenSplit) == 6):
                    resumptionTokenFromFlag = True
                    resumptionTokenUntilFlag = True
                    resumptionTokenSetFlag = True
                    resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                    resumptionTokenSet = resumptionTokenSplit[5]
                
                if (len(resumptionTokenSplit) == 5):
                    field = resumptionTokenSplit[3][0:1]

                    if (field == 'f'):
                        resumptionTokenFromFlag = True
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        field = resumptionTokenSplit[4][0:1]

                        if (field == 'u'):
                            resumptionTokenUntilFlag = True
                            resumptionTokenUntil = resumptionTokenSplit[4][1:len(resumptionTokenSplit[4])]
                        else:
                            resumptionTokenSetFlag = True
                            resumptionTokenSet = resumptionTokenSplit[4]

                    if (field == 'u'):
                        resumptionTokenUntilFlag = True
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        resumptionTokenSetFlag = True
                        resumptionTokenSet = resumptionTokenSplit[4]
                
                if (len(resumptionTokenSplit) == 4):
                    field = resumptionTokenSplit[3][0:1]
                    
                    if (field == 'f'):
                        resumptionTokenFromFlag = True
                        resumptionTokenFrom = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                        
                    elif (field == 'u'):
                        resumptionTokenUntilFlag = True
                        resumptionTokenUntil = resumptionTokenSplit[3][1:len(resumptionTokenSplit[3])]
                    else:
                        resumptionTokenSetFlag = True
                        resumptionTokenSet = resumptionTokenSplit[3]
             
                if (resumptionTokenExpirationDate != datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')):
                    raise
                
                if (resumptionTokenMetadataPrefix != "oai_dc"):
                    raise
                
                if (resumptionTokenFromFlag): 
                    if (resumptionTokenFrom != datetime.strptime(resumptionTokenFrom, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                
                if (resumptionTokenUntilFlag): 
                    if (resumptionTokenUntil != datetime.strptime(resumptionTokenUntil, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                
                if (resumptionTokenSetFlag):
                    if (resumptionTokenSet != "FHYA Depot"):
                        raise
                
                resumptionTokenExpirationDatebject = datetime.strptime(resumptionTokenExpirationDate, '%Y-%m-%dT%H:%M:%S')
                currentDate = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                currentDateObject = datetime.strptime(currentDate, '%Y-%m-%dT%H:%M:%S')
                                
                if (resumptionTokenExpirationDatebject <= currentDateObject):
                    raise
                
                if (resumptionTokenFromFlag):
                    frm = resumptionTokenFrom
                    
                if (resumptionTokenUntilFlag):
                    until = resumptionTokenUntil
                
                metadataPrefix = resumptionTokenMetadataPrefix
                
                if (resumptionTokenSetFlag):
                    set = resumptionTokenSet
                
                if (type(metadataPrefix) is type([])):
                    raise
                
                if (metadataPrefix == ""):
                    raise
                
                if (type(frm) is type([])):
                    raise
                if (frm != ""):
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    fromFlag = True
                else:
                    frm = "2020-01-01"
                    
                if (type(until) is type([])):
                    raise
                if (until != ""):
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    untilFlag = True
                else:
                    until = datetime.today().strftime('%Y-%m-%d')
                
                if (type(set) is type([])):
                    raise
                if (set == ""):
                    set = "FHYA Depot"
                else:
                    setFlag = True
                    
                if (metadataPrefixFlag):
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    if (frmDateObject > untilDateObject):
                        raise
                    
                    badChars = ['\"','<','>','\'']
                    for ch in badChars:
                        if (ch in metadataPrefix):
                            raise
                        if (ch in set):
                            raise
                        
            else:
                metadataPrefix = form.getvalue ("metadataPrefix", "")
                frm = form.getvalue ("from", "")
                until = form.getvalue ("until", "")
                set = form.getvalue ("set", "")
            
                if (type(metadataPrefix) is type([])):
                    raise
                if (metadataPrefix == ""):
                    raise
                
                if (type(frm) is type([])):
                    raise
                if (frm != ""):
                    if (frm != datetime.strptime(frm, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    fromFlag = True
                else:
                    frm = "2020-01-01"
                    
                if (type(until) is type([])):
                    raise
                if (until != ""):
                    if (until != datetime.strptime(until, "%Y-%m-%d").strftime('%Y-%m-%d')):
                        raise
                    untilFlag = True
                else:
                    until = datetime.today().strftime('%Y-%m-%d')
                
                if (type(set) is type([])):
                    raise
                if (set == ""):
                    set = "FHYA Depot"
                else:
                    setFlag = True
                    
                if (metadataPrefixFlag):
                    frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                    untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                    
                    if (frmDateObject > untilDateObject):
                        raise
                    
                    badChars = ['\"','<','>','\'']
                    for ch in badChars:
                        if (ch in metadataPrefix):
                            raise
                        if (ch in set):
                            raise
        
        except:
            if (resumptionTokenFlag and not metadataPrefixFlag):
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                verbRequest = "\n  <request verb=\"ListRecords\""
                verbRequest += " resumptionToken=\""+resumptionToken+"\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badResumptionToken\">The value of the resumptionToken argument is invalid or expired.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
            
            else:  
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                
                verbRequest = "\n  <request verb=\"ListRecords\">"
                verbRequest += serverURL+"</request>\n"
                verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)   
            
        else:
            try:
                if (metadataPrefix != "oai_dc"):
                    raise
            except:
                verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                verbResponseDate = "\n  <responseDate>"
                verbResponseDate += str(datetime.now())
                verbResponseDate += "</responseDate>"
                        
                verbRequest = "\n  <request verb=\"ListRecords\""
                
                if (resumptionTokenFlag):
                    verbRequest += " resumptionToken=\""+resumptionToken+"\""
                else:
                    if (fromFlag):
                        verbRequest += " from=\""+frm+"\""
                    
                    if (untilFlag):
                        verbRequest += " until=\""+until+"\""
                
                    if (setFlag):
                        verbRequest += " set=\""+set+"\""
                    
                    verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                
                verbRequest += ">"+serverURL+"</request>\n"
                verbRequest += "  <error code=\"cannotDisseminateFormat\">The metadata format identified by the value given for the metadataPrefix argument is not supported by the item or by the repository.</error>"
                
                response = []
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
                
                responseEnd = "\n</OAI-PMH>"
                response.append(responseEnd)
                strResp = ''.join([str(elem) for elem in response])
                print(strResp)
                    
            else:
                try:
                    if (set != "FHYA Depot"):
                        raise
                
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                            
                    verbRequest = "\n  <request verb=\"ListRecords\""
                    
                    path = 'FHYA Depot/'
                    count = 0
                    startFile = 1
                    startIndex = 1
                    endIndex = 11
                    complete = False
                    
                    if (resumptionTokenFlag):
                        startIndex = int(resumptionTokenNextIndex)
                        
                        if (endIndex < 87):
                            endIndex = startIndex+10
                        
                        if (endIndex > 87):
                            complete = True
                            endIndex = 88
                    
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                        
                    else:
                        if (fromFlag):
                            verbRequest += " from=\""+frm+"\""
                        
                        if (untilFlag):
                            verbRequest += " until=\""+until+"\""
                    
                        if (setFlag):
                            verbRequest += " set=\""+set+"\""
                            
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                
                    verbRequest += ">"+serverURL+"</request>\n  <ListRecords>\n"
                    
                    for root, directories, filenames in os.walk(path):
                        for i in range(startIndex,endIndex):
                            identifier = "http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/"+str(i)
                            
                            response = []
                            
                            if (startFile == 1):
                                response.append(verbResponseHeader)
                                response.append(verbResponseDate)
                                response.append(verbRequest)
                
                            splitString = "FHYA Depot/"
                            split = identifier.split(splitString)
                            dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
                            
                            try:
                                with open(dcFilePath, encoding="utf-8") as dcFile:
                                    data = dcFile.read()
                                    dcFile.close()
                            except Exception as e:
                                print(e)
                            
                            splitString = "<dc:date>"
                            split = data.split(splitString)
                            splitString = "</dc:date>"
                            split = split[1].split(splitString)
                            split = split[0].split(" ")
                            recordDate = split[0]
                            
                            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
                            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
                            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
                            
                            if((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                                count += 1
                                data = "     <metadata>\n      "+data[39:len(data)]+"    </metadata>"
                                about = "\n     <about>"
                                provenance = "        xmlns=\"http://www.openarchives.org/OAI/2.0/provenance\"\n        xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n        xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/provenance\n        http://www.openarchives.org/OAI/2.0/provenance.xsd\">"
                                
                                about += "\n       <provenance>\n"+provenance+"\n      </provenance>"
                                about += "\n     </about>"
                                
                                headerIdentifier = "   <record>\n     <header>\n       <identifier>"+identifier+"</identifier>"
                                headerDatestamp = "\n       <datestamp>"+recordDate+"</datestamp>"
                                headerSetSpec = "\n       <setSpec>"+set+"</setSpec>"
                            
                                headerSetSpec +=  "\n     </header>\n"
                                
                                header = []
                                header.append(headerIdentifier)
                                header.append(headerDatestamp)
                                header.append(headerSetSpec)
                                strHead = ''.join([str(elem) for elem in header]) 

                                record = []
                                record.append(strHead)
                                record.append(data)
                                record.append(about)
                                record.append("\n   </record>")
                                strRec = ''.join([str(elem) for elem in record])
                                
                                response.append(strRec)
                                strResp = ''.join([str(elem) for elem in response])
                                print(strResp)
                            
                            else:
                                pass
                            
                            startFile += 1
                        
                        if (count == 0):
                            raise
                        
                        completeListSize = 87
                        nextIndex = endIndex
                        expirationDate = datetime.now() + timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=10, hours=0, weeks=0)
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\""
                        
                        resumptionToken = "<resumptionToken"
                        resumptionToken += " expirationDate="+"\""+expirationDate.strftime('%Y-%m-%dT%H:%M:%S')+"\""
                        resumptionToken += " completeListSize="+"\""+str(completeListSize)+"\">"
                        
                        if (complete == False):
                            tokenString = str(nextIndex)
                            tokenString += ",e"+expirationDate.strftime('%Y-%m-%dT%H:%M:%S')
                            
                            tokenString += ","+metadataPrefix
                        
                            if (fromFlag):
                                tokenString += ",f"+frm

                            if (untilFlag):
                                tokenString += ",u"+until
                            
                            if (setFlag):
                                tokenString += ","+set                    
                            resumptionToken += tokenString
                        
                        resumptionToken += "</resumptionToken>\n"
                        responseEnd = "   "+resumptionToken
                                    
                        responseEnd += "  </ListRecords>\n</OAI-PMH>"
                        print(responseEnd)
                        break
                
                except:
                    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
                    verbResponseDate = "\n  <responseDate>"
                    verbResponseDate += str(datetime.now())
                    verbResponseDate += "</responseDate>"
                            
                    verbRequest = "\n  <request verb=\"ListRecords\""
                    
                    if (resumptionTokenFlag):
                        verbRequest += " resumptionToken=\""+resumptionToken+"\""
                        
                    else:    
                        if (fromFlag):
                            verbRequest += " from=\""+frm+"\""
                    
                        if (untilFlag):
                            verbRequest += " until=\""+until+"\""
                        
                        if (setFlag):
                            verbRequest += " set=\""+set+"\""
                        
                        verbRequest += " metadataPrefix=\""+metadataPrefix+"\""
                    
                    verbRequest += ">"+serverURL+"</request>\n"
                    verbRequest += "  <error code=\"noRecordsMatch\">The combination of the values of the from, until, set and metadataPrefix arguments results in an empty list.</error>"
                    
                    response = []
                    response.append(verbResponseHeader)
                    response.append(verbResponseDate)
                    response.append(verbRequest)
                    
                    responseEnd = "\n</OAI-PMH>"
                    response.append(responseEnd)
                    strResp = ''.join([str(elem) for elem in response])
                    print(strResp)
                    
    elif (query == 'ListSets'):
        try:
            for field in form:
                if (field != "verb"):
                    raise
        
        except:
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            verbRequest = "\n  <request verb=\"ListSets\">"
            verbRequest += serverURL+"</request>\n"
            verbRequest += "  <error code=\"badArgument\">The request includes illegal arguments, is missing required arguments, includes a repeated argument, or values for arguments have an illegal syntax.</error>"
            
            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            responseEnd = "\n</OAI-PMH>"
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
        
        else:    
            verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
            verbResponseDate = "\n  <responseDate>"
            verbResponseDate += str(datetime.now())
            verbResponseDate += "</responseDate>"
            
            verbRequest = "\n  <request verb=\"ListSets\">"
            verbRequest += serverURL+"</request>\n <ListSets>\n"

            response = []
            response.append(verbResponseHeader)
            response.append(verbResponseDate)
            response.append(verbRequest)
            
            set = "FHYA Depot"
            data = "  <set>\n    <setName>"+set+"</setName>\n    <setDescription>"
            data += "\n      <oai_dc:dc\n          xmlns:oai_dc=\"http://www.openarchives.org/OAI/2.0/oai_dc/\"\n          xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n          xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n          xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/oai_dc/\n          http://www.openarchives.org/OAI/2.0/oai_dc.xsd\">"
            data += "\n          <dc:description>This set contains metadata describing items from the Five Hundred Year Archive.</dc:description>"
            data += "\n       </oai_dc:dc>\n    </setDescription>\n  </set>"
            
            record = []
            record.append(data)
            strRec = ''.join([str(elem) for elem in record])
            
            responseEnd = "\n </ListSets>\n</OAI-PMH>"
            response.append(strRec)
            response.append(responseEnd)
            strResp = ''.join([str(elem) for elem in response])
            print(strResp)
    
    else:
        raise
    
except:
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"

    verbRequest = "\n  <request>"+serverURL+"</request>\n"
    verbRequest += "  <error code=\"badVerb\">Value of the verb argument is not a legal OAI-PMH verb, the verb argument is missing, or the verb argument is repeated.</error>"

    response = []
    response.append(verbResponseHeader)
    response.append(verbResponseDate)
    response.append(verbRequest)

    responseEnd = "\n</OAI-PMH>"
    response.append(responseEnd)
    strResp = ''.join([str(elem) for elem in response])
    print(strResp)