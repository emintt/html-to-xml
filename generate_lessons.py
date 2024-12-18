# This script processes a DOCX file containing multiple lessons.
# Any questions, if present, are located AT THE END OF EACH LESSON.
# This script focuses only on creating the content of the lessons and excludes the questions section.

import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import shutil
import os
import json
from utils.image_utils import image_url_to_base64
from utils.xml_utils import write_xml_with_custom_declaration, update_elements_text, update_xml_attributes
from utils.file_utils import copy_file_to_directory
from utils.file_utils import delete_contents_of_folder

def generate_lesson_folders():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Define the HTML source file and the output folder
    INPUT_FOLDER = os.path.normpath(config["input_folder"])
    HTML_FILE_PATH = os.path.join(INPUT_FOLDER, config["input_file_name"])  # The HTML file to be processed
    HTML_FILE_PATH = os.path.normpath(HTML_FILE_PATH)

    # Define the output folder
    OUTPUT_FOLDER = os.path.normpath(config["output_folder"])


    TEMPLATE_FOLDER = os.path.normpath(config["template_folder"])
    LESSON_FOLDER_TEMPLATE = os.path.normpath(f"{TEMPLATE_FOLDER}/{config['lesson_folder_template']}")
    BACKUP_FILE_TEMPLATE = os.path.normpath(f"{TEMPLATE_FOLDER}/{config['backup_file_template']}")
    # Define section number
    SECTION_NUMBER = config["section_number"]

    # Delete the old contents of outputs folder if exists
    delete_contents_of_folder(OUTPUT_FOLDER)

    # Load the HTML file
    with open(HTML_FILE_PATH, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all img element and replace src attribute with the base64-encoded image
    images = soup.findAll('img')
    for image in images:
        # Construct image file path to create a local path on Windows
        img_file = f"{INPUT_FOLDER}/{image['src']}"
        print(img_file)
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

    # Adjust header tags (h1, h2 is preseverd in moodle)
    for lesson in lessons:
        for i, element in enumerate(lesson):
            if element.name in ['h2', 'h3', 'h4', 'h5']:
                new_tag = 'h' + str(int(element.name[1]) + 1)  # Increment header level (e.g., h2 -> h3)
                element.name = new_tag  # Replace with new header tag
            if element.name in ['h6']:
                new_tag = 'p'
                element.name = new_tag  # Replace with new header tag


    # Get the root of moodle_backup_xml ready
    # Copy template to output folder with the correct naming convention
    shutil.copy2(f"{BACKUP_FILE_TEMPLATE}", f"{os.path.join(OUTPUT_FOLDER, 'moodle_backup.xml')}")

    # Construct the path to the copied file
    backup_file_path = os.path.join(OUTPUT_FOLDER, "moodle_backup.xml")

    # Parse the XML template file for moodle backup and load it into an ElementTree object
    tree_mbt = ET.parse(backup_file_path)

    # Get the root element of the parsed XML tree
    root_mbt = tree_mbt.getroot()


    # Create many lesson xml files from templates
    # Supposed ids
    module_id = int(config["default_ids"]["module_id"])
    activity_id = int(config["default_ids"]["activity_id"])
    lesson_id = int(config["default_ids"]["lesson_id"])
    page_id = int(config["default_ids"]["page_id"])
    answer_id = int(config["default_ids"]["answer_id"])
    context_id = int(config["default_ids"]["context_id"])
    page_id = int(config["default_ids"]["page_id"])
    answer_id = int(config["default_ids"]["answer_id"])
    grade_id = int(config["default_ids"]["grade_id"])

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
            # title = re.sub(r'Lesson \d+: ', '', title)  # Remove "Lesson x:" text
            title = re.sub(r'<[^>]*>', '', title)  # Remove all html tags

            # Clean up the contents by removing unwanted attributes
            contents = re.sub(r'\s*class="[^"]*"', '', contents)
            contents = re.sub(r'\s*id="[^"]*"', '', contents)
            contents = re.sub(r'\s*style="[^"]*"', '', contents)



        # Delcare a new path for outputs
        new_path = os.path.join(OUTPUT_FOLDER, f"lesson_{module_id}")


         # Check if the specified path exists, create it if it doesn't
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        # Create lesson.xml #

        # Parse the XML template file for lessons and load it into an ElementTree object
        tree_f = ET.parse(os.path.join(LESSON_FOLDER_TEMPLATE, "lesson.xml"))

        # Get the root element of the parsed XML tree
        root_f = tree_f.getroot()

        # modify attributes of root element
        root_f.attrib['moduleid'] = str(module_id)
        root_f.attrib['id'] = str(activity_id)
        root_f.attrib['contextid'] = str(context_id)

        # Find all <lesson> elements, which are direct children of current element, and update their id
        for lesson_elem in root_f.findall('lesson'):
            lesson_elem.attrib['id'] = str(lesson_id)

        # Assign unique ID to each <page> , <answaer>, ... element
        lesson_attributtes = {
            'page': {'id': page_id},
            'answer': {'id': answer_id}
        }
        update_xml_attributes(root_f,lesson_attributtes)

        # # Assign unique ID to each <page> element
        # for page_elem in root_f.iter('page'):
        #     page_elem.attrib['id'] = str(page_id)
        #
        #  # Assign unique ID to each <answer> element
        # for answer_elem in root_f.iter('answer'):
        #     answer_elem.attrib['id'] = str(answer_id)

        # Update the text content of elements with the specified data
        update_elements_text(root_f, {
            'title': title,
            'name': title,
            'answer_text': title,
            'contents': contents
        })

        #  # Update the text content of <title> elements with the specified title
        # for title_elem in root_f.iter('title'):
        #     title_elem.text = title
        #
        #  # Update the text content of <name> elements with the specified title
        # for name_elem in root_f.iter('name'):
        #     name_elem.text = title
        #
        #  # Update the text content of <answer_text> elements with the specified title
        # for answer_text_elem in root_f.iter('answer_text'):
        #     answer_text_elem.text = title
        #
        #  # Update the text content of <contents> elements with the specified contents
        # for contents_elem in root_f.iter('contents'):
        #     contents_elem.text = contents

         #  Set the file path and save the XML tree as a new file in the outputs folder
        lesson_file_path = "{0}\lesson.xml".format(new_path)
        write_xml_with_custom_declaration(tree_f, lesson_file_path)



        # Create grades.xml #
        # Parse the grades XML template file and load it into an ElementTree object
        tree_g = ET.parse(os.path.join(LESSON_FOLDER_TEMPLATE, "grades.xml"))


        # Get the root element of the parsed XML tree
        root_g = tree_g.getroot()

        # Assign unique ID to each <page> element
        for elem in root_g.iter('grade_item'):
            elem.attrib['id'] = str(grade_id)

        # Update the text content of <itemname>, <iteminstance> tag with the lesson's title and id
        update_elements_text(root_g, {
            'itemname': title,
            'iteminstance': str(activity_id)
        })
        # for elem in root_g.iter('itemname'):
        #     elem.text = title
        #
        # # Set the value of <iteminstance> tag with the lesson's activity tag's id
        # for elem in root_g.iter('iteminstance'):
        #     elem.text = str(activity_id)

        # Set the file path and save the XML tree as a new file in the outputs folder
        grades_file_path = "{0}\grades.xml".format(new_path)
        # tree_g.write(grades_file_path)
        write_xml_with_custom_declaration(tree_g, grades_file_path)

        # Create inforef.xml #
        # Parse the grades XML template file and load it into an ElementTree object
        tree_i = ET.parse(os.path.join(LESSON_FOLDER_TEMPLATE, "inforef.xml"))


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
        tree_m = ET.parse(os.path.join(LESSON_FOLDER_TEMPLATE, "module.xml"))

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
        tree_mb = ET.parse(os.path.join(TEMPLATE_FOLDER, "moodle_backup_template.xml"))

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
        copy_file_to_directory(LESSON_FOLDER_TEMPLATE, "calendar.xml", OUTPUT_FOLDER, f"lesson_{module_id}")
        copy_file_to_directory(LESSON_FOLDER_TEMPLATE, "competencies.xml", OUTPUT_FOLDER, f"lesson_{module_id}")
        copy_file_to_directory(LESSON_FOLDER_TEMPLATE, "filters.xml", OUTPUT_FOLDER, f"lesson_{module_id}")
        copy_file_to_directory(LESSON_FOLDER_TEMPLATE, "grade_history.xml", OUTPUT_FOLDER, f"lesson_{module_id}")
        copy_file_to_directory(LESSON_FOLDER_TEMPLATE, "roles.xml", OUTPUT_FOLDER, f"lesson_{module_id}")

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



