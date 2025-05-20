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
from flask import Flask, render_template, url_for, request, redirect, jsonify ,send_file, Response, send_from_directory, send_file
import json


def crear_carpeta (nombre_carpeta):
    try:
        # Intenta crear la carpeta
        os.mkdir(nombre_carpeta)
        print(f"La carpeta '{nombre_carpeta}' se ha creado correctamente.")
    except FileExistsError:
            # Si la carpeta ya existe, imprime un mensaje
            print(f"La carpeta '{nombre_carpeta}' ya existe.")
            
def underway_general (cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code):
  
    # Handle CSR code
  if csr_code != "UNKNOWN":
      # Download and parse the XML file
      xml_url = "https://161.111.137.92:8001/static/csrCodeList.xml"
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
  json_path = os.path.join("static", "csv", "sparql.json")
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
    
  url_bbox = "https://datahub.utm.csic.es/ws/getBBox/?id="+ vessel_reduit + cruise_id[4:12]
  r = requests.get(url_bbox)
  input_url='https://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
 
  dia= cruise_id[10:12]
  mes=cruise_id[8:10]
  any=cruise_id[4:8]
  short_date = any +"-"+ mes +"-"+ dia

  fila=0

  if path.exists("model_underway.txt"):
    remove("model_underway.txt")
  

  underway_general =cruise_id + "_underway.xml"
  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)


  shutil.copy("model_underway.xml", underway_general)
  print (underway_general)

  #Posem la url perque trobi el gml i l'enganxi en el xml
  input_file= underway_general
  input_url='https://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
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
  url_bbox = "https://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
  print (url_bbox)
  tree = etree.parse(input_file)
  r = requests.get(url_bbox)
  coord= r.text[4:-2] #nomes coordenades 4separades per espais i comes
  try : 
    posicio_primer_espai= r.text[4:-2].index(" ")

  except:
      return render_template('error.html', url_bbox=url_bbox, cruise_id= cruise_id)
  
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

  #afegim org_name
  tree = etree.parse(input_file)
  posList = tree.xpath("//sdn:SDN_EDMOCode[contains(text(), 'ORG_NAME')]", namespaces=namespace)[0]
  print("arriba aqui?----------------------------")
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

def underway_general_sense_sensor (cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code):
  
  # Handle CSR code
  if csr_code != "UNKNOWN":
      # Download and parse the XML file
      xml_url = "https://161.111.137.92:8001/static/csrCodeList.xml"
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
  json_path = os.path.join("static", "csv", "sparql.json")
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
    
  url_bbox = "https://datahub.utm.csic.es/ws/getBBox/?id="+ vessel_reduit + cruise_id[4:12]
  r = requests.get(url_bbox)
  input_url='https://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
 
  dia= cruise_id[10:12]
  mes=cruise_id[8:10]
  any=cruise_id[4:8]
  short_date = any +"-"+ mes +"-"+ dia

  fila=0

  if path.exists("model_underway.txt"):
    remove("model_underway.txt")
  


  underway_general =cruise_id + "_underway.xml"
  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)


  shutil.copy("model_underway_sensesensor.xml", underway_general)
  print (underway_general)

  #Posem la url perque trobi el gml i l'enganxi en el xml
  input_file= underway_general
  input_url='https://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
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
  url_bbox = "https://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
  print (url_bbox)
  tree = etree.parse(input_file)
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

