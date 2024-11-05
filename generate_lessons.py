import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import shutil
import base64

# Function to convert an image URL to a Base64-encoded string
def image_url_to_base64(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read())

    return ""


# Define the input HTML file and the output folder
INPUT_FOLDER = "html-source\\SDSModule3-CreatingSolutions\\"
INPUT_FILE_PATH = "{0}SDSModule3CreatingSolutions.html".format(INPUT_FOLDER)  # The HTML file to be processed

# Define the output folder
OUTPUT_FOLDER = "outputs\\for-many-lessons\\"

# Define the template folder
TEMPLATE_FOLDER = "templates\\for-many-lessons\\lesson_441530_template\\"

# Load the HTML file
with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all img element and replace src attribute with the base64-encoded image
images = soup.findAll('img')
print(images[0])
for image in images:
    # Construct image file path to create a local path on Windows
    img_file = "{0}{1}".format(INPUT_FOLDER, image['src'].replace("/","\\"))
    # Convert the image to base 64
    base64_img = "data:image/jpg;base64,{0}".format(image_url_to_base64(img_file))
    # Update src attribute with the base64-encoded image
    image['src'] = base64_img

# Find all lesson headers (assuming lessons start with <p class="title">)
lesson_headers = soup.find_all('p', class_='title')

# Keep track of each lesson's content
lessons = []
current_lesson = []

# Iterate through each element in the body to group content under lessons
for element in soup.body.children:
    if element in lesson_headers:
        if current_lesson:  # If there is content in the current lesson, save it
            lessons.append(current_lesson)
        current_lesson = [element]  # Start a new lesson
    else:
        current_lesson.append(element)

# Append the last lesson if it exists
if current_lesson:
    lessons.append(current_lesson)

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

     # Break before the last lesson which is the assignment
    if i == (len(lessons) - 1):
        break

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
    tree_f = ET.parse('{0}lesson.xml'.format(TEMPLATE_FOLDER))

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

     # Define the file path and write the XML tree to a new file
    file_name = "{0}\lesson.xml".format(new_path)
    tree_f.write(file_name)



    # Create grades.xml #
    # Parse the grades XML template file and load it into an ElementTree object
    tree_g = ET.parse('{0}grades.xml'.format(TEMPLATE_FOLDER))

    # Get the root element of the parsed XML tree
    root_g = tree_g.getroot()

    # Assign unique ID to each <page> element
    for page_elem in root_g.iter('grade_item'):
        page_elem.attrib['id'] = str(grade_id)

    # Update the text content of <itemname> tag with the lesson's title
    for contents_elem in root_f.iter('itemname'):
        contents_elem.text = title

    # Set the value of <iteminstance> tag with the lesson's activity tag's id
    for contents_elem in root_f.iter('iteminstance'):
        contents_elem.text = activity_id

    # Create inforef.xml #

     # Copy unchanged files to outputs folder
    shutil.copy2('{0}calendar.xml'.format(TEMPLATE_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}competencies.xml'.format(TEMPLATE_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}filters.xml'.format(TEMPLATE_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}grade_history.xml'.format(TEMPLATE_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))
    shutil.copy2('{0}roles.xml'.format(TEMPLATE_FOLDER), '{0}\\lesson_{1}'.format(OUTPUT_FOLDER, module_id))

     # Increment various ID counters for the next use
    module_id += 1
    activity_id += 1
    lesson_id += 1
    context_id += 1
    page_id += 1
    answer_id += 1
    grade_id += 1









