# Alex Priscu
# Program that takes in OAI-PMH Request verbs and provides Responses.
# OAI Data Provider Application
# 11 August 2020

#!/usr/bin/python3

# Imports
import os
import xmltodict
import pprint
from lxml import etree
from xmlutils import Rules, dump_etree_helper, etree_to_string
import simpledc
import cgi
from datetime import datetime
import xml.etree.ElementTree as ET

#form = cgi.FieldStorage()

#query = form["verb"].value

query = 'ListRecords'
baseURL = "www.heriport.com"
print ("Content-type: text/xml\n")

if (query == 'GetRecord'):
    """Get a record for a metadataPrefix and identifier.

    metadataPrefix - identifies metadata set to retrieve
    identifier - repository-unique identifier of record
    
    Should raise error.CannotDisseminateFormatError if
    metadataPrefix is unknown or not supported by identifier.
    
    Should raise error.IdDoesNotExistError if identifier is
    unknown or illegal.

    Returns a header, metadata, about tuple describing the record.
    """
    
    #metadataPrefix = form.getvalue ("metadataPrefix", "")
    #identifier = form.getvalue ("identifier", "")
    
    metadataPrefix = "oai_dc"
    identifier = "1"
            
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
    
    verbRequest = "\n  <request verb=\"GetRecord\" identifier=\""
    verbRequest += identifier+"\"\n           metadataPrefix=\""
    verbRequest += metadataPrefix+"\">"+baseURL+"</request>\n  <GetRecord>\n   <record>"
    
    response = []
    response.append(verbResponseHeader)
    response.append(verbResponseDate)
    response.append(verbRequest)
    
    fileName = "stories-dc/metadata-"+identifier+"-dc.xml"
    try:
        with open(fileName) as file:
            data = file.read()
            file.close()
    except Exception as e:
                print(e)
                print(fileName)
                print("File Error")
        
    splitString = "<dc:identifiers>"+identifier+"</dc:identifiers>"
    split = data.split(splitString)
    
    if len(split) == 2:
        part1 = split[0]
        part1 = part1[39:len(part1)-3]
        part2 = split[1]
        data = part1+part2
        
    else:
        part1 = split[0]
        part1 = part1[39:len(part1)-3]
        data = part1
        
    data = "    <metadata>"+"\n      "+data+"    </metadata>"
    headerIdentifier = "\n    <header>\n      <identifier>"+identifier+"</identifier>"
    headerDatestamp = "\n      <datestamp>"+str(datetime.now())+"</datestamp>\n    </header>\n"
    
    header = []
    header.append(headerIdentifier)
    header.append(headerDatestamp)
    strHead = ''.join([str(elem) for elem in header]) 

    record = []
    record.append(strHead)
    record.append(data)
    strRec = ''.join([str(elem) for elem in record]) 

    responseEnd = "\n  <record>\n </GetRecord>\n</OAI-PMH>"
    response.append(strRec)
    response.append(responseEnd)
    strResp = ''.join([str(elem) for elem in response])
    
    print(strResp)
  
elif (query == 'Identify'):
    """Retrieve information about the repository.

    Returns an Identify object describing the repository.
    """
    print ("<OAI-PMH> fill in Identify response according to protocol...</OAI-PMH>")
  
elif (query == 'ListIdentifiers'):
    """Get a list of header information on records.

        metadataPrefix - identifies metadata set to retrieve
        set - set identifier; only return headers in set (optional)
        from_ - only retrieve headers from from_ date forward (optional)
        until - only retrieve headers with dates up to and including
                until date (optional)

        Should raise error.CannotDisseminateFormatError if metadataPrefix
        is not supported by the repository.

        Should raise error.NoSetHierarchyError if the repository does not
        support sets.
        
        Returns an iterable of headers.
        """
  #  metadataPrefix = form.getvalue ("metadataPrefix", "")
  #  set = form.getvalue ("set", "")
  #  frm = form.getvalue ("from", "")
  #  until = form.getvalue ("until", "")
    
    metadataPrefix = "oai_dc"
    set = "Sci"
    frm = str(datetime.now())
    until = str(datetime.now())
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n  <request verb=\"ListIdentifiers\" from=\""
    verbRequest += frm+"\"\n           metadataPrefix=\""
    verbRequest += metadataPrefix+"\"\n           set=\""
    verbRequest += set+"\">"+baseURL+"</request>\n  <ListIdentifiers>"
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            
            identifier = str(i)
            
            response = []
            
            if (i == 1):
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
  
            fileName = "stories-dc/metadata-"+str(i)+"-dc.xml"

            try:
                with open(fileName) as file:
                    data = file.read()
                    file.close()
            except Exception as e:
                print(e)
                print(fileName)
                print("File Error")
                
            splitString = "<datestamp>"
            split = data.split(splitString)
            
            if len(split) == 2:
                splitString = "\<datestamp>"
                split = data.split(splitString)
                part1 = split[0]
                datestamp = part1

            headerIdentifier = "\n   <header>\n    <identifier>"+identifier+"</identifier>"
            headerDatestamp = "\n    <datestamp>"+datestamp+"</datestamp>"
            
            headerSetSpec = "\n    <setSpec>"+set+"</setSpec>"
            headerSetSpec +=  "\n   </header>"
            
            header = []
            header.append(headerIdentifier)
            header.append(headerDatestamp)
            header.append(headerSetSpec)
            strHead = ''.join([str(elem) for elem in header]) 

            record = []
            record.append(strHead)
            record.append(data)
            record.append("</record>")
            strRec = ''.join([str(elem) for elem in record]) 
            
            response.append(strRec)
            strResp = ''.join([str(elem) for elem in response]) 
            
            print(strResp)
            
        responseEnd = " </ListIdentifiers>\n</OAI-PMH>"
        print(responseEnd)
        break

