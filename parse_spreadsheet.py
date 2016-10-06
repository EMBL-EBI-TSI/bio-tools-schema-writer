import gspread
from oauth2client.service_account import ServiceAccountCredentials
import xml.etree.ElementTree as ET
import xml.dom.minidom
import json

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

print 'Authorising with googleDocs...'
gc = gspread.authorize(credentials)

wks = gc.open_by_key('1YYmvAD8xpB5UIG86YLS5-vEKNTnnEH4M1t9zDeXJ1Rk').get_worksheet(9)

print 'Parsing spreadsheet...'
xml_output_resources = ET.Element('resources')
json_output = []

for row_i in xrange(3,35):
	json_output_elem = {}

	# Fetch a row
	row = wks.row_values(row_i)
	
	# create XML resource element
	xml_output_resource = ET.SubElement(xml_output_resources, 'resource')
	
	# set name
	xml_output_resource_name = ET.SubElement(xml_output_resource, 'name')
	xml_output_resource_name.text = row[0]
	json_output_elem["name"] = row[0]
	json_output_elem["id"] = row[0].replace(" ", "").replace("(","").replace(")","")

	# set homepage
	xml_output_resource_homepage = ET.SubElement(xml_output_resource, 'homepage')
	xml_output_resource_homepage.text = row[1]
	json_output_elem["homepage"] = row[1]

	# set collection
	xml_output_resource_collection = ET.SubElement(xml_output_resource, 'collection')
	xml_output_resource_collection.text = 'BioExcel'
	json_output_elem["collection"] = [ 'BioExcel' ]

	# set resource type
	json_output_elem["resourceType"] = []
	for resource_type_elem in row[2].split(','):
		xml_output_resource_resource_type = ET.SubElement(xml_output_resource, 'resourceType')
		xml_output_resource_resource_type.text = resource_type_elem.strip()
		json_output_elem["resourceType"].append(resource_type_elem.strip())
	

	# set interface type
	json_output_elem["interface"] = []
	for intercace_type_elem in row[3].split(','):
		xml_output_resource_interface = ET.SubElement(xml_output_resource, 'interface')
		xml_output_resource_interface_type = ET.SubElement(xml_output_resource_interface, 'interfaceType')
		xml_output_resource_interface_type.text = intercace_type_elem.strip()
		interfaceType = {}
		interfaceType["interfaceType"] = intercace_type_elem.strip()
		json_output_elem["interface"].append(interfaceType)

	# set description
	xml_output_resource_description = ET.SubElement(xml_output_resource, 'description')
	xml_output_resource_description.text = row[11]
	json_output_elem["description"] = row[11]
	if len(json_output_elem["description"])<1:
		json_output_elem["description"] = json_output_elem["name"]

	# set topic
	xml_output_resource_topic = ET.SubElement(xml_output_resource, 'topic')
	xml_output_resource_topic.text = row[4]
	xml_output_resource_topic.set('uri','http://edamontology.org/topic_' + row[5])
	json_output_elem["topic"] = []
	json_topic = {}
	json_topic["uri"] = 'http://edamontology.org/topic_' + row[5]
	json_topic["term"] = row[4]
	json_output_elem["topic"].append(json_topic)

	# set function
	xml_output_resource_function = ET.SubElement(xml_output_resource, 'function')
	xml_output_resource_function_name = ET.SubElement(xml_output_resource_function, 'functionName')
	xml_output_resource_function_name.text = row[6]
	xml_output_resource_function_name.set('uri','http://edamontology.org/operation_' + row[7])
	json_output_elem["function"] = []
	json_function = {}
	json_function["functionName"] = []
	json_function_name = {}
	json_function_name["uri"] = 'http://edamontology.org/operation_' + row[7]
	json_function_name["term"] = row[6]
	json_function["functionName"].append(json_function_name)
	json_output_elem["function"].append(json_function)

	# set contact
	xml_output_resource_contact = ET.SubElement(xml_output_resource, 'contact')
	json_output_elem["contact"] = []
	json_contact = {}
	if len(row[9]) > 0:
		xml_output_resource_contact_email = ET.SubElement(xml_output_resource_contact, 'contactEmail')
		xml_output_resource_contact_email.text = row[9]
		json_contact["contactEmail"] = row[9]

	if len(row[10]) > 0:
		xml_output_resource_contact_email = ET.SubElement(xml_output_resource_contact, 'contactURL')
		xml_output_resource_contact_email.text = row[10]
		json_contact["contactURL"] = row[10]

	xml_output_resource_contact_name = ET.SubElement(xml_output_resource_contact, 'contactName')
	xml_output_resource_contact_name.text = row[8]
	json_contact["contactName"] = row[8]
	json_output_elem["contact"].append(json_contact)

	# add json elem to list
	json_output.append(json_output_elem)


# write xml file
print 'Writing to XML file...'
xmlstr = xml.dom.minidom.parseString(ET.tostring(xml_output_resources)).toprettyxml(indent="   ")
with open("bio_excel.xml", "w") as fxml:
  fxml.write(xmlstr)

# write JSON file
print 'Writing to JSON file...'
with open("bio_excel.json", "w") as fjson:
	json.dump(json_output, fjson, indent=2)

print 'DONE!'