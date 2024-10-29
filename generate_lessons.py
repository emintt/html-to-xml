import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re

# Define the input HTML file and the output folder
input_file_path = 'SDSModule3CreatingSolutions.html'  # The HTML file to be processed

# Load the HTML file
with open(input_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

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
module_id = 400000
activity_id = 2000
lesson_id = 2000
page_id = 7000
answer_id = 15000
context_id = 1200000
page_id = 7000
answer_id = 15000
for i, lesson in enumerate(lessons):

     # Break before the last lesson which is the assignment
    if i == (len(lessons) - 1):
        break

    newpath = "outputs\\for-many-lessons\\lesson_{0}".format(module_id)

    if not os.path.exists(newpath):
        os.makedirs(newpath)
        tree_f = ET.parse('templates\\for-many-lessons\\lesson_441530_template\\lesson.xml')
        root_f = tree_f.getroot()

        root_f.attrib['moduleid'] = str(module_id)
        root_f.attrib['id'] = str(activity_id)
        root_f.attrib['contextid'] = str(context_id)
        for lesson_elem in root_f.findall('lesson'):
            lesson_elem.attrib['id'] = str(lesson_id)
        for page_elem in root_f.iter('page'):
            page_elem.attrib['id'] = str(page_id)
        for answer_elem in root_f.iter('answer'):
            answer_elem.attrib['id'] = str(answer_id)

        file_name = "{0}\lesson.xml".format(newpath)
        tree_f.write(file_name)

    module_id += 1
    activity_id += 1
    lesson_id += 1
    context_id += 1
    page_id += 1
    answer_id += 1


    #activity_elem = root_f.findall('activity')

        #for activity_node in activity_elem:

        #    activity_node.attrib['moduleid'] = str(400000 + i)
            #module_id.set('moduleid', str(400000 + i))  # suppose the first module id will be 400000
#
#     with open('moodle_grades_template.xml', encoding='utf-8') as g:
#         tree_g = ET.parse(g)
#         root_g = tree_g.getroot()
#

#     title = ""
#     contents = ""
#     j = 0
#
#     for element in lesson:
#         if j == 0:
#             title = str(element) # Title is the first element
#         else:
#             contents = contents + str(element)
#         j = j + 1
#
#     title = re.sub(r'\s*class="[^"]*"', '', title) # Remove class attributes
#     title = re.sub(r'\s*id="[^"]*"', '', title) # Remove id attributes
#     title = re.sub(r'Lesson \d+: ', '', title) # Remove "Lesson x:" text
#     title = re.sub(r'<[^>]*>', '', title) # Remove all html tags
#
#     contents = re.sub(r'\s*class="[^"]*"', '', contents)
#     contents = re.sub(r'\s*id="[^"]*"', '', contents)
#     contents = re.sub(r'\s*style="[^"]*"', '', contents)
#
#     # insert content to lesson.xml
#     for elem in root_f.iter():
#         try:
#             elem.text = elem.text.replace('#TITLE#', title)
#             elem.text = elem.text.replace('#CONTENTS#', contents)
#         except AttributeError:
#             pass
#

#
#     # replace title in grades.xml
#     for elem in root_g.iter():
#         try:
#             elem.text = elem.text.replace('#TITLE#', title)
#         except AttributeError:
#             pass
#
#     file_name = "outputs\\lesson_{0}_grades.xml".format(i + 1)
#     with open(file_name, 'w', encoding='utf-8') as output_file:
#         tree_g.write(file_name, encoding='utf-8')
#
# print("Lessons have been saved as xml files")

# # Create lesson xml files from templates
# for i, lesson in enumerate(lessons):
#
#     # Break before the last lesson which is the assignment
#     if i == len(lessons):
#         break
#
#     # Read xml templates
#     with open('moodle_lesson_template.xml', encoding='utf-8') as f:
#         tree_f = ET.parse(f)
#         root_f = tree_f.getroot()
#
#     with open('moodle_grades_template.xml', encoding='utf-8') as g:
#         tree_g = ET.parse(g)
#         root_g = tree_g.getroot()
#
#
#     title = ""
#     contents = ""
#     j = 0
#
#     for element in lesson:
#         if j == 0:
#             title = str(element) # Title is the first element
#         else:
#             contents = contents + str(element)
#         j = j + 1
#
#     title = re.sub(r'\s*class="[^"]*"', '', title) # Remove class attributes
#     title = re.sub(r'\s*id="[^"]*"', '', title) # Remove id attributes
#     title = re.sub(r'Lesson \d+: ', '', title) # Remove "Lesson x:" text
#     title = re.sub(r'<[^>]*>', '', title) # Remove all html tags
#
#     contents = re.sub(r'\s*class="[^"]*"', '', contents)
#     contents = re.sub(r'\s*id="[^"]*"', '', contents)
#     contents = re.sub(r'\s*style="[^"]*"', '', contents)
#
#     # insert content to lesson.xml
#     for elem in root_f.iter():
#         try:
#             elem.text = elem.text.replace('#TITLE#', title)
#             elem.text = elem.text.replace('#CONTENTS#', contents)
#         except AttributeError:
#             pass
#
#     file_name = "outputs\\lesson_{0}.xml".format(i + 1)
#     with open(file_name, 'w', encoding='utf-8') as output_file:
#         tree_f.write(file_name, encoding='utf-8')
#
#     # replace title in grades.xml
#     for elem in root_g.iter():
#         try:
#             elem.text = elem.text.replace('#TITLE#', title)
#         except AttributeError:
#             pass
#
#     file_name = "outputs\\lesson_{0}_grades.xml".format(i + 1)
#     with open(file_name, 'w', encoding='utf-8') as output_file:
#         tree_g.write(file_name, encoding='utf-8')
#
# print("Lessons have been saved as xml files")





