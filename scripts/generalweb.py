<<<<<<< HEAD
import pandas as pd
import glob
from datetime import datetime
import numpy as np
import shutil
import os,sys
from os import remove
from os import path
from datetime import datetime
import requests, argparse
from lxml import etree
import copy
import logging, json
import csv
#importem els scripts de cada cdi

def crear_carpeta(nombre_carpeta):
    try:
        os.mkdir(nombre_carpeta)
        logging.info(f"Created folder '{nombre_carpeta}'")
    except FileExistsError:
        logging.info(f"Folder '{nombre_carpeta}' already exists")
    except Exception as e:
        logging.error(f"Error creating folder '{nombre_carpeta}': {str(e)}")
        raise

def process_xml_file(input_file, output_file, namespace, updates):
    try:
        tree = etree.parse(input_file)
        for xpath, value in updates:
            try:
                posList = tree.xpath(xpath, namespaces=namespace)[0]
                if isinstance(value, tuple):
                    posList.text = value[0]
                    posList.set("codeListValue", value[1])
                else: 
                    posList.text = value
            except IndexError as e:
                logging.error(f"Error finding element with xpath {xpath}: {str(e)}")
                raise
            except Exception as e:
                logging.error(f"Error updating element with xpath {xpath}: {str(e)}")
                raise
        tree.write(output_file)
        logging.info(f"Successfully updated XML file: {output_file}")
    except Exception as e:
        logging.error(f"Error processing XML file: {str(e)}")
        raise

def get_country_code_by_label(label):
            with open("static/c32_countries.csv", encoding="latin1") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["preflabel"].strip().lower() == label.strip().lower():
                        return row["conceptid"]
            return "99"  # Código por defecto


def compose_org_name(name, alt_name):
    name = (name or "").strip()
    alt_name = (alt_name or "").strip()

    has_name = name not in ("", "N/A")
    has_alt_name = alt_name not in ("", "N/A")

    if has_name and has_alt_name and alt_name != name:
        return f"{name} ({alt_name})"
    if has_name:
        return name
    if has_alt_name:
        return alt_name
    return "N/A"

