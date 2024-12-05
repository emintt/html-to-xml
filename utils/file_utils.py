# Copy a file to a destination directory
import os
import shutil


def copy_file_to_directory(source_folder: str, source_file_name: str, parent_dir: str,  destination_dir_name: str) -> None:
    # construct the source file path
    source_file = os.path.join(source_folder, source_file_name)
    # construct the destination directory path
    destination_dir = os.path.join(parent_dir, destination_dir_name)

    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"Source file does not exist: {source_file}")

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the file to the destination directory
    shutil.copy2(source_file, destination_dir)

# delete contents of a folder
def delete_contents_of_folder(folder) -> None:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Example usage:
# LESSON_FOLDER_TEMPLATE = "/path/to/lesson/templates"
# INPUT_FOLDER = "/path/to/input/folder"
# module_id = 1
#
# source = os.path.join(LESSON_FOLDER_TEMPLATE, "calendar.xml")
# destination = os.path.join(INPUT_FOLDER, f"lesson_{module_id}")
#
# copy_file_to_directory(source, destination)