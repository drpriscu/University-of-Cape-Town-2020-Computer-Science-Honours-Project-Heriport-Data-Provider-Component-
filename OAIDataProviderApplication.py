# Alex Priscu
# Program that takes in OAI-PMH Request verbs and provides Responses.
# OAI Data Provider Application
# 11 August 2020

#!/usr/bin/env python3

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
#"content-type: text/html; charset=UTF-8"
query = 'ListRecords'
serverURL = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/cgi-bin/OAIDataProviderApplicationBleekAndLloyd.py"
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
    identifier = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/6"
    set = "stories"
    
    splitString = "stories/"
    split = identifier.split(splitString)
    dcFilePath = splitString+split[1]+"/metadata-"+split[1]+"-dc.xml"
    
    try:
        with open(dcFilePath, encoding="utf-8") as dcFile:
            data = dcFile.read()
            dcFile.close()
    except:
        print("idDoesNotExist")
    
    if(metadataPrefix != "oai_dc"):
            print("cannotDisseminateFormat")
            sys.exit()
    
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

elif (query == 'Identify'):
    """Retrieve information about the repository.

    Returns an Identify object describing the repository.
    """
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
    
    verbRequest = "\n  <request verb=\"Identify\">"
    verbRequest += serverURL+"</request>\n  <Identify>\n"
    
    repositoryName = "The New Bleek and Lloyd Collection"
    repositoryIdentifier = "http://pumbaa.cs.uct.ac.za"
    earliestDatestamp = str(datetime.now())
            
    path = 'stories/'
    
    for root, directories, filenames in os.walk(path):
        for i in range(1,2058):
            identifier = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/"+str(i)
                          
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
            split = split[0].split(" ")
            recordDate = split[0]
                    
            if((recordDate <= earliestDatestamp)):
                earliestDatestamp = recordDate
        break
    
    data = "    <repositoryName>"+repositoryName+"</repositoryName>"
    data += "\n    <baseURL>"+serverURL+"<baseURL>"
    data += "\n    <protocolVersion>2.0</protocolVersion>"
    data += "\n    <adminEmail>admin@pumbaa.cs.uct.ac.za</adminEmail>"
    data += "\n    <earliestDatestamp>"+earliestDatestamp+"<\earliestDatestamp>"
    data += "\n    <deletedRecord>no</deletedRecord>"
    data += "\n    <granularity>YYYY-MM-DDThh:mm:ssZ</granularity>"
    
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
    
    responseEnd = "\n </Identify>\n</OAI-PMH>"
    response.append(strRec)
    response.append(responseEnd)
    strResp = ''.join([str(elem) for elem in response])
    
    print(strResp)
    
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
            split = split[0].split(" ")
            recordDate = split[0]
            
            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
            
            if((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                
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
    
    identifier = "http://pumbaa.cs.uct.ac.za/~balnew/metadata/stories/6"
  
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
    
    try:
        #identifier = form.getvalue ("identifier", "")
        identifier = identifier
        verbRequest = "\n  <request verb=\"ListMetadataFormats\"\n    identifier=\""
        verbRequest += identifier+"\">\n    "+serverURL+"</request>\n  <ListMetadataFormats>\n"
    
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
    
    except:
        verbRequest = "\n  <request verb=\"ListMetadataFormats\">\n"
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
    set = "stories"
    frm = "2020-01-01"
    until = datetime.today().strftime('%Y-%m-%d')
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n  <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
            
    verbRequest = "\n  <request verb=\"ListRecords\" from=\""
    verbRequest += frm+"\"\n           set=\""
    verbRequest += set+"\"\n           metadataPrefix=\""
    verbRequest += metadataPrefix+"\">"+"\n           "+serverURL+"</request>\n <ListRecords>\n"
    
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
            split = split[0].split(" ")
            recordDate = split[0]
                  
            recordDateObject = datetime.strptime(recordDate, "%Y-%m-%d")
            frmDateObject = datetime.strptime(frm, "%Y-%m-%d")
            untilDateObject = datetime.strptime(until, "%Y-%m-%d")
            
            if((recordDateObject >= frmDateObject) and (recordDateObject <= untilDateObject)):
                    
                data = "     <metadata>\n      "+data[39:len(data)]+"     </metadata>"
                about = "\n     <about>"
                provenance = "        xmlns=\"http://www.openarchives.org/OAI/2.0/provenance\"\n        xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n        xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/provenance\n        http://www.openarchives.org/OAI/2.0/provenance.xsd\">"
                
                about += "\n       <provenance>\n"+provenance+"\n       </provenance>"
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
                    
        responseEnd = "  </ListRecords>\n</OAI-PMH>"
        print(responseEnd)
        break      
    
elif (query == 'ListSets'):
    """Get a list of sets in the repository.

    Should raise error.NoSetHierarchyError if the repository does not
    support sets.

    Returns an iterable of setSpec, setName tuples (strings)."""
    
    verbResponseHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<OAI-PMH xmlns=\"http://www.openarchives.org/OAI/2.0/\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/\n         http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd\">"
    verbResponseDate = "\n <responseDate>"
    verbResponseDate += str(datetime.now())
    verbResponseDate += "</responseDate>"
    
    verbRequest = "\n <request verb=\"ListSets\">"
    verbRequest += serverURL+"</request>\n <ListSets>\n"

    response = []
    response.append(verbResponseHeader)
    response.append(verbResponseDate)
    response.append(verbRequest)
    
    set = "stories"
    data = "  <set>\n    <setName>"+set+"</setName>\n    <setDescription>"
    data += "\n      <oai_dc:dc\n          xmlns:oai_dc=\"http://www.openarchives.org/OAI/2.0/oai_dc/\"\n          xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n          xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n          xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/oai_dc/\n          http://www.openarchives.org/OAI/2.0/oai_dc.xsd\">"
    data += "\n          <dc:description>This set contains metadata describing stories from the Bleek and Lloyd Collection.</dc:description>"
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
# Error handling
    print ("Error")