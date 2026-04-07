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
<<<<<<< HEAD
from flask import Flask, render_template, url_for, request, redirect, jsonify ,send_file, Response, send_from_directory, send_file
import json
import csv
=======

>>>>>>> main


def crear_carpeta (nombre_carpeta):
    try:
        # Intenta crear la carpeta
        os.mkdir(nombre_carpeta)
        print(f"La carpeta '{nombre_carpeta}' se ha creado correctamente.")
    except FileExistsError:
            # Si la carpeta ya existe, imprime un mensaje
            print(f"La carpeta '{nombre_carpeta}' ya existe.")
<<<<<<< HEAD

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

def underway_general (cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final):

    # Handle CSR code 
  if csr_code != "UNKNOWN":
      # Download and parse the XML file
      xml_url = "http://datahub.utm.csic.es/cdigen/static/csrCodeList.xml"
      response = requests.get(xml_url, verify=False)  # verify=False for self-signed certificates
      if response.status_code != 200:
          raise Exception(f"Failed to download CSR code list: {response.status_code}")
          
      root = etree.fromstring(response.content)

      # Search for the cruisename element
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
  print(f"DEBUG: Total organizations in JSON: {len(results)}")
  print(f"DEBUG: Looking for organization URI: {valor_org}")
  
  matched = next((res for res in results if res.get("org", {}).get("value") == valor_org), None)

  if not matched:
      print(f"WARNING: Organization with URI {valor_org} not found in JSON file!")
      print(f"DEBUG: Available organization URIs in JSON:")
      for i, org_data in enumerate(results):
          org_uri = org_data.get("org", {}).get("value", "NO URI")
          org_name = org_data.get("orgName", {}).get("value", "NO NAME")
          print(f"  [{i}] {org_uri} -> {org_name}")
      raise Exception(f"Organization with URI {valor_org} not found in the JSON file.")

  # Extract the required fields
  org = matched.get("org", {}).get("value", "N/A")
  deperature_country_name=matched.get("name",{}).get("value", "N/A")
  org_name = matched.get("orgName", {}).get("value", "N/A")
  notation = matched.get("notation", {}).get("value", "N/A")
  alt_name = matched.get("altName", {}).get("value", "N/A")
  
  name = matched.get("name", {}).get("value", "N/A")
  print(f"DEBUG: Extracted org_name from JSON: '{org_name}'")
  print(f"DEBUG: Extracted alt_name from JSON: '{alt_name}'")
  print(f"DEBUG: Extracted name from JSON: '{name}'")

  org_name = compose_org_name(name, alt_name)
  if org_name == "N/A":
      print("WARNING: Organization name from JSON is N/A and no alternative name available!")
  else:
      print(f"INFO: Composed organization name: '{org_name}'")
  
  tel = matched.get("tel", {}).get("value", "N/A")
  street = matched.get("street", {}).get("value", "N/A")
  codepostal = matched.get("codepostal", {}).get("value", "N/A")
  locality = matched.get("locality", {}).get("value", "N/A")
  country = matched.get("country", {}).get("value", "N/A")
  web = matched.get("web", {}).get("value", "N/A")
  email = matched.get("email", {}).get("value", "sdn-userdesk@seadatanet.org").replace("mailto:", "").replace("%40", "@")

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
  
  if vessel_input == "sdg":
    vessel_mode = "Sarmiento"
    vessel_reduit='sdg' 
    vessel = "Sarmiento de Gamboa"
  elif vessel_input == "hes":
    vessel_mode ="Hesperides"
    vessel_reduit="hes"
    vessel = "Hespérides"
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
    
  url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+ vessel_reduit + cruise_id[4:12]
  r = requests.get(url_bbox)
  input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
 
  dia= cruise_id[10:12]
  mes=cruise_id[8:10]
  any=cruise_id[4:8]
  short_date = any +"-"+ mes +"-"+ dia

  fila=0

  if path.exists("model_underway_org.txt"):
    remove("model_underway_org.txt")
  

  underway_general =cruise_id + "_underway_org.xml"
  print(f'El arxiu es {underway_general}')

  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)


  shutil.copy("model_underway_org.xml", underway_general)
  print (underway_general)

  #Posem la url perque trobi el gml i l'enganxi en el xml
  input_file= underway_general
  input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
  output_file= underway_general


  #Definim el namespace perquè el trobi en el XML
  namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx'
  }


  #afegim GML
  url = input_url

  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:posList[contains(text(), '-1 -1 -1 -1')]", namespaces=namespace)[0]
  posList.text = requests.get(url).text.strip()
  tree.write(output_file)
  #print('Your GMLs coordinates were successfully added to your new XML document.')"""

  #afegim BOUNDING BOX
  url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
  print (url_bbox)
  tree = etree.parse(input_file)
  try:
    r = requests.get(url_bbox)
    r.raise_for_status()
    raw_bbox = r.text.strip()

    if raw_bbox.upper().startswith("BOX(") and raw_bbox.endswith(")"):
      bbox_text = raw_bbox[4:-1]
    elif "," in raw_bbox and " " in raw_bbox:
      bbox_text = raw_bbox
    else:
      raise ValueError(f"Unexpected bbox format: {raw_bbox!r}")

    pair_1, pair_2 = [p.strip() for p in bbox_text.split(",", 1)]
    w, s = pair_1.split()
    e, n = pair_2.split()

    posList_w = tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)
    posList_s = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)
    posList_e = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)
    posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)

    if posList_w and posList_s and posList_e and posList_n:
      posList_w[0].text = w
      posList_s[0].text = s
      posList_e[0].text = e
      posList_n[0].text = n
      tree.write(output_file)
    else:
      print(f"Warning: Could not find BBOX placeholder elements in {input_file}")

  except Exception as err:
    print(f"Warning: could not get/update bbox from {url_bbox}: {err}")

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

  #afegim data inicial
  hora_inicial = date_inicial[11:]
  begin_position = any + "-"+ mes + "-" + dia + "T" + hora_inicial

  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:beginPosition[contains(text(), '2023-01-01T00:00:00')]", namespaces=namespace)[0]
  posList.text = begin_position
  tree.write(output_file)

  #afegim data final
  hora_final = date_final[11:]
  data_final = date_final[:10]
  dia_final= data_final[0:2]
  mes_final=data_final[3:5]
  any_final=data_final[6:10]

  final_position = any_final + "-"+ mes_final + "-" + dia_final + "T" + hora_final
  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:endPosition[contains(text(), '2023-01-02T00:00:00')]", namespaces=namespace)[0]
  posList.text = final_position
  tree.write(output_file)

  deperature_country_code = get_country_code_by_label(country)

  #afegim org_name
  tree = etree.parse(input_file)
  print(f"DEBUG: Looking for SDN_EDMOCode with text 'ORG_NAME'")
  org_elements = tree.xpath("//sdn:SDN_EDMOCode", namespaces=namespace)
  print(f"DEBUG: Found {len(org_elements)} total SDN_EDMOCode elements")
  for i, elem in enumerate(org_elements):
      print(f"DEBUG:   [{i}] Text: '{elem.text}'")
  
  try:
      posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
      if posList:
          print(f"DEBUG: Found element with 'ORG_NAME', updating with org_name='{org_name}' and notation='{notation}'")
          posList[0].text = org_name
          posList[0].set("codeListValue", notation)
          tree.write(output_file)
          print(f"✓ Updated organization name (1st occurrence)")
      else:
          print(f"⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found. Available texts: {[e.text for e in org_elements]}")
  except Exception as e:
      print(f"✗ ERROR updating org_name (1st): {str(e)}")

  #afegim org_name per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
      if posList:
          print(f"DEBUG: Found element with 'ORG_NAME', updating with org_name='{org_name}' and notation='{notation}'")
          posList[0].text = org_name
          posList[0].set("codeListValue", notation)
          tree.write(output_file)
          print(f"✓ Updated organization name (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating org_name (2nd): {str(e)}")

  #afegim street
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
      if posList:
          posList[0].text = street
          tree.write(output_file)
          print(f"✓ Updated street (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_street' text found")
  except Exception as e:
      print(f"✗ ERROR updating street (1st): {str(e)}")

  #afegim street per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
      if posList:
          posList[0].text = street
          tree.write(output_file)
          print(f"✓ Updated street (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_street' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating street (2nd): {str(e)}")

  #afegim city
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
      if posList:
          posList[0].text = locality
          tree.write(output_file)
          print(f"✓ Updated city (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_city' text found")
  except Exception as e:
      print(f"✗ ERROR updating city (1st): {str(e)}")

  #afegim city per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
      if posList:
          posList[0].text = locality
          tree.write(output_file)
          print(f"✓ Updated city (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_city' text found (2nd time)")
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
          print(f"✓ Updated country (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_country' text found")
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
          print(f"✓ Updated country (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_country' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating country (2nd): {str(e)}")

  #afegim email
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
      if posList:
          posList[0].text = email
          tree.write(output_file)
          print(f"✓ Updated email (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_mail' text found")
  except Exception as e:
      print(f"✗ ERROR updating email (1st): {str(e)}")

  #afegim email per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
      if posList:
          posList[0].text = email
          tree.write(output_file)
          print(f"✓ Updated email (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_mail' text found (2nd time)")
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
          print(f"✓ Updated CSR code")
      else:
          print(f"⚠ WARNING: No CSR code element found")
  except Exception as e:
      print(f"✗ ERROR updating CSR code: {str(e)}")