def get_organization_info(valor_org):
    try:
        # Load metadata from JSON file
        json_path = os.path.join("static", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Find the organization data using the `valor_org` URI
        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract the required fields
        org_info = {
            'org': matched.get("org", {}).get("value", "N/A"),
            'org_name': matched.get("orgName", {}).get("value", "N/A"),
            'notation': matched.get("notation", {}).get("value", "N/A"),
            'street': matched.get("street", {}).get("value", "N/A"),
            'country': matched.get("country", {}).get("value", "N/A")
        }
        
        logging.info(f"Organization Info: {org_info}")
        return org_info
    except Exception as e:
        logging.error(f"Error getting organization info from JSON: {str(e)}")
        raise

def get_organization_email(valor_org):
    try:
        # Load metadata from JSON file
        json_path = os.path.join("static", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Find the organization data using the `valor_org` URI
        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            logging.info("No email found, using default email")
            return "sdn-userdesk@seadatanet.org"

        email = matched.get("email", {}).get("value", "N/A")
        return email.replace("mailto:", "").replace("%40", "@")
    except Exception as e:
        logging.error(f"Error getting organization email from JSON: {str(e)}")
        raise

def general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final): #copia sense_sensor
        # Handle CSR code
        print(csr_code)
        if csr_code != "UNKNOWN":
            xml_url = "http://datahub.utm.csic.es/cdigen/static/csrCodeList.xml"
            response = requests.get(xml_url, verify=False)
            if response.status_code != 200:
                raise Exception(f"Failed to download CSR code list: {response.status_code}")
            root = etree.fromstring(response.content)
            for cruisename in root.findall(".//{http://www.opengis.net/gml}cruisename"):
                if cruisename.text == csr_code:
                    description_csr = cruisename.getparent().find("{http://www.opengis.net/gml}description").text
                    id_csr = cruisename.getparent().find("{http://www.opengis.net/gml}identifier").text
                    break
            else:
                raise Exception(f"CSR code {csr_code} not found in the XML file.")
        else:
            id_csr = '2004 - Unknown(ZZ99)'
            description_csr = "20050002"

        print(f"CSR ID: {id_csr}")
        print(f"CSR Description: {description_csr}")

        # Load metadata from JSON
        json_path = os.path.join("static", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract metadata
        org = matched.get("org", {}).get("value", "N/A")
        org_name = matched.get("orgName", {}).get("value", "N/A")
        notation = matched.get("notation", {}).get("value", "N/A")
        tel = matched.get("tel", {}).get("value", "N/A")
        alt_name = matched.get("altName", {}).get("value", "N/A")
        street = matched.get("street", {}).get("value", "N/A")
        codepostal = matched.get("codepostal", {}).get("value", "N/A")
        locality = matched.get("locality", {}).get("value", "N/A")
        country = matched.get("country", {}).get("value", "N/A")
        web = matched.get("web", {}).get("value", "N/A")
        email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")

        name = matched.get("name", {}).get("value", "N/A")
        print(f"DEBUG: Extracted org_name from JSON: '{org_name}'")
        print(f"DEBUG: Extracted alt_name from JSON: '{alt_name}'")
        print(f"DEBUG: Extracted name from JSON: '{name}'")

        org_name = compose_org_name(name, alt_name)
        if org_name == "N/A":
            print("WARNING: Organization name from JSON is N/A and no alternative name available!")
        else:
            print(f"INFO: Composed organization name: '{org_name}'")

        print(f"Organization URI: {org}")
        print(f"Organization Name: {org_name}")
        print(f"Notation: {notation}")
        print(f"Telephone: {tel}")
        print(f"Alternative Name: {alt_name}")
        print(f"Street: {street}")
        print(f"Postal Code: {codepostal}")
        print(f"Locality: {locality}")
        print(f"Country: {country}")
        print(f"Web: {web}")
        print(f"Email: {email}")


        # Asignar información del buque
        if vessel_input == "sdg":
            vessel = "Sarmiento de Gamboa"
            vessel_mode = "Sarmiento"
            vessel_reduit = "sdg"
        elif vessel_input == "hes":
            vessel = "Hespérides"
            vessel_mode = "Hesperides"
            vessel_reduit = "hes"
        elif vessel_input == "odb":
            vessel = "Odón de Buen"
            vessel_mode = "Odón"
            vessel_reduit = "odb"
            vessel_code = "29OD"
        elif vessel_input == "gdc":
            vessel = "García del Cid"
            vessel_mode = "García"
            vessel_reduit = "gdc"
            vessel_code = "29GD"           
        else:
            raise ValueError(f"Invalid vessel_input: {vessel_input}")

        # Extraer fecha
        dia = cruise_id[10:12]
        mes = cruise_id[8:10]
        any = cruise_id[4:8]
        short_date = f"{any}-{mes}-{dia}"

        # Crear carpeta y preparar archivo CDI individual
        cdi_individual = f"{cruise_id}_cdi.xml"
        nombre_carpeta = cruise_id
        crear_carpeta(nombre_carpeta)

        # Copiar plantilla XML
        if path.exists("model_cdi_sensegml.txt"):
            remove("model_cdi_sensegml.txt")
        shutil.copy("model_cdi_sensegml.xml", cdi_individual)
        logging.info(f"Created CDI file: {cdi_individual}")

        #Posem la url perque trobi el gml i l'enganxi en el xml
        input_file = cdi_individual
        input_url = 'http://datahub.utm.csic.es/ws/getTrack/GML/?id=' + vessel_input + cruise_id[4:12] + '&n=999'
        output_file = cdi_individual

        # Definir namespaces
        namespace = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gml': 'http://www.opengis.net/gml',
            'gco': 'http://www.isotc211.org/2005/gco',
            'sdn': 'http://www.seadatanet.org',
            'gmx': 'http://www.isotc211.org/2005/gmx'
        }

        # GML y BBOX
        #gml_result, bbox = extract_gml_and_bbox(ruta_csv)
        #logging.info(f"GML result: {gml_result}")
        #logging.info(f"BBOX: {bbox}")

        # Reemplazos en el XML
        deperature_country_code = get_country_code_by_label(country)
        # Parse the XML and update the fields
        tree = etree.parse(input_file)

        #afegim short id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
        posList.text = cruise_id
        tree.write(output_file)

        #afegim csr id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'CSR_CRUISE_NAME')]", namespaces=namespace)[0]
        posList.text = cruise_name
        tree.write(output_file)

        #afegim short date
        data = any + "-" + mes + "-" + dia
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:Date[contains(text(), '2023-05-04')]", namespaces=namespace)[0]
        posList.text = data
        tree.write(output_file)

        #afegim org_name
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
            if posList:
                posList[0].text = org_name
                posList[0].set("codeListValue", notation)
                tree.write(output_file)
                print("✓ Updated organization name (1st occurrence)")
            else:
                print("⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found")
        except Exception as e:
            print(f"✗ ERROR updating org_name (1st): {str(e)}")

        #afegim org_name per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
            if posList:
                posList[0].text = org_name
                posList[0].set("codeListValue", notation)
                tree.write(output_file)
                print("✓ Updated organization name (2nd occurrence)")
            else:
                print("⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating org_name (2nd): {str(e)}")

        #afegim street
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
            if posList:
                posList[0].text = street
                tree.write(output_file)
                print("✓ Updated street (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_street' text found")
        except Exception as e:
            print(f"✗ ERROR updating street (1st): {str(e)}")

        #afegim street per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
            if posList:
                posList[0].text = street
                tree.write(output_file)
                print("✓ Updated street (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_street' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating street (2nd): {str(e)}")

        #afegim city
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
            if posList:
                posList[0].text = locality
                tree.write(output_file)
                print("✓ Updated city (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_city' text found")
        except Exception as e:
            print(f"✗ ERROR updating city (1st): {str(e)}")

        #afegim city per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
            if posList:
                posList[0].text = locality
                tree.write(output_file)
                print("✓ Updated city (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_city' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating city (2nd): {str(e)}")

        #afegim country
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CountryCode[contains(text(), 'org_country')]", namespaces=namespace)
            if posList:
                posList[0].text = country
                posList[0].set("codeListValue", deperature_country_code)
                tree.write(output_file)
                print("✓ Updated country (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_country' text found")
        except Exception as e:
            print(f"✗ ERROR updating country (1st): {str(e)}")

        #afegim country per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CountryCode[contains(text(), 'org_country')]", namespaces=namespace)
            if posList:
                posList[0].text = country
                posList[0].set("codeListValue", deperature_country_code)
                tree.write(output_file)
                print("✓ Updated country (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_country' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating country (2nd): {str(e)}")

        #afegim email
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
            if posList:
                posList[0].text = email
                tree.write(output_file)
                print("✓ Updated email (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_mail' text found")
        except Exception as e:
            print(f"✗ ERROR updating email (1st): {str(e)}")

        #afegim email per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
            if posList:
                posList[0].text = email
                tree.write(output_file)
                print("✓ Updated email (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_mail' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating email (2nd): {str(e)}")

        #afegim csrcodelist
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)
            if posList:
                posList[0].text = description_csr
                posList[0].set("codeListValue", id_csr)
                tree.write(output_file)
                print("✓ Updated CSR code")
            else:
                print("⚠ WARNING: No CSR code element found")
        except Exception as e:
            print(f"✗ ERROR updating CSR code: {str(e)}")
        print("fet generalweb----------------") 