elif (query == 'ListMetadataFormats'):
    """List metadata formats supported by repository or record.

    identifier - identify record for which we want to know all
                    supported metadata formats. if absent, list all metadata
                    formats supported by repository. (optional)

    Should raise error.IdDoesNotExistError if record with
    identifier does not exist.
    
    Should raise error.NoMetadataFormatsError if no formats are
    available for the indicated record.

    Returns an iterable of metadataPrefix, schema, metadataNamespace
    tuples (each entry in the tuple is a string).
    """
    
    identifier = "1"
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n  <request verb=\"ListMetadataFormats\"\n identifier=\""
    verbRequest += identifier+"\">\n"
    verbRequest += baseURL+"</request>\n  <ListMetadataFormats>"
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            
            identifier = str(i)
            
            response = []
            
            if (i == 1):
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
  
            fileName = "stories-dc/metadata-"+str(i)+"-dc.xml"
            
            try:
                with open(fileName) as file:data = file.read()
            file.close()
            except Exception as e:
                print(e)
                print(fileName)
                print("File Error")
                
            splitString = "<datestamp>"
            split = data.split(splitString)
            
            if len(split) == 2:
                splitString = "\<datestamp>"
                split = split[1].split(splitString)
                part1 = split[0]
                datestamp = part1

            headerIdentifier = " <header>\n  <identifier>"+identifier+"</identifier>"
            headerDatestamp = "\n  <datestamp>"+datestamp+"</datestamp>"
            
            headerSetSpec = "<setSpec>"+set+"</setSpec>"
            headerSetSpec +=  "\n</header>"
            
            header = []
            header.append(headerIdentifier)
            header.append(headerDatestamp)
            header.append(headerSetSpec)
            strHead = ''.join([str(elem) for elem in header]) 

            record = []
            record.append(strHead)
            record.append(data)
            record.append("</record>")
            strRec = ''.join([str(elem) for elem in record]) 
            
            response.append(strRec)
            strResp = ''.join([str(elem) for elem in response]) 
            
            print(strResp)
            
        responseEnd = " </ListMetadataFormats>\n</OAI-PMH>"
        print(responseEnd)
        break

elif (query == 'ListRecords'):
    """Get a list of header, metadata and about information on records.

    metadataPrefix - identifies metadata set to retrieve
    set - set identifier; only return records in set (optional)
    from_ - only retrieve records from from_ date forward (optional)
    until - only retrieve records with dates up to and including
            until date (optional)

    Should raise error.CannotDisseminateFormatError if metadataPrefix
    is not supported by the repository.

    Should raise error.NoSetHierarchyError if the repository does not
    support sets.

    Returns an iterable of header, metadata, about tuples.
    """
    
    #metadataPrefix = form.getvalue ("metadataPrefix", "")
    #set = form.getvalue ("set", "")
    #frm = form.getvalue ("from", "")
    #until = form.getvalue ("until", "")
    
    metadataPrefix = "oai_dc"
    set = "Sci"
    frm = str(datetime.now())
    until = str(datetime.now())
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n <request verb=\"ListRecords\" from=\""
    verbRequest += frm+"\"\n          set=\""
    verbRequest += set+"\"\n          metadataPrefix=\""
    verbRequest += metadataPrefix+"\">"+"\n          "+baseURL+"</request>\n <ListRecords>\n"
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(5,7):
            
            identifier = str(i)
            
            response = []
            
            if (i == 1):
                response.append(verbResponseHeader)
                response.append(verbResponseDate)
                response.append(verbRequest)
  
            fileName = "stories-dc/metadata-"+str(i)+"-dc.xml"
            
            try:
                with open(fileName) as file:
                    data = file.read()
                    file.close()
            except Exception as e:
                print(e)
                print(fileName)
                print("File Error")
                
            splitString = "<dc:identifiers>"+identifier+"</dc:identifiers>"
                            
            split = data.split(splitString)
            
            if len(split) == 2:
                part1 = split[0]
                part1 = part1[39:len(part1)-3]
                part2 = split[1]
                data = part1+part2
            else:
                part1 = split[0]
                part1 = part1[39:len(part1)-3]
                data = part1
            
            data = "    <metadata>\n"+data+"    </metadata>"
            
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
            record.append("\n  </record>")
            strRec = ''.join([str(elem) for elem in record]) 
            
            response.append(strRec)
            strResp = ''.join([str(elem) for elem in response]) 
            
            print(strResp)
            
        responseEnd = " </ListRecords> \n</OAI-PMH>"
        print(responseEnd)
        break        

elif (query == 'ListSets'):    
    """Get a list of sets in the repository.

    Should raise error.NoSetHierarchyError if the repository does not
    support sets.

    Returns an iterable of setSpec, setName tuples (strings)."""

else:
# Error handling
    print ("Error")