def underway_general_sense_sensor (cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final):
  
  # Handle CSR code
  if csr_code != "UNKNOWN":
      # Download and parse the XML file
      xml_url = "http://datahub.utm.csic.es/cdigen/static/csrCodeList.xml"
      response = requests.get(xml_url, verify=False)  # verify=False for self-signed certificates
      if response.status_code != 200:
          raise Exception(f"Failed to download CSR code list: {response.status_code}")
          
      root = etree.fromstring(response.content)

      # Search for the cruisename element
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

  # Extract the required fields
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
=======
            
def underway_general (cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code):
  

  
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
    
>>>>>>> main

  if vessel_input == "sdg":
    vessel_mode = "Sarmiento"
    vessel_reduit='sdg' 
    vessel = "Sarmiento de Gamboa"
  elif vessel_input == "hes":
    vessel_mode ="Hesperides"
    vessel_reduit="hes"
    vessel = "Hespérides"
<<<<<<< HEAD
  elif vessel_input == "odb":
    vessel = "Odón de Buen"
    vessel_mode = "Odón"
    vessel_reduit = "odb"
    vessel_code = "29OD"
  if vessel_input == "gdc":
    vessel_mode = "Garcia del Cid"
    vessel_reduit = "gdc"
    vessel = "Garcia del Cid"
