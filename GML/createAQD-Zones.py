import json
from pprint import pprint

from xml.dom import minidom 

"""
repeat the tab character n times. 
"""
def tab(n):
	return "\t"*n

# source name is the shapefile these data elements were extracted from
# text is the actual name of the zone

def printAmNameGML(sourceName,text):
	print (tab(2) + "<am:name>")
	print (tab(3) + "<gn:geographicalName>")
	print (tab(3) + "<gn:nativeness>edonym</gn:nativeness>")
	print (tab(3) + "<gn:nameStatus>standardised</gn:nameStatus>")
	print (tab(3) + "<gn:sourceOfName>" + sourceName + "</gn:sourceOfName>")
	print (tab(3) + "<gn:pronunciation nillReason=\"Unknown\" xsi:nil = \"true\"/>")
	print (tab(3) + "<gn:spelling>")
	print (tab(4) + "<gn:spellingOfName>")
	print (tab(5) + "<gn:text>" + text +  "</gn:text>")
	print (tab(5) + "<gn:script>Latn</gn:script>")
	print (tab(4) + "</gn:spellingOfName>")
	print (tab(3) + "</gn:spelling>")
	print (tab(3) + "</gn:geographicalName>")
	print (tab(2) + "</am:name>")

def printInspireID(zoneID):
	print (tab(2) + "<am:inspireId>")
	print (tab(3) + "<base:Identifier>")
	print (tab(4) + "<base:localId>"  + str(zoneID) + "</base:localId>")
	print (tab(4) + "<base:namespace>"  + str("aqd.ie.zones") + "</base:namespace>")
	print (tab(3) + "</base:Identifier>")
	print (tab(2) + "</am:inspireId>")
	
	
	

def readGMLForFeatures():
	gmldoc = minidom.parse('AIRZONES.gml')

	gmlfeatureMember = gmldoc.getElementsByTagName('gml:featureMember')
	
	N = len(gmlfeatureMember)
	
	i = 0
	topMatter = getXMLStaticValues("Top-of-GML.gml",0)
	print (topMatter)
	
	print ("<!-- Responsible Party Information  -->")
	
	responsibleParty = getXMLStaticValues("EPAResponsibleParty.xml",1)
	print (responsibleParty)
	
	print ("<!-- Now begin the zone information -->")
	
	while i < N:
		ogrAIRZONES = gmlfeatureMember[i].getElementsByTagName('ogr:AIRZONES')
		
		
		j = 0
		while j < len(ogrAIRZONES):
			
			
			zoneID = returnTagTextValue(ogrAIRZONES[j],'ogr:ZoneID')
			
			print ("<!-- Write out the XML for the feature member " + str(zoneID) + "__" + str(i) + " -->")
			ogrZoneID = ogrAIRZONES[j].getElementsByTagName('ogr:ZoneID')
			print ("<gml:featureMember>")
			print (tab(1) + "<aqd:AQD_Zone gml:id=\"" + str(zoneID) + "__" + str(i) + "\">")


			aqZone  = returnTagTextValue(ogrAIRZONES[j],'ogr:Name')

			
			population = returnTagTextValue(ogrAIRZONES[j],'ogr:Population')

			
			aggType = returnTagTextValue(ogrAIRZONES[j],'ogr:Type')
			
			printInspireID(zoneID)
			printAmNameGML("airQZonesIE.shp",aqZone)
			
			print (tab(3) + "<am:specialisedZoneType>")
			if (aggType == "nonag"):
				print (tab(4) + "nonagglomeration")
			else:
				print (tab(4) + "agglomeration")
			print (tab(3) + "</am:specialisedZoneType>")
			print ("<!-- In spreadsheet of mappings ... this is zoneType - left both here just to check them both-->")
			print (tab(3) + "<am:zoneType>")
			if (aggType == "nonag"):
				print (tab(4) + "nonagglomeration")
			else:
				print (tab(4) + "agglomeration")
			print (tab(3) + "</am:zoneType>")
			
			
			legalBasisEtc = getXMLStaticValues("LegalBasis-Section.gml",2)

			print (legalBasisEtc)
			

			
			print (tab(2) + "<aqd:zoneCode>" + str(zoneID) + "</aqd:zoneCode>")
			print (tab(2) + "<aqd:LAU>" + str("unknown") + "</aqd:LAU>")
			print (tab(2) + "<aqd:residentPopulation>" + str(population) + "</aqd:residentPopulation>")
			print (tab(2) + "<aqd:residentPopulationYear>" + str("2002-01-01") + "</aqd:residentPopulationYear>")
			# this needs to be XML as it is the GML of the polygon... 
			ogrGeom = ogrAIRZONES[j].getElementsByTagName('ogr:geometryProperty')
			
			## geometry starts here... 
			print ("<!-- The GML geometry object ENDS here .. -->")
			print (tab(2) + "<am:geometry>")
			
			theGeometry = ""
			print ("<!-- There are " + str(len(ogrGeom)) + " GML geometry objects -->")
			for z1 in ogrGeom:
				
				theGeometry = str(z1.childNodes[0].toxml())
			
			if (theGeometry.find("gml:MultiPolygon") >= 0):
				print ("<!-- this is a multipolygon - local id supplied and SRS -->")
				# need to replace with the coordinate reference system... 
				theGeometry = theGeometry.replace("<gml:MultiPolygon>", "<gml:MultiPolygon srsName=\"urn:ogc:def:crs:EPSG::4326\" gml:id=\"GeomID_" +  str(zoneID) + "__" + str(i) + "\">",1)
			else:
				print ("<!-- this is a gml polygon  - local id supplied and SRS -->")
				theGeometry = theGeometry.replace("<gml:Polygon>", "<gml:Polygon srsName=\"urn:ogc:def:crs:EPSG::4326\" gml:id=\"GeomID_" +  str(zoneID) + "__" + str(i) + "\">",1)

			print (tab(3) + theGeometry)
			print (tab(2) + "</am:geometry>")			
			print ("<!-- The GML geometry object ENDS here .. -->")
			
			pollutantList = returnTagTextValue(ogrAIRZONES[j],'ogr:Pollutant')
			
			print ("\t\t<!-- Metals and Pollutant listing .. -->")
			print ("<!-- Codelist not available - used chemical symbols as temporary data-->")
			printPollutantsListing(pollutantList)
			
			print (tab(1) + "</aqd:AQD_Zone>")
			print ("</gml:featureMember>")
			j = j + 1
		i = i + 1


	print ("</gml:FeatureCollection>")