def general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final):
        # Handle CSR code
        print(csr_code)
        if csr_code != "UNKNOWN":
            xml_url = "http://datahub.utm.csic.es/cdigen/static/csrCodeList.xml"
            response = requests.get(xml_url, verify=False)
            if response.status_code != 200:
                raise Exception(f"Failed to download CSR code list: {response.status_code}")
            root = etree.fromstring(response.content)
            for cruisename in root.findall(".//{http://www.opengis.net/gml}cruisename"):
                if cruisename.text == csr_code:
                    description_csr = cruisename.getparent().find("{http://www.opengis.net/gml}description").text
                    id_csr = cruisename.getparent().find("{http://www.opengis.net/gml}identifier").text
                    break
            else:
                raise Exception(f"CSR code {csr_code} not found in the XML file.")
        else:
            id_csr = '2004 - Unknown(ZZ99)'
            description_csr = "20050002"

        print(f"CSR ID: {id_csr}")
        print(f"CSR Description: {description_csr}")

        # Load metadata from JSON
        json_path = os.path.join("static", "sparql.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        results = data.get("results", {}).get("bindings", [])
        matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

        if not matched:
            raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

        # Extract metadata
        org = matched.get("org", {}).get("value", "N/A")
        org_name = matched.get("orgName", {}).get("value", "N/A")
        notation = matched.get("notation", {}).get("value", "N/A")
        tel = matched.get("tel", {}).get("value", "N/A")
        alt_name = matched.get("altName", {}).get("value", "N/A")
        street = matched.get("street", {}).get("value", "N/A")
        codepostal = matched.get("codepostal", {}).get("value", "N/A")
        locality = matched.get("locality", {}).get("value", "N/A")
        country = matched.get("country", {}).get("value", "N/A")
        web = matched.get("web", {}).get("value", "N/A")
        email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")

        name = matched.get("name", {}).get("value", "N/A")
        print(f"DEBUG: Extracted org_name from JSON: '{org_name}'")
        print(f"DEBUG: Extracted alt_name from JSON: '{alt_name}'")
        print(f"DEBUG: Extracted name from JSON: '{name}'")

        org_name = compose_org_name(name, alt_name)
        if org_name == "N/A":
            print("WARNING: Organization name from JSON is N/A and no alternative name available!")
        else:
            print(f"INFO: Composed organization name: '{org_name}'")

        print(f"Organization URI: {org}")
        print(f"Organization Name: {org_name}")
        print(f"Notation: {notation}")
        print(f"Telephone: {tel}")
        print(f"Alternative Name: {alt_name}")
        print(f"Street: {street}")
        print(f"Postal Code: {codepostal}")
        print(f"Locality: {locality}")
        print(f"Country: {country}")
        print(f"Web: {web}")
        print(f"Email: {email}")


        # Asignar información del buque
        if vessel_input == "sdg":
            vessel = "Sarmiento de Gamboa"
            vessel_mode = "Sarmiento"
            vessel_reduit = "sdg"
        elif vessel_input == "hes":
            vessel = "Hespérides"
            vessel_mode = "Hesperides"
            vessel_reduit = "hes"
        elif vessel_input == "odb":
            vessel = "Odón de Buen"
            vessel_mode = "Odón"
            vessel_reduit = "odb"
            vessel_code = "29OD"
        else:
            raise ValueError(f"Invalid vessel_input: {vessel_input}")

        # Extraer fecha
        dia = cruise_id[10:12]
        mes = cruise_id[8:10]
        any = cruise_id[4:8]
        short_date = f"{any}-{mes}-{dia}"

        # Crear carpeta y preparar archivo CDI individual
        cdi_individual = f"{cruise_id}_cdi.xml"
        nombre_carpeta = cruise_id
        crear_carpeta(nombre_carpeta)

        # Copiar plantilla XML
        if path.exists("model_cdi_sensegml_sensesensor.txt"):
            remove("model_cdi_sensegml_sensesensor.txt")
        shutil.copy("model_cdi_sensegml_sensesensor.xml", cdi_individual)
        logging.info(f"Created CDI file: {cdi_individual}")

        #Posem la url perque trobi el gml i l'enganxi en el xml
        input_file = cdi_individual
        input_url = 'http://datahub.utm.csic.es/ws/getTrack/GML/?id=' + vessel_input + cruise_id[4:12] + '&n=999'
        output_file = cdi_individual

        # Definir namespaces
        namespace = {
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gml': 'http://www.opengis.net/gml',
            'gco': 'http://www.isotc211.org/2005/gco',
            'sdn': 'http://www.seadatanet.org',
            'gmx': 'http://www.isotc211.org/2005/gmx'
        }

        # GML y BBOX
        #gml_result, bbox = extract_gml_and_bbox(ruta_csv)
        #logging.info(f"GML result: {gml_result}")
        #logging.info(f"BBOX: {bbox}")

        # Reemplazos en el XML

        deperature_country_code = get_country_code_by_label(country)
        #afegim short id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
        posList.text = cruise_id
        tree.write(output_file)

        #afegim csr id
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:CharacterString[contains(text(), 'CSR_CRUISE_NAME')]", namespaces=namespace)[0]
        posList.text = cruise_name
        tree.write(output_file)

        #afegim short date
        data=any +"-" + mes + "-"+ dia
        tree = etree.parse(input_file)
        posList = tree.xpath("//gco:Date[contains(text(), '2023-05-04')]", namespaces=namespace)[0]
        posList.text = data
        tree.write(output_file)

        #afegim org_name
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
            if posList:
                posList[0].text = org_name
                posList[0].set("codeListValue", notation)
                tree.write(output_file)
                print("✓ Updated organization name (1st occurrence)")
            else:
                print("⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found")
        except Exception as e:
            print(f"✗ ERROR updating org_name (1st): {str(e)}")

        #afegim org_name per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
            if posList:
                posList[0].text = org_name
                posList[0].set("codeListValue", notation)
                tree.write(output_file)
                print("✓ Updated organization name (2nd occurrence)")
            else:
                print("⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating org_name (2nd): {str(e)}")
        
        #afegim street
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
            if posList:
                posList[0].text = street
                tree.write(output_file)
                print("✓ Updated street (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_street' text found")
        except Exception as e:
            print(f"✗ ERROR updating street (1st): {str(e)}")

        #afegim street per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
            if posList:
                posList[0].text = street
                tree.write(output_file)
                print("✓ Updated street (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_street' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating street (2nd): {str(e)}")

        #afegim city
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
            if posList:
                posList[0].text = locality
                tree.write(output_file)
                print("✓ Updated city (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_city' text found")
        except Exception as e:
            print(f"✗ ERROR updating city (1st): {str(e)}")

        #afegim city per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
            if posList:
                posList[0].text = locality
                tree.write(output_file)
                print("✓ Updated city (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_city' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating city (2nd): {str(e)}")

        #afegim country
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CountryCode[contains(text(), 'org_country')]", namespaces=namespace)
            if posList:
                posList[0].text = country
                posList[0].set("codeListValue", deperature_country_code)
                tree.write(output_file)
                print("✓ Updated country (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_country' text found")
        except Exception as e:
            print(f"✗ ERROR updating country (1st): {str(e)}")

        #afegim country per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CountryCode[contains(text(), 'org_country')]", namespaces=namespace)
            if posList:
                posList[0].text = country
                posList[0].set("codeListValue", deperature_country_code)
                tree.write(output_file)
                print("✓ Updated country (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_country' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating country (2nd): {str(e)}")

        #afegim email
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
            if posList:
                posList[0].text = email
                tree.write(output_file)
                print("✓ Updated email (1st occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_mail' text found")
        except Exception as e:
            print(f"✗ ERROR updating email (1st): {str(e)}")

        #afegim email per segon cop
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
            if posList:
                posList[0].text = email
                tree.write(output_file)
                print("✓ Updated email (2nd occurrence)")
            else:
                print("⚠ WARNING: No element with 'org_mail' text found (2nd time)")
        except Exception as e:
            print(f"✗ ERROR updating email (2nd): {str(e)}")

        logging.info(f"Successfully processed general sense sensor XML for cruise {cruise_id}")

        #afegim csrcodelist
        tree = etree.parse(input_file)
        try:
            posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)
            if posList:
                posList[0].text = description_csr
                posList[0].set("codeListValue", id_csr)
                tree.write(output_file)
                print("✓ Updated CSR code")
            else:
                print("⚠ WARNING: No CSR code element found")
        except Exception as e:
            print(f"✗ ERROR updating CSR code: {str(e)}")

