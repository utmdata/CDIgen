import os
import shutil
#import time
import logging


# Define the directory to save the generated zip files
ZIP_FOLDER = os.path.join(os.getcwd(), 'static', 'tareas')
CSV_FOLDER = os.path.join(os.getcwd(), 'static', 'csv')

#Writte the logs:
logging.basicConfig(filename='zipclear.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def delete_zip_folder_content():
    # Check if the ZIP_FOLDER exists
    if os.path.exists(ZIP_FOLDER):
        # Iterate over all files inside ZIP_FOLDER
        for root, dirs, files in os.walk(ZIP_FOLDER):
            for file in files:
                # Check if the file has a .zip extension
                if file.endswith('.zip' or '.csv'):
                    # Construct the full path to the file
                    file_path = os.path.join(root, file)
                    # Delete the file
                    os.remove(file_path)
                    logging.info(f"Deleted .zip or .csv file: {file_path}")
            # Directories are not deleted since we're only targeting .zip files
    else:
        logging.warning(f"Directory {ZIP_FOLDER} does not exist.")
    
    # Now let's delete only .zip files in CSV_FOLDER
    if os.path.exists(CSV_FOLDER):
        # Iterate over all files inside CSV_FOLDER
        for root, dirs, files in os.walk(CSV_FOLDER):
            for file in files:
                # Check if the file has a .zip extension
                if file.endswith('.zip' or '.csv'):
                    # Construct the full path to the file
                    file_path = os.path.join(root, file)
                    # Delete the file
                    os.remove(file_path)
                    logging.info(f"Deleted .zip or csv file: {file_path}")
            # Directories are not deleted since we're only targeting .zip files
    else:
        logging.warning(f"Directory {CSV_FOLDER} does not exist.")
        
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

