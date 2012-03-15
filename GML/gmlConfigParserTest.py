import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('gml.cfg')

# this is the name of the attribute in the DBF file that holds the Zone ID or EIONET code
zoneIDVariableName = config.get('ZoneDBF', 'zoneIDVariableName')
# the actual text/local name of the Zone
actualNameOfZoneVariableName = config.get('ZoneDBF', 'actualNameOfZoneVariableName')
# the name of the attribute in the DBF file that holds the population value for this zone
populationVariableName = config.get('ZoneDBF', 'populationVariableName')
# the name of the attribute in the DBF file that holds the type (agglom or non-aglom) value for this zone
typeOfZoneVariableName = config.get('ZoneDBF', 'typeOfZoneVariableName')
# this is hte name of the attribute in the DBF file that holds the list of pollutants (and maybe protection targets) for the 
# pollutants/metals measured in this zone. 
pollutantListVariableName = config.get('ZoneDBF', 'pollutantListVariableName')
# the actual geometry of the zone - the name of the attibute/column in the DBF file holding the geometry.
geometryVariableName = config.get('ZoneDBF', 'geometryVariableName')

print geometryVariableName
