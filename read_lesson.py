import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re

# Define the input HTML file and the output folder
input_file_path = 'SDSModule1Foundations.html'  # The HTML file to be processed

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
    ####################
    with open('lesson-template.xml', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

    title = ""
    contents = ""
    j = 0
    ####################

    for element in lesson:
        #lesson_soup.body.append(element)
        if j == 0:
            title = str(element)
        else:
            contents = contents + str(element)

        j = j + 1

    title = re.sub(r'\s*class="[^"]*"', '', title)
    title = re.sub(r'\s*id="[^"]*"', '', title)
    title = re.sub(r'Lesson \d+: ', '', title)

    contents = re.sub(r'\s*class="[^"]*"', '', contents)
    contents = re.sub(r'\s*id="[^"]*"', '', contents)

    for elem in root.iter():
        try:

            elem.text = elem.text.replace('#TITLE#', title)
            elem.text = elem.text.replace('#CONTENTS#', contents)
        except AttributeError:
            pass
    tree.write('C:\\Users\\elmin\\Documents\\Metropolia\\S-24-MoodleProjekti\\Test\\html-to-xml\\output.xml',
               encoding='utf-8')
    break
    """
    # Create a new soup object to replicate the structure of the original file
    lesson_soup = BeautifulSoup(str(soup), 'html.parser')

    # Clear the body content from the replicated structure
    lesson_soup.body.clear()

    # Add the lesson content to the new body's structure
    for element in lesson:
        lesson_soup.body.append(element)

    # Determine the lesson title or a fallback filename
    lesson_title = lesson[0].get_text().strip().replace(' ', '_').replace(':', '').replace('/', '')[
                   :50]  # Generate a safe file name
    file_name = f'{lesson_title}_lesson_{i + 1}.html'

    # Write the lesson HTML to a file in the current directory
    with open(file_name, 'w', encoding='utf-8') as output_file:
        output_file.write(str(lesson_soup.prettify()))  # Prettify ensures proper HTML formatting
    """
print("Lessons have been saved to the current directory with the original structure.")

