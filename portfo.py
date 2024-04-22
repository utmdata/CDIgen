from flask import Flask, render_template, url_for, request, redirect, jsonify ,send_file, Response, send_from_directory, send_file, request
from flask_cors import CORS
from flask import session

app = Flask(__name__, static_url_path='/static')
CORS(app, resources={r"/*": {"origins": "http://datahub.utm.csic.es"}})
import csv
import cgi
import pandas as pd
import os
from os import path, remove
from datetime import datetime
import scripts.underwayweb,scripts.met_script, scripts.ts_script, scripts.sbe_script, scripts.generalweb, scripts.xbt ,scripts.adcp, scripts.ffe ,scripts.mbe, scripts.mcs, scripts.mag, scripts.sss, scripts.srs, scripts.sbp
import scripts.ctd, scripts.dre , scripts.ctd_ros, scripts.xsv , scripts.ctd_ros_ladcp, scripts.grv, scripts.tra, scripts.moc
import requests
import shutil
import logging
from shutil import make_archive,copy
import zipfile, tempfile
import json, re

#Ruta estàtica de Flask a static/tareas
# Define the directory to save the generated zip file
ZIP_FOLDER = os.path.join(app.static_folder, 'tareas')
ruta_csv = ""

# Function to fetch and save the CSR code list XML file
def fetch_and_save_csr_code_list():
    url = "https://csr.seadatanet.org/isoCodelists/csrCodeList.xml"
    static_folder = "static"
    file_name = "csrCodeList.xml"
    file_path = os.path.join(static_folder, file_name)

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


# Ara aprendrem a fer tota l'associació de diferents pàgines a HTML d'una forma eficient i sense haver d'afegir cada cop una funció per cada pàgina.

@app.route('/')
def my_home():
    return render_template('index.html')


@app.route(
    '/<string:page_name>')  # Fent això enlloc d'haver de copiar tants fx per pàgines que tinguem agafarà el page_name i el mostrarà!
def html_page(page_name):
    return render_template(page_name)


# Ara podem accedir a aquestes dades amb el Flask attribute request.

