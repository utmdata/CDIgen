import os
import shutil
import time
import logging

# Define the directory to save the generated zip files
ZIP_FOLDER = os.path.join(os.getcwd(), 'static', 'tareas')

#Writte the logs:
logging.basicConfig(filename='zipclear.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def delete_zip_folder_content():
    """
    Deletes all files and directories inside the ZIP_FOLDER directory.
    """
    # Check if the ZIP_FOLDER exists
    if os.path.exists(ZIP_FOLDER):
        # Iterate over all files and directories inside ZIP_FOLDER
        for root, dirs, files in os.walk(ZIP_FOLDER):
            for file in files:
                # Construct the full path to each file
                file_path = os.path.join(root, file)
                # Delete the file
                os.remove(file_path)
                logging.info(f"Deleted file: {file_path}")
            for dir in dirs:
                # Construct the full path to each directory
                dir_path = os.path.join(root, dir)
                # Delete the directory
                shutil.rmtree(dir_path)
                logging.info(f"Deleted directory: {dir_path}")
    else:
        logging.warning(f"Directory {ZIP_FOLDER} does not exist.")

def weekly_maintenance():
    """
    Performs weekly maintenance tasks.
    """
    logging.info("Starting weekly maintenance...")
    delete_zip_folder_content()
    logging.info("Weekly maintenance completed.")

# Schedule the weekly maintenance to run every Sunday at midnight
#schedule.every().tuesday.at("11:52").do(weekly_maintenance)
weekly_maintenance()

