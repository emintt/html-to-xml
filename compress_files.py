# This code duplicates an extracted Moodle backup template folder and organizes the created lesson files, along with
# the modified moodle_backup.xml file, into the correct directories.
# Finally, it compresses the folder into a .mbz file compatible with Moodle.
import json
import os
import shutil
import subprocess
from utils.file_utils import delete_contents_of_folder

with open("config.json", "r") as config_file:
    config = json.load(config_file)

path_to_outputs_folder = config["output_folder"]
path_to_backup_dir_template = os.path.join(config["template_folder"], config["backup_folder_template"])
path_to_temp_folder = os.path.join(config["final_file_folder"], "temp_folder")

# delete temp_folder and old backup compressed file if exists
delete_contents_of_folder(os.path.join(config["final_file_folder"]))

# copy all the content of moodle backup template folder to final_files folder
shutil.copytree(path_to_backup_dir_template, path_to_temp_folder)

# then copy the moodle_backup.xml from the output folder to temp folder
shutil.copy2(os.path.join(path_to_outputs_folder, "moodle_backup.xml"), path_to_temp_folder)

# copy all generated outputs lessons to activities folder of the moodle bu template
# first, delete the activities folder first if it exists
path_to_activities_folder = os.path.join(path_to_temp_folder, "activities")
if os.path.exists(path_to_activities_folder):
    shutil.rmtree(path_to_activities_folder)
# then copy all the contents, delete moodle_backup.xml
shutil.copytree(path_to_outputs_folder, path_to_activities_folder)
os.remove(os.path.join(path_to_activities_folder, "moodle_backup.xml"))


### compress temp_folder to create final file

# Set the name of the compressed .mbz file (without the .tar.gz extension)
output_filename = os.path.join(config["final_file_folder"], "backup_compressed.mbz")


absFilePath = os.path.abspath(__file__)
# Change the working directory to the temp folder
os.chdir(path_to_temp_folder)

# Run the tar command using subprocess
command = ["tar", "-czf", "backup_compressed.mbz", "*"]
try:
    subprocess.run(command, check=True)
    # Move the compressed file to final file
    os.chdir(os.path.dirname(absFilePath))
    shutil.move(os.path.join(path_to_temp_folder, "backup_compressed.mbz"), output_filename)
    print(f"Backup successfully compressed into {output_filename}")
except subprocess.CalledProcessError as e:
    print(f"Error compressing the backup: {e}")