# this is the semi colon separated list from the GML file. 
#SO2:HV;NO2:HV;PM10:H;PM25:H;Pb:H;C6H6:H;CO:H;O3:HV;As:H;Cd:H;Ni:H;Hg:H;PAH:H
def printPollutantsListing(pollList):
	
	individualPollutants = pollList.split(";")
	
	for poll in individualPollutants:
		
		# we need to split poll up...
		
		pollSplit = str(poll).split(":")
		
		print("<aqd:pollutants>")
		print("\t<aqd:pollutantCode>" + str(pollSplit[0]) + "</aqd:pollutantCode>")
		
		typeOfProtection = "Health and Vegetation/ecosystem"
		
		if (pollSplit[1] == "H"):
			typeOfProtection = "Health"
		
		print("\t<aqd:protectionTarget>" + str(typeOfProtection) + "</aqd:protectionTarget>")
		print("</aqd:pollutants>")
	


	#print gmlfeatureMember[0].toxml()
def returnTagTextValue(theParent,theTag):
	tagInfo = theParent.getElementsByTagName(theTag)
	strT = ""
	for t in tagInfo:
		strT = strT + t.childNodes[0].nodeValue

	return strT

def printResponsibleParty(respPartyName):
	print(tab(3) + "<aqd:AQD_ReportingUnits><am-ru:reportingAuthority>")
	print(tab(4) + "<gmd:CI_ResponsibleParty>")
	print(tab(5) + "<gmd:organisationName")
	print(tab(6) + str(respPartyName))
	print(tab(5) + "</gmd:organisationName")
	print(tab(4) + "</gmd:CI_ResponsibleParty>")
	print(tab(3) + "</am-ru:reportingAuthority>")
	print(tab(3) + "</aqd:AQD_ReportingUnits>")
	
def getXMLStaticValues(filename,tabbing):
	
	XML = ""
	
	for line in open(filename):
		XML = XML + tab(tabbing) + str(line)
	return XML

readGMLForFeatures()