=======
>>>>>>> main
    
  url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+ vessel_reduit + cruise_id[4:12]
  r = requests.get(url_bbox)
  input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
 
  dia= cruise_id[10:12]
  mes=cruise_id[8:10]
  any=cruise_id[4:8]
  short_date = any +"-"+ mes +"-"+ dia

  fila=0

  if path.exists("model_underway.txt"):
    remove("model_underway.txt")
  


<<<<<<< HEAD
  underway_general = cruise_id + "_underway.xml"
=======
  underway_general =cruise_id + "_underway.xml"
>>>>>>> main
  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)


<<<<<<< HEAD
  shutil.copy("model_underway_sensesensor.xml", underway_general)
=======
  shutil.copy("model_underway.xml", underway_general)
>>>>>>> main
  print (underway_general)

  #Posem la url perque trobi el gml i l'enganxi en el xml
  input_file= underway_general
  input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
  output_file= underway_general


  #Definim el namespace perquè el trobi en el XML
  namespace = {
      'gmd': 'http://www.isotc211.org/2005/gmd',
      'gml': 'http://www.opengis.net/gml',
      'gco': 'http://www.isotc211.org/2005/gco',
      'sdn': 'http://www.seadatanet.org',
      'gmx': 'http://www.isotc211.org/2005/gmx'
  }


  #afegim GML
  url = input_url

  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:posList[contains(text(), '-1 -1 -1 -1')]", namespaces=namespace)[0]
  posList.text = requests.get(url).text.strip()
  tree.write(output_file)
  #print('Your GMLs coordinates were successfully added to your new XML document.')"""

  #afegim BOUNDING BOX
  url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
  print (url_bbox)
  tree = etree.parse(input_file)
<<<<<<< HEAD
  try:
    r = requests.get(url_bbox)
    r.raise_for_status()
    raw_bbox = r.text.strip()

    if raw_bbox.upper().startswith("BOX(") and raw_bbox.endswith(")"):
      bbox_text = raw_bbox[4:-1]
    elif "," in raw_bbox and " " in raw_bbox:
      bbox_text = raw_bbox
    else:
      raise ValueError(f"Unexpected bbox format: {raw_bbox!r}")

    pair_1, pair_2 = [p.strip() for p in bbox_text.split(",", 1)]
    w, s = pair_1.split()
    e, n = pair_2.split()

    posList_w = tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)
    posList_s = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)
    posList_e = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)
    posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)

    if posList_w and posList_s and posList_e and posList_n:
      posList_w[0].text = w
      posList_s[0].text = s
      posList_e[0].text = e
      posList_n[0].text = n
      tree.write(output_file)
    else:
      print(f"Warning: Could not find BBOX placeholder elements in {input_file}")

  except Exception as err:
    print(f"Warning: could not get/update bbox from {url_bbox}: {err}")
