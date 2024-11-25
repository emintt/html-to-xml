
# Function to write an XML tree to a file with a custom XML declaration using double quotes.
def write_xml_with_custom_declaration(tree, file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        # Write the XML declaration with double quotes
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        # Write the rest of the XML content without the XML declaration
        tree.write(file, encoding="unicode")