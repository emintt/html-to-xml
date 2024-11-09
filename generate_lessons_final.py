import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import shutil
import base64

# Function to convert an image URL to a Base64-encoded string
def image_url_to_base64(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

    return ""

# Function to write an XML tree to a file with a custom XML declaration using double quotes.
def write_xml_with_custom_declaration(tree, file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        # Write the XML declaration with double quotes
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

        # Write the rest of the XML content without the XML declaration
        tree.write(file, encoding="unicode")

# Define the HTML source file and the output folder
INPUT_FOLDER = "html-source\\FinalSDSChapter5WinningSupport\\"
INPUT_FILE_PATH = "{0}FinalSDSChapter5WinningSupport.html".format(INPUT_FOLDER)  # The HTML file to be processed

# Define the output folder
OUTPUT_FOLDER = "outputs\\for-many-lessons\\"

# Define the template folder
TEMPLATE_FOLDER = "templates\\for-many-lessons\\"
TEMPLATE_LESSON_FOLDER = "templates\\for-many-lessons\\lesson_441530_template\\"

# Define section number
SECTION_NUMBER = 4

# Load the HTML file
with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all img element and replace src attribute with the base64-encoded image
images = soup.findAll('img')
for image in images:
    # Construct image file path to create a local path on Windows
    img_file = "{0}{1}".format(INPUT_FOLDER, image['src'].replace("/","\\"))
    # Convert the image to base 64
    base64_img = "data:image/jpg;base64,{0}".format(image_url_to_base64(img_file))
    # Update src attribute with the base64-encoded image
    image['src'] = base64_img

# Find module/chapter name (assuming module/chapter start with <p class="title">)
module_name = soup.find_all('p', class_='title')
# Find all titles (assuming lessons start with <h1>)
lesson_headers = soup.find_all('h1')


# Keep track of each lesson's content
lessons = []
current_lesson = []
exclude_exercises = False  # Flag to identify if exercise section is encountered

# Iterate through each element in the body to group content under lessons, exclude the exercises part if exists at the end of a lesson
for element in soup.body.children:
    # Skip the module name (first <p class="title"> element)
    if element in module_name:
        continue

    if element in lesson_headers:
        if current_lesson:  # If there is content in the current lesson, save it
            lessons.append(current_lesson)
        current_lesson = [element]  # Start a new lesson
        exclude_exercises = False  # Reset flag at the start of a new lesson

    else:
        # Check if the element is a <p> tag with text '[EXERCISES]'
        if element.name == 'p' and '[EXERCISES]' in element.get_text(strip=True):
            exclude_exercises = True  # Set flag to exclude exercises
            continue

        # Only add elements if exercises have not started
        if not exclude_exercises:
            current_lesson.append(element)

# Append the last lesson if it exists
if current_lesson:
    lessons.append(current_lesson)


# Get the root of moodle_backup_xml ready
# Copy template to output folder with the correct naming convention
shutil.copy2('{0}moodle_backup_template.xml'.format(TEMPLATE_FOLDER), '{0}\\moodle_backup.xml'.format(OUTPUT_FOLDER))
# Parse the XML template file for moodle backup and load it into an ElementTree object
tree_mbt = ET.parse('{0}moodle_backup.xml'.format(OUTPUT_FOLDER))
# Get the root element of the parsed XML tree
root_mbt = tree_mbt.getroot()


# Create many lesson xml files from templates
# Supposed ids
module_id = 400000
activity_id = 2000
lesson_id = 2000
page_id = 7000
answer_id = 15000
context_id = 1200000
page_id = 7000
answer_id = 15000
grade_id = 90000

for i, lesson in enumerate(lessons):

    title = ""
    contents = ""
    j = 0

    for element in lesson:
        # Assign the first element as the title, concatenate others to contents
        if j == 0:
            title = str(element)  # Title is the first element
        else:
            contents = contents + str(element)
        j = j + 1

        # Clean up the title by removing unwanted attributes and tags
        title = re.sub(r'\s*class="[^"]*"', '', title)  # Remove class attributes
        title = re.sub(r'\s*id="[^"]*"', '', title)  # Remove id attributes
        title = re.sub(r'Lesson \d+: ', '', title)  # Remove "Lesson x:" text
        title = re.sub(r'<[^>]*>', '', title)  # Remove all html tags

        # Clean up the contents by removing unwanted attributes
        contents = re.sub(r'\s*class="[^"]*"', '', contents)
        contents = re.sub(r'\s*id="[^"]*"', '', contents)
        contents = re.sub(r'\s*style="[^"]*"', '', contents)

    # Delcare a new path for outputs
    new_path = "outputs\\for-many-lessons\\lesson_{0}".format(module_id)

     # Check if the specified path exists, create it if it doesn't
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Create lesson.xml #

    # Parse the XML template file for lessons and load it into an ElementTree object
    tree_f = ET.parse('{0}lesson.xml'.format(TEMPLATE_LESSON_FOLDER))

    # Get the root element of the parsed XML tree
    root_f = tree_f.getroot()

    # modify attributes of root element
    root_f.attrib['moduleid'] = str(module_id)
    root_f.attrib['id'] = str(activity_id)
    root_f.attrib['contextid'] = str(context_id)

    # Find all <lesson> elements, which are direct children of current element, and update their id
    for lesson_elem in root_f.findall('lesson'):
        lesson_elem.attrib['id'] = str(lesson_id)

    # Assign unique ID to each <page> element
    for page_elem in root_f.iter('page'):
        page_elem.attrib['id'] = str(page_id)

     # Assign unique ID to each <answer> element
    for answer_elem in root_f.iter('answer'):
        answer_elem.attrib['id'] = str(answer_id)

     # Update the text content of <title> elements with the specified title
    for title_elem in root_f.iter('title'):
        title_elem.text = title

     # Update the text content of <name> elements with the specified title
    for name_elem in root_f.iter('name'):
        name_elem.text = title

     # Update the text content of <answer_text> elements with the specified title
    for answer_text_elem in root_f.iter('answer_text'):
        answer_text_elem.text = title

     # Update the text content of <contents> elements with the specified contents
    for contents_elem in root_f.iter('contents'):
        contents_elem.text = contents

     #  Set the file path and save the XML tree as a new file in the outputs folder
    lesson_file_path = "{0}\lesson.xml".format(new_path)
    # tree_f.write(lesson_file_path)
    write_xml_with_custom_declaration(tree_f, lesson_file_path)



    # Create grades.xml #
    # Parse the grades XML template file and load it into an ElementTree object
    tree_g = ET.parse('{0}grades.xml'.format(TEMPLATE_LESSON_FOLDER))

    # Get the root element of the parsed XML tree
    root_g = tree_g.getroot()

    # Assign unique ID to each <page> element
    for elem in root_g.iter('grade_item'):
        elem.attrib['id'] = str(grade_id)

    # Update the text content of <itemname> tag with the lesson's title
    for elem in root_g.iter('itemname'):
        elem.text = title

    # Set the value of <iteminstance> tag with the lesson's activity tag's id
    for elem in root_g.iter('iteminstance'):
        elem.text = str(activity_id)

    # Set the file path and save the XML tree as a new file in the outputs folder
    grades_file_path = "{0}\grades.xml".format(new_path)
    # tree_g.write(grades_file_path)
    write_xml_with_custom_declaration(tree_g, grades_file_path)

    # Create inforef.xml #
    # Parse the grades XML template file and load it into an ElementTree object
    tree_i = ET.parse('{0}inforef.xml'.format(TEMPLATE_LESSON_FOLDER))

    # Get the root element of the parsed XML tree
    root_i = tree_i.getroot()

    # Update the text content of <id> tag with the grade id
    for elem in root_i.iter('id'):
        elem.text = str(grade_id)

    # Set the file path and save the XML tree as a new file in the outputs folder
    inforef_file_path = "{0}\inforef.xml".format(new_path)
    # tree_i.write(inforef_file_path)
    write_xml_with_custom_declaration(tree_i, inforef_file_path)

    ## Create module.xml ##
    # Parse the grades XML template file and load it into an ElementTree object
    tree_m = ET.parse('{0}module.xml'.format(TEMPLATE_LESSON_FOLDER))

    # Get the root element of the parsed XML tree
    root_m = tree_m.getroot()

    # modify id attribute of root element (<module>)
    root_m.attrib['id'] = str(module_id)

    # Update the text content of <sectionnumber> tag with the desired section number
    for elem in root_m.iter('sectionnumber'):
        elem.text = str(SECTION_NUMBER)

    # Set the file path and save the XML tree as a new file in the outputs folder
    module_file_path = "{0}\module.xml".format(new_path)
    # tree_m.write(module_file_path)
    write_xml_with_custom_declaration(tree_m, module_file_path)


    ## Create moodle_backup_template.xml ##
    # Parse the grades XML template file and load it into an ElementTree object
    tree_mb = ET.parse('{0}moodle_backup_template.xml'.format(TEMPLATE_FOLDER))

    # Get the root element of the parsed XML tree
    root_mb = tree_mb.getroot()

    # Create new activity elements
    new_activity = ET.Element('activity')

    new_activity_moduleid = ET.SubElement(new_activity, 'moduleid')
    new_activity_moduleid.text = str(module_id)

    new_activity_sectionid = ET.SubElement(new_activity, 'sectionid')
    new_activity_sectionid.text = str(41670)

    new_activity_modulename = ET.SubElement(new_activity, 'modulename')
    new_activity_modulename.text = 'lesson'

    new_activity_title = ET.SubElement(new_activity, 'title')
    new_activity_title.text = title

    new_activity_directory = ET.SubElement(new_activity, 'directory')
    new_activity_directory.text = "activities/lesson_{0}".format(module_id)

    # Add activity element to activities element on the moodle_backup xml file
    for elem in root_mbt.iter('activities'):
        elem.append(new_activity)


    # Create the first <setting> element
    new_setting_included = ET.Element('setting')
    ET.SubElement(new_setting_included, 'level').text = 'activity'
    ET.SubElement(new_setting_included, 'activity').text = f'lesson_{module_id}'
    ET.SubElement(new_setting_included, 'name').text = f'lesson_{module_id}_included'
    ET.SubElement(new_setting_included, 'value').text = '1'

    # Add the first setting element to the <settings> element
    for elem in root_mbt.iter('settings'):
        elem.append(new_setting_included)

    # Create the second <setting> element with a different name and value
    new_setting_userinfo = ET.Element('setting')
    ET.SubElement(new_setting_userinfo, 'level').text = 'activity'
    ET.SubElement(new_setting_userinfo, 'activity').text = f'lesson_{module_id}'
    ET.SubElement(new_setting_userinfo, 'name').text = f'lesson_{module_id}_userinfo'
    ET.SubElement(new_setting_userinfo, 'value').text = '0'

    # Add the second setting element to the <settings> element
    for elem in root_mbt.iter('settings'):
        elem.append(new_setting_userinfo)


     # Copy unchanged files to outputs folder
    shutil.copy2('{0}calendar.xml'.format(TEMPLATE_LESSON_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}competencies.xml'.format(TEMPLATE_LESSON_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}filters.xml'.format(TEMPLATE_LESSON_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}grade_history.xml'.format(TEMPLATE_LESSON_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}roles.xml'.format(TEMPLATE_LESSON_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))

     # Increment various ID counters for the next use
    module_id += 1
    activity_id += 1
    lesson_id += 1
    context_id += 1
    page_id += 1
    answer_id += 1
    grade_id += 1

# Write the modified XML back to the output file
write_xml_with_custom_declaration(tree_mbt, f'{OUTPUT_FOLDER}/moodle_backup.xml')
# tree_mbt.write(f'{OUTPUT_FOLDER}/moodle_backup.xml', encoding="UTF-8")



