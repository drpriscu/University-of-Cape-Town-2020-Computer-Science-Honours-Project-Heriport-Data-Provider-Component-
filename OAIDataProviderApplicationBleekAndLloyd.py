#!/usr/bin/env python3

import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import cgi
from datetime import datetime
import xml.etree.ElementTree as ET

form = cgi.FieldStorage()

query = form["verb"].value

print ("Content-type: text/xml\n")

serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"

if (query == 'GetRecord'):
    
    metadataPrefix = form.getvalue ("metadataPrefix", "")
    identifier = form.getvalue ("identifier", "")
    
    set = "stories"
        
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
    
    splitString = "stories/"
    split = identifier.split(splitString)
    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
    
    try:
        with open(dcFilePath, encoding="utf-8") as dcFile:
            data = dcFile.read()
            dcFile.close()
    except Exception as e:
                print(e)
        
    splitString = "<dc:identifier>"+identifier+"</dc:identifier>"
    split = data.split(splitString)
    
    if len(split) == 2:
        part1 = split[0]
        part1 = part1[39:len(part1)-3]
        part2 = split[1]
        data = part1+part2
       
    else:
        part1 = split[0]
        part1 = part1[39:len(part1)-1]
        data = part1
    
    data = "    <metadata>\n      "+data+"\n    </metadata>"
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
    
elif(query == 'ListIdentifiers'):
    
    metadataPrefix = form.getvalue ("metadataPrefix", "")
    try:
        set = form.getvalue ("set", "")
        frm = form.getvalue ("from", "")
        until = form.getvalue ("until", "")
    except:
        metadataPrefix = "oai_dc"
        set = "stories"
        frm = "2020-01-01"
        until = datetime.today().strftime('%Y-%m-%d')
        
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n  <request verb=\"ListIdentifiers\" from=\""
    verbRequest += frm+"\"\n           metadataPrefix=\""
    verbRequest += metadataPrefix+"\"\n           set=\""
    verbRequest += set+"\">"+serverURL+"</request>\n  <ListIdentifiers>\n"
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            identifier = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
            
            response = []
            
            if (i == 1):
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
  
            splitString = "stories/"
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
            recordDate = split[0]
            
            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
            
            if((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                
                headerIdentifier = "   <header>\n      <identifier>"+identifier+"</identifier>"
                headerDatestamp = "\n      <datestamp>"+str(datetime.now())+"</datestamp>"
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
                    
        responseEnd = " </ListIdentifiers>\n</OAI-PMH>"
        print(responseEnd)
        break
    
elif (query == 'ListRecords'):
    
    try:
        metadataPrefix = form.getvalue ("metadataPrefix", "")
        set = form.getvalue ("set", "")
        frm = form.getvalue ("from", "")
        until = form.getvalue ("until", "")
    except:
        set = "stories"
        frm = "2020-01-01"
        until = datetime.today().strftime('%Y-%m-%d')
        
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n <request verb=\"ListRecords\" from=\""
    verbRequest += frm+"\"\n          set=\""
    verbRequest += set+"\"\n          metadataPrefix=\""
    verbRequest += metadataPrefix+"\">"+"\n          "+serverURL+"</request>\n <ListRecords>\n"
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            identifier = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
            
            response = []
            
            if (i == 1):
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
  
            splitString = "stories/"
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
            recordDate = split[0]
            
            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
            
            if((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                                
                data = "    <metadata>\n      "+data[39:len(data)]+"    </metadata>"
                about = "\n    <about>"
                provenance = "       xmlns=\"http://www.openarchives.org/OAI/2.0/provenance\"\n       xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n       xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/provenance\n       http://www.openarchives.org/OAI/2.0/provenance.xsd\">"
                
                about += "\n      <provenance>\n"+provenance+"\n      </provenance>"
                about += "\n    </about>"
                
                headerIdentifier = "  <record>\n    <header>\n      <identifier>"+identifier+"</identifier>"
                headerDatestamp = "\n      <datestamp>"+str(datetime.now())+"</datestamp>"
                headerSetSpec = "\n      <setSpec>"+set+"</setSpec>"
            
                headerSetSpec +=  "\n    </header>\n"
                
                header = []
                header.append(headerIdentifier)
                header.append(headerDatestamp)
                header.append(headerSetSpec)
                strHead = ''.join([str(elem) for elem in header]) 

                record = []
                record.append(strHead)
                record.append(data)
                record.append(about)
                record.append("\n  </record>")
                strRec = ''.join([str(elem) for elem in record])
                
                response.append(strRec)
                strResp = ''.join([str(elem) for elem in response]) 
                
                print(strResp)
            
            else:
                pass
                    
        responseEnd = " </ListRecords> \n</OAI-PMH>"
        print(responseEnd)
        break  

else:
    print ("Error")