def grabar_underway (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data,valor_org, csr_code):
        input_url='http://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
        scripts.underwayweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, data, valor_org, csr_code)

        if "met" in data:
            scripts.met_script.funcio_met (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data)
        else:
            print ("No met")

        
        if "grv" in data:
            scripts.grv.funcio_grv (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data)
        else:
            print ("No grv")    

        if "ts" in data:
            scripts.ts_script.funcio_ts (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data)
        else:
            print ("No ts")
            
        if "sbe" in data:
            scripts.sbe_script.funcio_sbe (cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No sbe")
        if "adcp" in data:
            scripts.adcp.funcio_adcp (cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No adcp")

        if "ffe" in data:
            scripts.ffe.funcio_ffe (cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No ffe")   

        if "mag" in data:
            scripts.mag.funcio_mag (cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No mag")
        if "mbe" in data:
            scripts.mbe.funcio_mbe(cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No mbe")

        if "mcs" in data:
            scripts.mcs.funcio_mcs(cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No mcs") 

        if "sss" in data:
            scripts.sss.funcio_sss (cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No sss")

        if "srs" in data:
            scripts.srs.funcio_srs(cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No srs")

        if "sbp" in data:
            scripts.sbp.funcio_sbp(cruise_id, cruise_name, date_inicial, date_final, vessel_input,data)
        else: 
            print ("No sbp")
        
        underway_general =cruise_id + "_underway.xml"

        if path.exists(underway_general):
            remove(underway_general)

tareas_cdi = []
@app.route('/guardar_tareas', methods=['POST'])
def guardar_tareas():
    global tareas_cdi
    nuevo_valor_tareas_cdi = request.json.get('tareas_cdi')
    tareas_cdi = nuevo_valor_tareas_cdi
    #print("tareas_cdi actualizado:", tareas_cdi)
    return jsonify({"success": True})

valor_org =[] #crec que es innecesaria aquesta funcio: revisar he borrat la funcio obtenervalor de org

@app.route('/download_file', methods=['POST', 'GET'])
def download_file():
    if request.method == "POST" or request.method == "GET":
        global tareas_cdi
        global valor_org
        cruise_id = request.values.get('cruise_id')
        print (cruise_id)
        csr_code = request.values.get("cdSelect")
        print(csr_code)

        url_org = request.values.get("organizacion")
        print( url_org)
        
        cruise_name = request.values.get("cruise_name")
        date_inicial_input = request.values.get("date_inicial")
        print(date_inicial_input)
        año, mes, dia = date_inicial_input.split("-")
        date_inicial= "{}/{}/{} 00:00:00".format(dia, mes, año)
        print (date_inicial)

        date_final_input = request.values.get("date_final")
        año, mes, dia = date_final_input.split("-")
        date_final= "{}/{}/{} 00:00:00".format(dia, mes, año)
        print (date_final)
        
        vessel_input = request.values.get("vessel_input")

        if vessel_input == "sdg":
            vessel_reduit='sdg' 
        elif vessel_input == "hes":
            vessel_reduit="hes"
        url_bbox = "http://datahub.utm.csic.es/ws/getBBox/?id="+vessel_reduit + cruise_id[4:12]
        r = requests.get(url_bbox)
        
        valor_org= url_org

        try : 
            posicio_primer_espai= r.text[4:-2].index(" ")

        except:
            return render_template('error.html', url_bbox=url_bbox, cruise_id= cruise_id)
        
        data = tareas_cdi
        
        print(tareas_cdi)
        #if tareas_cdi == [] or None or "":
            #return render_template('error_variables.html')
            #return "no variables"
        if valor_org == []:
            return render_template ("error_org.html")
        else:
            grabar_underway(cruise_id, cruise_name, date_inicial, date_final, vessel_input, data, valor_org, csr_code)
            # Path to the folder to be compressed
            source_folder = os.path.abspath(cruise_id)
            zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
            
            if path.exists(zip_filename):
                remove(zip_filename)
        
            # Compress the folder into a ZIP file
            zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
            shutil.make_archive(zip_filename[:-4], 'zip', source_folder)

            #Delete the original folder from portfo folder
            shutil.rmtree(source_folder)

        return render_template('service.html', cruise_id=cruise_id)


def save_json_to_file(json_data, filename):
    
    directory = 'static/csv'
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # If the file exists, replace it
        mode = 'w'
    else:
        # If the file does not exist, create a new file
        mode = 'x'

    # Write JSON data to file
    with open(file_path, mode) as file:
        json.dump(json_data, file)



@app.route('/upload_json', methods=['POST'])
def upload_json():
    if request.method == 'POST': 
        json_data = request.get_json()  # Get JSON data from the request body
        filename = 'uploaded_data.json'
        directory = 'static/csv'
        
        save_json_to_file(json_data, filename)
        logging.info('JSON data saved successfully')
        data = json.loads(json_data)
        name=datetime.now() 
        print (name)
        name= str(name)
        name= name.replace(":", "").replace("-", "").replace(" ", "").replace(".", "")
        print (name)
        name_csv = name + ".csv"
        logging.info(f'name_csv: {name_csv}')
        print(name_csv)
        file_path = os.path.join(directory, name + ".csv") 
        # Creación del DataFrame
        df = pd.DataFrame(data)

        # Renombrar las columnas
        df.columns = ['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time', 'Instrument', 'Coments']
        print (df)
        
        df.to_csv(file_path, header=True, index=False)

        logging.info('CSV data saved successfully')
        # Return a response indicating success
        return jsonify({'message': 'JSON data saved successfully',"file_path" : file_path})

def grabar_individual (cruise_id, cruise_name, vessel_input,valor_org, csr_code, selects, ruta_csv,date_inicial, date_final):
        print("select de grabar_ind", selects)
        print("ruta_csv inside grabar_individual:", ruta_csv)  # Add this print statement to check the value of ruta_csv

        scripts.generalweb.general(cruise_id, cruise_name,  vessel_input, valor_org, csr_code,ruta_csv,selects,date_inicial, date_final)

        if "XBT" in selects:
            scripts.xbt.funcio_xbt (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" xbt")
        else:
            print("no hi ha select de XBT")

        if "CTD" in selects:
            scripts.ctd.funcio_ctd (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" ctd")
        else:
            print("no hi ha select de CTD")

        if "CTD_ROS" in selects:
            scripts.ctd_ros.funcio_ctd_ros (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" ctd_ros")
        else:
            print("no hi ha select de CTD_ROS")   

        if "CTD_ROS_LADCP" in selects:
            scripts.ctd_ros_ladcp.funcio_ctd_ros_ladcp (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" ctd_ros_ladcp")
        else:
            print("no hi ha select de CTD_ROS_LADCP")  
                     
        if "DRE" in selects:
            scripts.dre.funcio_dre (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" dre")
        else:
            print("no hi ha select de DRE")
        

        if "SVP" in selects:
            scripts.svp.funcio_svp (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" svp")
        else:
            print("no hi ha select de SVP")
        
        if "XSV" in selects:
            scripts.xsv.funcio_xsv (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" xsv")
        else:
            print("no hi ha select de XSV")
        
        if "TRA" in selects:
            scripts.tra.funcio_tra (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" tra")
        else:
            print("no hi ha select de TRA")
        
        if "MOC" in selects:
            scripts.moc.funcio_moc (cruise_id, cruise_name, vessel_input,ruta_csv,date_inicial, date_final)
            print(" moc")
        else:
            print("no hi ha select de MOC")

        if "ADCP" in selects:
            
            scripts.globalweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.adcp.funcio_adcp (cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No adcp")

        if "ffe" in selects:
            scripts.ffe.funcio_ffe (cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No ffe")   

        if "mag" in selects:
            scripts.mag.funcio_mag (cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mag")
        if "mbe" in selects:
            scripts.mbe.funcio_mbe(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mbe")

        if "mcs" in selects:
            scripts.mcs.funcio_mcs(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mcs") 

        if "sss" in selects:
            scripts.sss.funcio_sss (cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No sss")

        if "srs" in selects:
            scripts.srs.funcio_srs(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No srs")

        if "sbp" in selects:
            scripts.sbp.funcio_sbp(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No sbp")
        


        cdi_general =cruise_id + "_general.xml"
        if path.exists(cdi_general):
            remove(cdi_general)  


@app.route('/download_step1', methods=['POST', 'GET'])
def download_step1():
    filename = None  # Set a default value for the filename
    ruta_csv = None
    if request.method == 'POST':
        # Retrieve name_csv from server logs
        log_file = './record.log'
        with open(log_file, 'r') as file:
            log_content = file.read()
            match = re.findall(r'name_csv:\s*(\d+\.csv)', log_content)
            if match:
                filename = match[-1] #Get the last ruta_csv value
            else:
                # Handle case where name_csv is not found in logs
                return "Error: name_csv not found in logs"

        if filename is not None:
            try:
                ruta_csv = f"http://datahub.utm.csic.es/cdigen/static/csv/{filename}"
                print("ruta_csv:", ruta_csv)
            except Exception as e:
                print("Error constructing ruta_csv:", e)
        else:
            print("Filename is None. Unable to construct ruta_csv.")
            # Handle case where filename is None

        cruise_id = request.values.get('cruise_id')
        print (cruise_id)
        csr_code = request.values.get("cdSelect")
        print(csr_code)
        url_org = request.values.get("organizacion")
        print( url_org)
        vessel_input = request.values.get("vessel_input")
        cruise_name = request.values.get("cruise_name")
        valor_org= url_org
        #contadorselects = request.values.get("lbResultado")
        #print ("contador selects:", contadorselects)

        if vessel_input == "sdg":
            vessel_reduit='sdg' 
        elif vessel_input == "hes": 
            vessel_reduit="hes"

        date_inicial_input = request.values.get("date_inicial")
        print(date_inicial_input)
        año, mes, dia = date_inicial_input.split("-")
        date_inicial= "{}/{}/{} 00:00:00".format(dia, mes, año)
        print (date_inicial)

        date_final_input = request.values.get("date_final")
        año, mes, dia = date_final_input.split("-")
        date_final= "{}/{}/{} 00:00:00".format(dia, mes, año)
        print (date_final)
        contadorselects = 10 #el contadorselects hauria de ser el numero maxims de tipus de cdis que podem generar

        selects = []
        for i in range(contadorselects):
            select_value = request.values.get('select-' + str(i))
            selects.append(select_value)

        print("Valores de selects:", selects)
        grabar_individual (cruise_id, cruise_name, vessel_input,valor_org, csr_code, selects, ruta_csv,date_inicial, date_final)

        source_folder = os.path.abspath(cruise_id)
        zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
        
        if path.exists(zip_filename):
            remove(zip_filename)
    
        # Compress the folder into a ZIP file
        zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
        print(zip_filename)
        shutil.make_archive(zip_filename[:-4], 'zip', source_folder)

        #Delete the original folder from portfo folder
        shutil.rmtree(source_folder)

        return render_template('service.html', cruise_id=cruise_id)

@app.route('/descargar/<cruise_id>')
def descarga(cruise_id):
    # Path to the ZIP file to be downloaded
    ruta_zip = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
    response=  send_file(ruta_zip, mimetype='application/zip', as_attachment=True)
    return response

@app.route('/fetch_csr_code_list', methods=['GET'])
def fetch_csr_code_list():
    fetch_and_save_csr_code_list()
    return "CSR code list fetch updated successfully."

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