=======
import pandas as pd
import glob
from datetime import datetime
import numpy as np
import shutil
import os,sys
from os import remove
from os import path
from datetime import datetime
import requests, argparse
from lxml import etree
import copy
#importem els scripts de cada cdi

def crear_carpeta (nombre_carpeta):
    try:
        # Intenta crear la carpeta
        os.mkdir(nombre_carpeta)
        print(f"La carpeta '{nombre_carpeta}' se ha creado correctamente.")
    except FileExistsError:
            # Si la carpeta ya existe, imprime un mensaje
            print(f"La carpeta '{nombre_carpeta}' ya existe.")

def general (cruise_id, cruise_name,  vessel_input, valor_org, csr_code,ruta_csv,selects,date_inicial, date_final):
  print(selects)
  fila=0  
  if csr_code != "UNKNOWN":
    #agafem el xml i busquem en ell la campanya que estem fent. aqui s'agafa el identificador i i la descripció per posar al xml
    xml_file = "http://161.111.137.92:8001/static/csrCodeList.xml"
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Buscar los elementos cruisename
    for cruisename in root.findall(".//{http://www.opengis.net/gml}cruisename"):
        if cruisename.text == csr_code:
            description_csr = cruisename.getparent().find("{http://www.opengis.net/gml}description").text
            id_csr = cruisename.getparent().find("{http://www.opengis.net/gml}identifier").text            
    print (id_csr)
    print(description_csr)
  
  else: 
    id_csr = '2004 - Unknown(ZZ99)'
    description_csr = "20050002" 


  sparql_query = '''
      SELECT ?org ?name ?altName (CONCAT(?name, " (", ?altName, ")") AS ?orgName) ?notation ?street ?codepostal ?locality ?country ?web

      WHERE {{

          ?org a <http://www.w3.org/ns/org#Organization> ;
                  <http://www.w3.org/ns/org#name> ?name ;
                <http://www.w3.org/2004/02/skos/core#notation> ?notation ;
                <http://www.w3.org/2006/vcard/ns#street-address> ?street ;
                <http://www.w3.org/2006/vcard/ns#postal-code> ?codepostal ;
                <http://www.w3.org/2006/vcard/ns#locality> ?locality ;
                <http://www.w3.org/2006/vcard/ns#country-name> ?country ;
                <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?web ;
                <http://www.w3.org/2004/02/skos/core#altName> ?altName.
      
      FILTER (?org = <{0}>)
      }}
      '''.format(valor_org)

  sparql_endpoint = 'https://edmo.seadatanet.org/sparql/sparql'
  query_params = {'query': sparql_query, 'accept': 'application/json'}

  response = requests.get(sparql_endpoint, params=query_params)
  print(response)


  if response.status_code == 200:
      data = response.json()
      results = data.get('results', {}).get('bindings', [])
  # org,org_name,notation,tel,alt_name,street,codepostal,locality, country, web, email
      for result in results:
          org = result.get('org', {}).get('value', 'N/A')
          org_name = result.get('orgName', {}).get('value', 'N/A')
          notation = result.get('notation', {}).get('value', 'N/A')
          tel = result.get('tel', {}).get('value', 'N/A')
          alt_name = result.get('altName', {}).get('value', 'N/A')
          street = result.get('street', {}).get('value', 'N/A')
          codepostal = result.get('codepostal', {}).get('value', 'N/A')
          locality = result.get('locality', {}).get('value', 'N/A')
          #email = result.get('email', {}).get('value', 'N/A')
          country = result.get('country', {}).get('value', 'N/A')
          web = result.get('web', {}).get('value', 'N/A')
          
          # Modify the email address before printing
          #email = result.get('email', {}).get('value', 'N/A')
          #email = email.replace('mailto:', '').replace('%40', '@')

          print(f'Organization URI: {org}')
          print(f'Organization Name: {org_name}')
          print(f'Notation: {notation}')
          print(f'Telephone: {tel}')
          print(f'Alternative Name: {alt_name}')
          print(f'Street: {street}')
          print(f'Postal Code: {codepostal}')
          print(f'Locality: {locality}')
          #print(f'Email: {email}')
          print(f'Country: {country}')
          print(f'Web: {web}')
          print('-' * 30)
       
  sparql_query_email = '''
    SELECT ?org ?name ?altName (CONCAT(?name, " (", ?altName, ")") AS ?orgName) ?email

    WHERE {{

        ?org a <http://www.w3.org/ns/org#Organization> ;
                <http://www.w3.org/2006/vcard/ns#email> ?email.
            
    FILTER (?org = <{0}>)
    }}
    '''.format(valor_org)

  sparql_endpoint = 'https://edmo.seadatanet.org/sparql/sparql'
  query_params_email = {'query': sparql_query_email, 'accept': 'application/json'}

  response = requests.get(sparql_endpoint, params=query_params_email)
  print(response)

  if response.status_code == 200:
      data = response.json()
      print("data:",data)
      results = data.get('results', {}).get('bindings', [])
      #results = "{'head': {'vars': ['org', 'name', 'altName', 'orgName', 'email']}, 'results': {'bindings': []}}"
      resultat = "{'head': {'vars': ['org', 'name', 'altName', 'orgName', 'email']}, 'results': {'bindings': []}}"
      data = str (data)
      if data == resultat: 
          print("no hi ha email")
          email = "sdn-userdesk@seadatanet.org"

      elif data != resultat:
              # org,org_name,notation,tel,alt_name,street,codepostal,locality, country, web, email
          for result in results:
              email = result.get('email', {}).get('value', 'N/A')
              # Modify the email address before printing
              email = result.get('email', {}).get('value', 'N/A')
              email = email.replace('mailto:', '').replace('%40', '@')
              print(f'Email: {email}')
    
  if vessel_input == "sdg":
    vessel_mode = "Sarmiento"
    vessel_reduit='sdg' 
    vessel = "Sarmiento de Gamboa"
  elif vessel_input == "hes":
    vessel_mode ="Hesperides"
    vessel_reduit="hes"
    vessel = "Hespérides"
    

 
  dia= cruise_id[10:12]
  mes=cruise_id[8:10]
  any=cruise_id[4:8]
  short_date = any +"-"+ mes +"-"+ dia

  fila=0

  if path.exists("model_cdi_sensegml.xml.txt"):
    remove("model_cdi_sensegml.xml.txt")
  
  cdi_individual =cruise_id + "_cdi.xml"
  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)
  

  shutil.copy("model_cdi_sensegml.xml", cdi_individual)
  print (cdi_individual)

  #Posem la url perque trobi el gml i l'enganxi en el xml
  input_file= cdi_individual
  input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
  output_file= cdi_individual


  #Definim el namespace perquè el trobi en el XML
  namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx'
  }

  #afegim short id
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'SHORT_ID')]", namespaces=namespace)[0]
  posList.text = cruise_id
  tree.write(output_file)

  #afegim csr id
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'CSR_CRUISE_NAME')]", namespaces=namespace)[0]
  posList.text = cruise_name
  tree.write(output_file)

  #afegim short date
  data=any +"-" + mes + "-"+ dia
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:Date[contains(text(), '2023-05-04')]", namespaces=namespace)[0]
  posList.text = data
  tree.write(output_file)

  #afegim org_name
  tree = etree.parse(input_file)
  posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
  posList.text = org_name
  posList.set ("codeListValue",notation)
  tree.write(output_file)
  
  #afegim org_name
  tree = etree.parse(input_file)
  posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
  posList.text = org_name
  posList.set ("codeListValue",notation)
  tree.write(output_file)
 
  #afegim street
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
  posList.text = street
  tree.write(output_file)
  #afegim street
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)[0]
  posList.text = street
  tree.write(output_file)
  #afegim city
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
  posList.text = country
  tree.write(output_file)

  #afegim city
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)[0]
  posList.text = country
  tree.write(output_file)

  #afegim email
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
  posList.text = email
  tree.write(output_file)
  #afegim email
  tree = etree.parse(input_file)
  posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)[0]
  posList.text = email
  tree.write(output_file)

  #afegim csrcodelist
  tree = etree.parse(input_file)
  posList = tree.xpath("//sdn:SDN_CSRCode[contains(text(), '2004 - Unknown(ZZ99)')]", namespaces=namespace)[0]
  posList.text = description_csr
  posList.set ("codeListValue",id_csr)
  tree.write(output_file)


>>>>>>> main
