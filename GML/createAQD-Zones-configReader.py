import ConfigParser
from pprint import pprint

from xml.dom import minidom 


'''
Created by Dr. Peter Mooney
Department of Computer Science, National University of Ireland Maynooth - and Environmental Research Centre, Environmental Protection Agency Ireland. 

Please read the README.

Backup important files before running this code! 

Read the gml.cfg file carefully also. 

'''

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

def printInspireID(zoneID,baseNameSpace):
	print (tab(2) + "<am:inspireId>")
	print (tab(3) + "<base:Identifier>")
	print (tab(4) + "<base:localId>"  + str(zoneID) + "</base:localId>")
	print (tab(4) + "<base:namespace>"  + str(baseNameSpace) + "</base:namespace>")
	print (tab(3) + "</base:Identifier>")
	print (tab(2) + "</am:inspireId>")
	
	
	

def readGMLForFeatures():

	__ERROR_STRING__ = ""
	
	__ErrorCount__ = 0

	# read the config file - so that we don't hardcode in the names of the attributes
	
	config = ConfigParser.RawConfigParser()
	config.read('gml.cfg')
	
	featureTypeName = ""
	_baseNameSpace_ = ""
	_shapefileName_ = ""
	zoneIDVariableName = ""
	actualNameOfZoneVariableName = ""
	populationVariableName = ""
	typeOfZoneVariableName = ""
	pollutantListVariableName = ""
	geometryVariableName = ""
	populationYearName = ""
	srsName = ""
	__INPUT_GML_FILE_NAME__ = ""	
	
	 
	try:
		# the top level name for the feature geometry for each zone. 
		featureTypeName = config.get('ZoneDBF', 'featureTypeName2')
	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for Feature Type Name in gml.cfg"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)
		
	try:
		# base name space (inspire)
		_baseNameSpace_ = config.get('ZoneDBF','baseNameSpace')
	
	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for Base Name Space in gml.cfg"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)	
	
	
	try:
		# the name of the original shapefile 
		_shapefileName_ = config.get('ZoneDBF','shapefileName')

	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for Shapefile Name in gml.cfg - you must supply the name of the shapefile"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)	
	
	try:
		# this is the name of the attribute in the DBF file that holds the Zone ID or EIONET code
		zoneIDVariableName = config.get('ZoneDBF', 'zoneIDVariableName')
	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for zoneIDVariableName in gml.cfg - you must supply name of the attribute holdinf the Zone ID in the input GML file"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)		
	
	try:
		# the actual text/local name of the Zone
		actualNameOfZoneVariableName = config.get('ZoneDBF', 'actualNameOfZoneVariableName')
	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for actualNameOfZoneVariableName in gml.cfg - you must supply name of the attribute holding the text name of the zone in the input GML file"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)		
		
	try:
		# the name of the attribute in the DBF file that holds the population value for this zone
		populationVariableName = config.get('ZoneDBF', 'populationVariableName')
	except ConfigParser.NoOptionError:
		__ERROR_STRING__ = __ERROR_STRING__ + "\nNo Option Error for populationVariableName in gml.cfg - you must supply name of the attribute holding the population value of the zone in the input GML file"
		__ErrorCount__ = __ErrorCount__ + 1
		print (__ERROR_STRING__)		
		
	
	# the name of the attribute in the DBF file that holds the type (agglom or non-aglom) value for this zone
	typeOfZoneVariableName = config.get('ZoneDBF', 'typeOfZoneVariableName')
	# this is hte name of the attribute in the DBF file that holds the list of pollutants (and maybe protection targets) for the 
	# pollutants/metals measured in this zone. 
	pollutantListVariableName = config.get('ZoneDBF', 'pollutantListVariableName')
	# the actual geometry of the zone - the name of the attibute/column in the DBF file holding the geometry.
	geometryVariableName = config.get('ZoneDBF', 'geometryVariableName')

	# the year which the population number was measured at - this is in the config file. 
	populationYearName = config.get('ZoneDBF', 'populationYearName')
	
	# the number of the spatial reference system that the coordinates in the originating GML file are specified in 
	srsName = config.get('ZoneDBF', 'srsName')

	# IMPORTANT
	# the name - or full path - to the input GML file...
	__INPUT_GML_FILE_NAME__ = config.get('ZoneDBF','inputGMLFile')

	
	#####
	##### BEGIN READING AND PROCESSING. 
	#####
	
	# read in the GML file. 
	gmldoc = minidom.parse(__INPUT_GML_FILE_NAME__)
	


	# this should be fairly generic - if you use an ogr2ogr based transformation of
	# your shapefile to GML. . 
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
			
			# this is the zoneID - and it's proper name is in the config file. 
			zoneID = returnTagTextValue(ogrAIRZONES[j],zoneIDVariableName)
			
			__GML_ID__ = str(zoneID) + "__" + str(i) # this is unique 
			
			print ("<!-- Write out the XML for the feature member " + __GML_ID__ + " -->")
			
			print ("<gml:featureMember>")
			print (tab(1) + "<aqd:AQD_Zone gml:id=\"" + __GML_ID__ + "\">")


			# the actual name of the zone . . in the config file. 
			aqZone  = returnTagTextValue(ogrAIRZONES[j],actualNameOfZoneVariableName)

			# read from the config file....
			population = returnTagTextValue(ogrAIRZONES[j],populationVariableName)

			# read from the config file... 
			aggType = returnTagTextValue(ogrAIRZONES[j],typeOfZoneVariableName)
			
			printInspireID(zoneID,_baseNameSpace_)
			printAmNameGML(_shapefileName_,aqZone)
			
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
			print (tab(2) + "<aqd:residentPopulationYear>" + str(populationYearName) + "</aqd:residentPopulationYear>")
			# this needs to be XML as it is the GML of the polygon... 
			# the geometry should be already created by the GML - so it is actually 
			# just really a copy and paste of the geometry. 
			# we get the name of the attribute from the Shapefile in the config file. 
			ogrGeom = ogrAIRZONES[j].getElementsByTagName(geometryVariableName)
			
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
				theGeometry = theGeometry.replace("<gml:MultiPolygon>", "<gml:MultiPolygon srsName=\"" + srsName + "\" gml:id=\"GeomID_" +  str(zoneID) + "__" + str(i) + "\">",1)
			else:
				print ("<!-- this is a gml polygon  - local id supplied and SRS -->")
				theGeometry = theGeometry.replace("<gml:Polygon>", "<gml:Polygon srsName=\"" + srsName + "\" gml:id=\"GeomID_" +  str(zoneID) + "__" + str(i) + "\">",1)

			print (tab(3) + theGeometry)
			print (tab(2) + "</am:geometry>")			
			print ("<!-- The GML geometry object ENDS here .. -->")
			
			# the name of the attribute variable for pollutant. 
			pollutantList = returnTagTextValue(ogrAIRZONES[j],pollutantListVariableName)
			
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
