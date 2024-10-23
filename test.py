import xml.etree.ElementTree as ET

with open('moodle_lesson_template.xml', encoding='utf-8') as f:
  tree = ET.parse(f)
  root = tree.getroot()

  for elem in root.iter():
    try:
      elem.text = elem.text.replace('#TITLE#', 'LIEM')
    except AttributeError:
      pass

tree.write('C:\\Users\\elmin\\Documents\\Metropolia\\S-24-MoodleProjekti\\Test\\html-to-xml\\output.xml', encoding='utf-8')
print("END")