
Project: Data Provider Interfaces component of - HERIPORT - a low-cost South African national heritage Web portal built with metadata aggregation (1/10/2020).

# About

The Data Provider Interface is a software component that comprises of two Python scripts, that map Data Provider XML metadata records to (unqualified) Dublin Core (DC) and expose the metadata using the Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH). The OAI-PMH Data Provider Interface is designed to be run on a Web server and process HTTP requests, parse arguments, create arguments-based record requests, and produce XML record responses. 

When a Service Provider sends an OAI-PMH request to the OAI-PMH Data Provider. The request is then handled by methods located in the Python script. These methods include reading the original metadata and converting it to the DC format in the DC Converter script. The Data Provider Interface script then requests the DC converted metadata and returns the appropriate OAI-PMH response to the Service Provider, who can then store the metadata in their harvested metadata collection. A DC Converter Tester is used to evaluate whether A DC Converter can produce XML metadata records that conforms to the DC schema - oai_dc.xsd

Current Data Providers: The New Digital Bleek and Lloyd Archive, The Five Hundred Year Archive and The Metsemegologolo Archive.
Original XML metadata record collections (sets): FHYA Depot, Metsemegologolo and stories.
Data Provider names: BleekAndLloyd, FHYA and Metsemegologolo.
Executables: <Data Provider Name>OAIInterface.py, <Data Provider Name>DCConverter.py and DCConverterTester.py files.

## Assumptions
*DC Converter Tester application is run on a Data Provider DC Converter before developing the Data Provider Interface.
*DC Converter application and OAI-PMH Data Provider Interface will be configured for a Data Provider not listed above.
*Current Data Providers use the server URL: http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/

### Prerequisites
*Server running Data Provider Interface/s contains a directory named: "/home/public_html/cgi-bin", with permissions 755.
*Executable files are located in the "/home/public_html/cgi-bin" directory.
*Data Provider XML metadata collections are located in the same directory as the executable files.
*Support files listed in Acknowledgments are located in the same directory as the executable files.
*Python packages listed in Acknowledgments are installed using pip3 for Python.
*Python 3 is installed on the environment operating system.
*CGI is configured on the environment operating system.
*Data Provider executes the <Data Provider Name>DCConverter.py before the <Data Provider Name>OAIInterface.py.

#### Installing

*Perform these operations in a terminal*

1. Unzip the DataProvider.zip in the "/home/public_html/cgi-bin" directory.
2. Change the working directory permissions by typing: chmod 755 -R *

##### Running

-----------------------------------------------------------------------
To run a DC Converter application: <Data Provider Name>DCConverter.py

*Perform this operation in a terminal*

1. Run by typing: python3 <Data Provider Name>DCConverter.py
Example: python3 MetsemegologoloDCConverter.py
-----------------------------------------------------------------------
To run the DC Converter tester application: DCConverterTester.py

*Perform these operations in a terminal*

1. Run by typing: python3 DCConverterTester.py
2. Enter a name of a Data Provider DC Converter application.
Example: BleekAndLloydDCConverter.py
-----------------------------------------------------------------------
To Interface with a Data Provider Interface: <Data Provider Name>OAIInterface.py.

*Perform this operation in a Web browser*

1. Enter the server URL concatenated with the name of the Data Provider Interface and valid OAI-PMH request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py?

Example: http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListRecords&metadataPrefix=oai_dc
-----------------------------------------------------------------------
To call each verb of the Data Provider Interface: <Data Provider Name>OAIInterface.py.

Date granularity: YYYY-MM-DD
Metadata Preifx: oai_dc
Set: Data Provider XML metadata record collection.

resumptionToken Request Format:
resumptionToken=Next record Index,Expiration Date,metadataPrefix,from,until,set
Where from, until and set are optional arguments and Next record Index, Expiration Date and metadataPrefix are required.
Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListRecords&resumptionToken=11,e2020-10-05T18:20:15Z,oai_dc

resumptionToken Response Format: 
<resumptionToken expirationDate=YYYY-MM-DDTHH:MM:SSZ completeListSize>Next record Index,Expiration Date,metadataPrefix,from,until,set</resumptionToken>
Example: 
<resumptionToken expirationDate="2020-10-05T18:20:15Z"completeListSize="87">11,e2020-10-05T18:20:15Z,oai_dc</resumptionToken>

*Perform these operations in a Web browser*

To request GetRecord:
2.1 Enter the server URL concatenated with the name of the Data Provider Interface and GetRecord request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=GetRecord

