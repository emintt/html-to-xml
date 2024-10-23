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

# Save each lesson into separate HTML files in the same directory
for i, lesson in enumerate(lessons):

    # Break before the last lesson which is the assignment
    if i == len(lessons):
        break

    # Read xml template
    with open('moodle_lesson_template.xml', encoding='utf-8') as f:
        tree_f = ET.parse(f)
        root_f = tree_f.getroot()

    with open('moodle_grades_template.xml', encoding='utf-8') as g:
        tree_g = ET.parse(g)
        root_g = tree_g.getroot()


    title = ""
    contents = ""
    j = 0

    for element in lesson:
        if j == 0:
            title = str(element) # Title is the first element
        else:
            contents = contents + str(element)
        j = j + 1

    title = re.sub(r'\s*class="[^"]*"', '', title) # Remove class attributes
    title = re.sub(r'\s*id="[^"]*"', '', title) # Remove id attributes
    title = re.sub(r'Lesson \d+: ', '', title) # Remove "Lesson x:" text
    title = re.sub(r'<[^>]*>', '', title) # Remove all html tags

    contents = re.sub(r'\s*class="[^"]*"', '', contents)
    contents = re.sub(r'\s*id="[^"]*"', '', contents)
    contents = re.sub(r'\s*style="[^"]*"', '', contents)

    # insert content to lesson.xml
    for elem in root_f.iter():
        try:
            elem.text = elem.text.replace('#TITLE#', title)
            elem.text = elem.text.replace('#CONTENTS#', contents)
        except AttributeError:
            pass

    file_name = "outputs\\lesson_{0}.xml".format(i + 1)
    with open(file_name, 'w', encoding='utf-8') as output_file:
        tree_f.write(file_name, encoding='utf-8')

    # replace title in grades.xml
    for elem in root_g.iter():
        try:
            elem.text = elem.text.replace('#TITLE#', title)
        except AttributeError:
            pass

    file_name = "outputs\\lesson_{0}_grades.xml".format(i + 1)
    with open(file_name, 'w', encoding='utf-8') as output_file:
        tree_g.write(file_name, encoding='utf-8')

print("Lessons have been saved as xml files")

