import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='csrcodelist.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch and save the CSR code list XML file
def fetch_and_save_csr_code_list():
    url = "http://csr.seadatanet.org/isoCodelists/csrCodeList.xml"
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

def fetch_and_save_sparql_results():
    base_url = "http://edmo.seadatanet.org/sparql/sparql"
    query = """
        SELECT ?org ?name ?altName (CONCAT(?name, " (", ?altName, ")") AS ?orgName) ?notation ?street
        WHERE {
            ?org a <http://www.w3.org/ns/org#Organization> ;
                 <http://www.w3.org/ns/org#name> ?name ;
                 <http://www.w3.org/2004/02/skos/core#notation> ?notation ;
                 <http://www.w3.org/2006/vcard/ns#street-address> ?street ;
                 <http://www.w3.org/2004/02/skos/core#altName> ?altName.
        }
    """
    # Encode the query for use in the URL
    encoded_query = requests.utils.quote(query)
    full_url = f"{base_url}?query={encoded_query}&accept=application/json"

    static_folder = "static"
    file_name = "sparql.json"
    file_path = os.path.join(static_folder, file_name)
    logging.info("Script to fetch SPARQL results started.")

    try:
        # Send the GET request
        response = requests.get(full_url)
        if response.status_code == 200:
            # Check if the file already exists
            if os.path.exists(file_path):
                os.remove(file_path)  # Remove the old file

            # Save the response content as a JSON file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
                logging.info(f"SPARQL results saved successfully at {datetime.now()}.")
                print("SPARQL results saved successfully.")
        else:
            logging.error(f"Failed to fetch SPARQL results. Status code: {response.status_code}")
            print(f"Failed to fetch SPARQL results. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

# Call the function
#fetch_and_save_sparql_results()

#fetch_and_save_csr_code_list()