With Arguments:
identifier
metadataPrefix

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=GetRecord&metadataPrefix=oai_dc&identifier=http://emandulo.apc.uct.ac.za/metadata/FHYA%20Depot/1

To request Identify:
2.2 Enter the server URL concatenated with the name of the Data Provider Interface and Identify request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=Identify

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=Identify

To request ListIdentifiers:
2.3 Enter the server URL concatenated with the name of the Data Provider Interface and ListIdentifiers request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=ListIdentifiers

With Arguments:
from
until
metadataPrefix
set
resumptionToken

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListIdentifiers&metadataPrefix=oai_dc

To request ListMetadataformats:
2.4 Enter the server URL concatenated with the name of the Data Provider Interface and ListMetadataformats request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=ListMetadataformats

With Argument:
identifier

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListMetadataFormats&identifier=http://emandulo.apc.uct.ac.za/metadata/FHYA Depot/1

To request ListRecords:
2.5 Enter the server URL concatenated with the name of the Data Provider Interface and ListRecords request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=ListRecords

With Arguments:
from
until
set
resumptionToken X
meta R

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListRecords&metadataPrefix=oai_dc&from=2000-01-01&until=2020-11-01

To request ListSets:
2.6 Enter the server URL concatenated with the name of the Data Provider Interface and ListSets request by typing:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/<Data Provider Name>OAIInterface.py.py?verb=ListSets

Example:
http://rafiki1.cs.uct.ac.za/~alex/cgi-bin/FHYAOAIInterface.py?verb=ListSets

###### Files

DC Converter Applications:
BleekAndLloydDCConverter.py, FHYADCConverter.py and MetsemegologoloDCConverter.py. 

All three scripts are designed to convert XML metadata records read in from a directory path and output the converted DC XML metadata records in the same directory so that they can be accessed by the OAI-PMH Data Provider Interfaces.

Sample records from the Data Providers adhered to an incremental number indexing convention for each directory sub-folder. As a result, each sub-folder can be accessed by the corresponding number and each sub-folder contains an XML metadata file. When a file is converted the terminal prints “Successfully created file: metadata-#-dc.xml”. When all files are converted, the terminal prints “Successfully converted files.”

DC Converter Tester Application:
DCConverterTester.py

Input is a valid name for one of the three DC Converters. The Tester then runs the DC Converter and performs two tests on each DC Data Provider XML metadata record. The first case tests if XML is well-formed. The second case tests metadata validity against the imported DC schema file - oai_dc.xsd. After each record is read in and tested, the total number of successfully converted records is compared to the total number of records read in.

OAI-PMH Data Provider Interfaces:
BleekAndLloydOAIInterface.py, FHYAOAIInterface.py and MetsemegogoloOAIInterface.py. 

All three scripts are able to receive OAI-PMH requests and output OAI-PMH responses based on the DC metadata records generated by the DC Converters. Using conditional statements, each script responds to OAI-PMH verb values.

####### Built With

* [Visual Studio Code] - Used to write code.
* [Mac OSX Terminal] - Used to manage git repo and run files.
* [Ubunutu Web Server] - Used to host the Data Provider Interfaces that received and outputted OAI-PMH requests and responses. 

######## Versioning

Final Submitted Version

######### Author

Alex Priscu
PRSALE003

########## License

Not Applicable.

########### Acknowledgments

Python Packages:

lxml:
lxml dev team, March 2006
License: BSD License (BSD)
Homepage: https://lxml.de/

simpledc (dcxml):
CERN, March 2016
License: MIT License
Copyright (C) 2016-2018 CERN.
Homepage: https://github.com/inveniosoftware/dcxml

xmltodict:
Martin Blech, July 2012
License: MIT License
Homepage: https://github.com/martinblech/xmltodict

xmlutils:
Kailash Nadh, October 2011
License: MIT License
Homepage: https://github.com/knadh/xmlutils.py

Open Archives Initiative Repository Explorer Tool:
Hussein Suleman, September 2014  
Homepage: http://dl.cs.uct.ac.za/projects/re/

XML Schema:

oai_dc.xsd: Adjusted for usage in the OAI-PMH.
Pete Johnston, March 2002
Schema imports the Dublin Core elements from the DCMI schema for unqualified Dublin Core.
http://www.openarchives.org/OAI/2.0/oai_dc/
http://purl.org/dc/elements/1.1/
http://www.w3.org/2001/XMLSchema
http://www.openarchives.org/OAI/2.0/oai_dc/