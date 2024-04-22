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



def crear_carpeta (nombre_carpeta):
    try:
        # Intenta crear la carpeta
        os.mkdir(nombre_carpeta)
        print(f"La carpeta '{nombre_carpeta}' se ha creado correctamente.")
    except FileExistsError:
            # Si la carpeta ya existe, imprime un mensaje
            print(f"La carpeta '{nombre_carpeta}' ya existe.")
            
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
      SELECT ?org (CONCAT(?name, " (", ?altName, ")") AS ?orgName) ?notation ?tel ?altName ?street ?codepostal ?locality ?email ?country ?web
      WHERE {{
      ?org a <http://www.w3.org/ns/org#Organization> ;
          <http://www.w3.org/2004/02/skos/core#altName> ?altName ;
          <http://www.w3.org/ns/org#name> ?name ;
          <http://www.w3.org/2006/vcard/ns#tel> ?tel ;
          <http://www.w3.org/2004/02/skos/core#notation> ?notation ;
          <http://www.w3.org/2006/vcard/ns#street-address> ?street ;
          <http://www.w3.org/2006/vcard/ns#postal-code> ?codepostal ;
          <http://www.w3.org/2006/vcard/ns#locality> ?locality ;
          <http://www.w3.org/2006/vcard/ns#email> ?email ;
          <http://www.w3.org/2006/vcard/ns#country-name> ?country ;
          <http://www.w3.org/2000/01/rdf-schema#seeAlso> ?web .
      
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
          email = result.get('email', {}).get('value', 'N/A')
          country = result.get('country', {}).get('value', 'N/A')
          web = result.get('web', {}).get('value', 'N/A')
          
          # Modify the email address before printing
          email = result.get('email', {}).get('value', 'N/A')
          email = email.replace('mailto:', '').replace('%40', '@')

          print(f'Organization URI: {org}')
          print(f'Organization Name: {org_name}')
          print(f'Notation: {notation}')
          print(f'Telephone: {tel}')
          print(f'Alternative Name: {alt_name}')
          print(f'Street: {street}')
          print(f'Postal Code: {codepostal}')
          print(f'Locality: {locality}')
          print(f'Email: {email}')
          print(f'Country: {country}')
          print(f'Web: {web}')
          print('-' * 30)
       

  if vessel_input == "sdg":
    vessel_mode = "Sarmiento"
    vessel_reduit='sdg' 
    vessel = "Sarmiento de Gamboa"
  elif vessel_input == "hes":
    vessel_mode ="Hesperides"
    vessel_reduit="hes"
    vessel = "Hespérides"
    
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
  


  underway_general =cruise_id + "_underway.xml"
  
  nombre_carpeta = cruise_id

  crear_carpeta (nombre_carpeta)


  shutil.copy("model_underway.xml", underway_general)
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


