import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='csrcodelist.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch and save the CSR code list XML file
def fetch_and_save_csr_code_list():
    url = "https://csr.seadatanet.org/isoCodelists/csrCodeList.xml"
    static_folder = "static"
    file_name = "csrCodeList.xml"
    file_path = os.path.join(static_folder, file_name)
    logging.info("Script of csrcodelist started.")

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Check if the file already exists
            if os.path.exists(file_path):
                os.remove(file_path)  # Remove the old file

            with open(file_path, "wb") as file:
                file.write(response.content)
                logging.info(f"CSR code list XML file saved successfully at {datetime.now()}.")
                print("CSR code list XML file saved successfully.")
        else:
            logging.error(f"Failed to fetch CSR code list XML file. Status code: {response.status_code}")
            print(f"Failed to fetch CSR code list XML file. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

fetch_and_save_csr_code_list()
