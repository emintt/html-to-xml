
# Function to write an XML tree to a file with a custom XML declaration using double quotes.
def write_xml_with_custom_declaration(tree, file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        # Write the XML declaration with double quotes
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        # Write the rest of the XML content without the XML declaration
        tree.write(file, encoding="unicode")

def update_xml_attributes(root, attributes):
    for tag, attr_values in attributes.items():
        for elem in root.iter(tag):
            for key, value in attr_values.items():
                elem.attrib[key] = str(value)


def update_elements_text(root, tag_values):
    for tag, value in tag_values.items():
        for elem in root.iter(tag):
            elem.text = value