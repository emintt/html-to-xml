- generate_lessons.py script is designed to automate the generation of Moodle-compatible XML files for course lessons. This script takes HTML-based lesson content, transforms it into a structured set of XML files, and organizes them into a folder hierarchy. These XML files are ready for direct inclusion in Moodle’s backup format (.mbz) for easy import into a Moodle course.

## Repository structure
- generate_lessons.py: The main script file for generating XML files from HTML lessons.
- html-source/: Contains source HTML files and images for each lesson. Each lesson is contained within its own subfolder.
- outputs/for-many-lessons/: The directory where the generated lesson folders and XML files are stored.
- templates/for-many-lessons/lesson_441530_template/: Stores XML templates used as the basis for each generated lesson.

## Feature
- HTML to XML Conversion: Parses HTML content, extracting lesson titles and content, then converts these into XML elements.
- Image Base64 Encoding: Encodes images as Base64 strings and embeds them directly into XML.
- Template-Based XML Generation: Utilizes pre-existing XML templates to standardize each generated XML file.
- Moodle Backup Preparation: Creates a moodle_backup.xml file which includes metadata for each lesson, allowing for smooth Moodle course import.

## Usage
1. Prepare Input Data: Place your lesson HTML files and associated images in the html-source/ folder. Each lesson should be in its own subfolder within html-source/.
2. Run the Script: python generate_lessons.py
    This will:

    - Parse each HTML file in the html-source/ directory.
    - Convert images to Base64 and embed them within the XML structure.
    - Generate a folder for each lesson in outputs/for-many-lessons/ containing lesson.xml, grades.xml, inforef.xml, and module.xml.
    - Create a moodle_backup.xml file for the full backup structure.
3. Import to Moodle:
- TODO

## Configuration