=======
  r = requests.get(url_bbox)
  coord= r.text[4:-2] #nomes coordenades 4separades per espais i comes
  posicio_primer_espai= r.text[4:-2].index(" ")
  posicio_coma= r.text[4:-2].index(",")
  w= coord[0:posicio_primer_espai]
  s= coord[posicio_primer_espai:posicio_coma].strip()
  coord_2=coord[posicio_coma:]
  coord_2= coord_2[1:]
  posicio_segon_espai= coord_2.index(" ")
  e= coord_2[0:posicio_segon_espai].strip()
  n= coord_2[posicio_segon_espai:].strip()

  posList_w= tree.xpath("//gco:Decimal[contains(text(), '80.00')]", namespaces=namespace)[0]
  posList_w.text=w
  posList_s = tree.xpath("//gco:Decimal[contains(text(), '10.00')]", namespaces=namespace)[0]
  posList_s.text= s
  posList_e = tree.xpath("//gco:Decimal[contains(text(), '90.00')]", namespaces=namespace)[0]
  posList_e.text= e
  posList_n = tree.xpath("//gco:Decimal[contains(text(), '20.00')]", namespaces=namespace)[0]
  posList_n.text=n

  tree.write(output_file)
>>>>>>> main

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

  #afegim data inicial
  hora_inicial = date_inicial[11:]
  begin_position = any + "-"+ mes + "-" + dia + "T" + hora_inicial

  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:beginPosition[contains(text(), '2023-01-01T00:00:00')]", namespaces=namespace)[0]
  posList.text = begin_position
  tree.write(output_file)

  #afegim data final
  hora_final = date_final[11:]
  data_final = date_final[:10]
  dia_final= data_final[0:2]
  mes_final=data_final[3:5]
  any_final=data_final[6:10]

  final_position = any_final + "-"+ mes_final + "-" + dia_final + "T" + hora_final
  tree = etree.parse(input_file)
  posList = tree.xpath("//gml:endPosition[contains(text(), '2023-01-02T00:00:00')]", namespaces=namespace)[0]
  posList.text = final_position
  tree.write(output_file)
<<<<<<< HEAD
  deperature_country_code = get_country_code_by_label(country)


  #afegim org_name
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)
      if posList:
          posList[0].text = org_name
          posList[0].set("codeListValue", notation)
          tree.write(output_file)
          print(f"✓ Updated organization name (1st occurrence)")
      else:
          print(f"⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found")
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
          print(f"✓ Updated organization name (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No SDN_EDMOCode element with 'ORG_NAME' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating org_name (2nd): {str(e)}")
 
  #afegim street
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
      if posList:
          posList[0].text = street
          tree.write(output_file)
          print(f"✓ Updated street (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_street' text found")
  except Exception as e:
      print(f"✗ ERROR updating street (1st): {str(e)}")

  #afegim street per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_street')]", namespaces=namespace)
      if posList:
          posList[0].text = street
          tree.write(output_file)
          print(f"✓ Updated street (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_street' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating street (2nd): {str(e)}")

  #afegim city
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
      if posList:
          posList[0].text = locality
          tree.write(output_file)
          print(f"✓ Updated city (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_city' text found")
  except Exception as e:
      print(f"✗ ERROR updating city (1st): {str(e)}")

  #afegim city per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_city')]", namespaces=namespace)
      if posList:
          posList[0].text = locality
          tree.write(output_file)
          print(f"✓ Updated city (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_city' text found (2nd time)")
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
          print(f"✓ Updated country (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_country' text found")
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
          print(f"✓ Updated country (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_country' text found (2nd time)")
  except Exception as e:
      print(f"✗ ERROR updating country (2nd): {str(e)}")

  #afegim email
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
      if posList:
          posList[0].text = email
          tree.write(output_file)
          print(f"✓ Updated email (1st occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_mail' text found")
  except Exception as e:
      print(f"✗ ERROR updating email (1st): {str(e)}")

  #afegim email per segon cop
  tree = etree.parse(input_file)
  try:
      posList = tree.xpath("//gco:CharacterString[contains(text(), 'org_mail')]", namespaces=namespace)
      if posList:
          posList[0].text = email
          tree.write(output_file)
          print(f"✓ Updated email (2nd occurrence)")
      else:
          print(f"⚠ WARNING: No element with 'org_mail' text found (2nd time)")
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
          print(f"✓ Updated CSR code")
      else:
          print(f"⚠ WARNING: No CSR code element found")
  except Exception as e:
      print(f"✗ ERROR updating CSR code: {str(e)}")
=======

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

