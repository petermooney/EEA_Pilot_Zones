from xml.dom import minidom 

def readGMLExample(fileToRead):
	gmldoc = minidom.parse(fileToRead) # read in the GML file
	
	# first element in the hierarchy is gml:featureMember - access this
	gmlfeatureMember = gmldoc.getElementsByTagName('gml:featureMember')

	N = len(gmlfeatureMember) # the Number of GMLFeatureMembers
	# one for each zone.
	# let's iterate over the list of feature members
	i = 0
	while i < N:
		ogrAIRZONES = gmlfeatureMember[i].getElementsByTagName('ogr:AIRZONES')
		j = 0
		while j < len(ogrAIRZONES):
			# access various attributes of the zone in the GML
			zoneID = returnTagTextValue(ogrAIRZONES[j],'ogr:ZoneID')
			aqZoneName  = returnTagTextValue(ogrAIRZONES[j],'ogr:Name')
			population = returnTagTextValue(ogrAIRZONES[j],'ogr:Population')
			
			print("<gn:spelling><gn:spellingOfName><gn:text>")
			print(aqZoneName + "</gn:text><gn:script>Latn</gn:script></gn:spellingOfName></gn:spelling>")
			
			print ("\t<aqd:zoneCode>" + str(zoneID) + "</aqd:zoneCode>")
			print ("\t<aqd:LAU>unknown</aqd:LAU>")
			print ("\t<aqd:residentPopulation>" + str(population) + "</aqd:residentPopulation>\n")
			j = j + 1 
		i = i + 1

def returnTagTextValue(theParent,theTag):
	tagInfo = theParent.getElementsByTagName(theTag)
	strT = ""
	for t in tagInfo:
		strT = strT + t.childNodes[0].nodeValue

	return strT

readGMLExample("AIRZONES.gml")
