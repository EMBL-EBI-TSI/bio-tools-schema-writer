import gspread
from oauth2client.service_account import ServiceAccountCredentials
import xml.etree.ElementTree as ET
import xml.dom.minidom

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

print 'Authorising with googleDocs...'
gc = gspread.authorize(credentials)

wks = gc.open_by_key('1YYmvAD8xpB5UIG86YLS5-vEKNTnnEH4M1t9zDeXJ1Rk').get_worksheet(9)

print 'Parsing spreadsheet...'
xml_output_resources = ET.Element('resources')

for row_i in xrange(3,35):
	# Fetch a row
	row = wks.row_values(row_i)
	
	# create resource element
	xml_output_resource = ET.SubElement(xml_output_resources, 'resource')
	
	# set name
	xml_output_resource_name = ET.SubElement(xml_output_resource, 'name')
	xml_output_resource_name.text = row[0]
	
	# set homepage
	xml_output_resource_homepage = ET.SubElement(xml_output_resource, 'homepage')
	xml_output_resource_homepage.text = row[1]
	
	# set resource type
	xml_output_resource_resource_type = ET.SubElement(xml_output_resource, 'resourceType')
	xml_output_resource_resource_type.text = row[2]

	# set interface type
	xml_output_resource_interface = ET.SubElement(xml_output_resource, 'interface')
	xml_output_resource_interface_type = ET.SubElement(xml_output_resource_interface, 'interfaceType')
	xml_output_resource_interface_type.text = row[3]
	
	# set description
	xml_output_resource_description = ET.SubElement(xml_output_resource, 'description')
	xml_output_resource_description.text = row[10]

	# set topic
	xml_output_resource_topic = ET.SubElement(xml_output_resource, 'topic')
	xml_output_resource_topic.text = row[4]
	xml_output_resource_topic.set('uri','http://edamontology.org/topic_'+row[5])

	# set function
	xml_output_resource_function = ET.SubElement(xml_output_resource, 'function')
	xml_output_resource_function_name = ET.SubElement(xml_output_resource_function, 'functionName')
	xml_output_resource_function_name.text = row[6]
	xml_output_resource_function_name.set('uri','http://edamontology.org/operation_'+row[7])

	# set contact
	xml_output_resource_contact = ET.SubElement(xml_output_resource, 'contact')
	xml_output_resource_contact_name = ET.SubElement(xml_output_resource_contact, 'contactName')
	xml_output_resource_contact_name.text = row[8]
	xml_output_resource_contact_email = ET.SubElement(xml_output_resource_contact, 'contactEmail')
	xml_output_resource_contact_email.text = row[9]

# write xml file
print 'Writing to file...'
xmlstr = xml.dom.minidom.parseString(ET.tostring(xml_output_resources)).toprettyxml(indent="   ")
with open("bio_excel.xml", "w") as f:
    f.write(xmlstr)

print 'DONE!'