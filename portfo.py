from flask import Flask, render_template, url_for, request, redirect, jsonify ,send_file, Response, send_from_directory, send_file
from flask_cors import CORS
from flask import session
#Define static route to flask into the folder static
app = Flask(__name__, static_url_path='/static')
#app.config['APPLICATION_ROOT'] = '/cdigen'
CORS(app, resources={r"/*": {"origins": "https://datahub.utm.csic.es"}})
import csv
import cgi
import pandas as pd
import os
from os import path, remove
from datetime import datetime,timedelta
import scripts.underwayweb,scripts.met_script, scripts.ts_script, scripts.sbe_script, scripts.generalweb, scripts.xbt ,scripts.adcp, scripts.ffe ,scripts.mbe, scripts.mcs, scripts.mag, scripts.sss, scripts.srs, scripts.sbp, scripts.net, scripts.cor
import scripts.ctd, scripts.dre , scripts.ctd_ros, scripts.xsv , scripts.svp, scripts.ctd_ros_ladcp, scripts.grv, scripts.tra, scripts.moc, scripts.globalweb, scripts.ctd_und, scripts.obs, scripts.rov, scripts.auv, scripts.msc, scripts.isp, scripts.moo,scripts.pies
import csrcodelist
import requests
import shutil
import logging
from shutil import make_archive,copy
import zipfile, tempfile
import json, re
import glob
from urllib import request as url_request
import subprocess
from logging.handlers import RotatingFileHandler

#Route from flask to serve static files
# Define the directory to save the generated zip file
ZIP_FOLDER = os.path.join(app.static_folder, 'tareas')
ruta_csv = ""

# Configure logging with more robust setup
def setup_logging():
    try:
        # Get the absolute path to the directory containing the script
        base_dir = os.path.abspath(os.path.dirname(__file__))
        log_file_path = os.path.join(base_dir, 'record.log')
        
        # Create a logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create handlers
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10000000,  # 10MB
            backupCount=5
        )
        console_handler = logging.StreamHandler()
        
        # Create formatters and add it to handlers
        log_format = '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(file_formatter)
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Log initial messages
        logging.info("Logging setup completed")
        logging.info(f"Log file path: {log_file_path}")
        
        # Ensure the CSV directory exists
        csv_dir = os.path.join(base_dir, 'static', 'csv')
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
            logging.info(f"Created CSV directory: {csv_dir}")
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        raise

# Call the setup function
setup_logging()

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

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route(
    '/<string:page_name>')  # Fent això enlloc d'haver de copiar tants fx per pàgines que tinguem agafarà el page_name i el mostrarà!
def html_page(page_name):
    return render_template(page_name)

#Starting the metadata generation process for the underway variables:
def grabar_underway (cruise_id, cruise_name, date_inicial, date_final, vessel_input, data,valor_org, csr_code):
        input_url='https://datahub.utm.csic.es/ws/getTrack/GML/?id='+ vessel_input+ cruise_id[4:12]+'&n=999'
        scripts.underwayweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, data, valor_org, csr_code)
        print(data)

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

        
        underway_general = cruise_id + "_underway.xml"

        if path.exists(underway_general):
            remove(underway_general)

tareas_cdi = []
@app.route('/guardar_tareas', methods=['POST'])
def guardar_tareas():
    try:
        nuevo_valor_tareas_cdi = request.json.get('tareas_cdi')
        if not nuevo_valor_tareas_cdi:
            return jsonify({"error": "tareas_cdi is required"}), 400

        # Save to a file
        with open('tareas_cdi.json', 'w') as file:
            json.dump(nuevo_valor_tareas_cdi, file)

        print("tareas_cdi actualizado:", nuevo_valor_tareas_cdi)
        return jsonify({"success": True})
    except Exception as e:
        logging.error(f"Error in guardar_tareas: {str(e)}")
        return jsonify({"error": str(e)}), 500

#valor_org =[] #crec que es innecesaria aquesta funcio: revisar he borrat la funcio obtener valor de org
@app.route('/download_file', methods=['POST', 'GET'])
def download_file():
    try:
        # Load tareas_cdi from the file
        try:
            with open('tareas_cdi.json', 'r') as file:
                tareas_cdi = json.load(file)
        except FileNotFoundError:
            tareas_cdi = []

        print(f"tareas_cdi in /download_file: {tareas_cdi}")

        if not tareas_cdi:
            return jsonify({"error": "No tasks selected in tareas_cdi"}), 400

        cruise_id = request.values.get('cruise_id')
        print(cruise_id)
        csr_code = request.values.get("cdSelect")
        print(csr_code)

        url_org = request.values.get("organizacion")
        if not url_org:
            return jsonify({"error": "organization is required"}), 400
            
        print(url_org)
        
        cruise_name = request.values.get("cruise_name")
        if not cruise_name:
            return jsonify({"error": "cruise_name is required"}), 400
            
        date_inicial_input = request.values.get("date_inicial")
        if not date_inicial_input:
            return jsonify({"error": "date_inicial is required"}), 400
            
        print(date_inicial_input)
        año, mes, dia = date_inicial_input.split("-")
        date_inicial = "{}/{}/{} 00:00:00".format(dia, mes, año)
        print(date_inicial)

        date_final_input = request.values.get("date_final")
        if not date_final_input:
            return jsonify({"error": "date_final is required"}), 400
            
        año, mes, dia = date_final_input.split("-")
        date_final = "{}/{}/{} 00:00:00".format(dia, mes, año)
        print(date_final)
        
        vessel_input = request.values.get("vessel_input")
        if not vessel_input:
            return jsonify({"error": "vessel_input is required"}), 400

        if vessel_input == "sdg":
            vessel_reduit = 'sdg' 
        elif vessel_input == "hes":
            vessel_reduit = "hes"
        else:
            return jsonify({"error": "Invalid vessel_input"}), 400
            
        # Fetch the bounding box data
        url_bbox = f"https://datahub.utm.csic.es/ws/getBBox/?id={vessel_reduit}{cruise_id[4:12]}"
        r = requests.get(url_bbox)

        # Validate the response
        if r.status_code != 200 or not r.text.strip():
            return jsonify({"error": f"Failed to fetch bounding box data from {url_bbox}. Response: {r.text}"}), 400

        coord = r.text[4:-2].strip()  # Extract the coordinates, removing the first 4 and last 2 characters
        if not coord or " " not in coord or "," not in coord:
            return jsonify({"error": f"Invalid bounding box format in response: {r.text}"}), 400

        try:
            # Parse the coordinates
            posicio_primer_espai = coord.index(" ")
            posicio_coma = coord.index(",")
            w = coord[0:posicio_primer_espai]
            s = coord[posicio_primer_espai:posicio_coma].strip()
            coord_2 = coord[posicio_coma + 1:]
            posicio_segon_espai = coord_2.index(" ")
            e = coord_2[0:posicio_segon_espai].strip()
            n = coord_2[posicio_segon_espai:].strip()
        except ValueError as e:
            return jsonify({"error": f"Error parsing bounding box coordinates: {str(e)}. Response: {r.text}"}), 400

        # Log the parsed coordinates for debugging
        logging.info(f"Parsed bounding box coordinates: W={w}, S={s}, E={e}, N={n}")
        
        valor_org = url_org

        try:
            posicio_primer_espai = r.text[4:-2].index(" ")
        except:
            return render_template('error.html', url_bbox=url_bbox, cruise_id=cruise_id)
        
        data = tareas_cdi
        print(tareas_cdi)
        
        if not valor_org:
            return render_template("error_org.html")
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
    except Exception as e:
        logging.error(f"Error in download_file: {str(e)}")
        return jsonify({"error": str(e)}), 500

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
        print(data)
        name=datetime.now() 
        print (name)
        name= str(name)
        name= name.replace(":", "").replace("-", "").replace(" ", "").replace(".", "")
        print (name)    
        name_csv = name + ".csv"
        logging.info(f'name_csv: {name_csv}')

        file_path = os.path.join(directory, name + ".csv") 
        print("file path ------", file_path)
        df = pd.DataFrame(data)
        print(df)
        columns = len(df.columns)
        print("columnes---",columns)
        if columns == 6:
            df.columns=  ['First_lat', 'First_long', 'First_time', 'End_time','Instrument', 'Coments']
            df['End_lat'] = df['First_lat']
            df['End_long'] = df['First_long']
            #df['End_time'] = df['First_time']
            desired_column_order = ['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time', 'Instrument', 'Coments']

            # Reorganizar el DataFrame
            df = df[desired_column_order]
            df.to_csv(file_path, header=True, index=False)
        elif columns == 5:
            df.columns=  ['First_lat', 'First_long', 'First_time', 'Instrument', 'Coments']
            df['End_lat'] = df['First_lat']
            df['End_long'] = df['First_long']
            df['End_time'] = df['First_time']
            desired_column_order = ['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time', 'Instrument', 'Coments']

            # Reorganizar el DataFrame
            df = df[desired_column_order]
            df.to_csv(file_path, header=True, index=False)
        elif columns == 8:
            df.columns=  ['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time', 'Instrument', 'Coments']
            # Reorganizar el DataFrame
            
            df.to_csv(file_path, header=True, index=False)
        else:
            print("----------------el csv carregat del json no te ni 5 ni 6 columnes----------------")
            logging.error("el csv carregat del json no te ni 5 ni 6 ni 8 columnes")
   

        """# Create DataFrame
        df = pd.DataFrame(data)
        
        # Print the actual columns for debugging
        actual_columns = df.columns.tolist()
        logging.info(f"Actual columns in data: {actual_columns}")
        
        # Rename columns only if they match the expected structure
        expected_columns = ['First_lat', 'First_long', 'End_lat', 'End_long', 'First_time', 'End_time', 'Instrument', 'Coments']
        
        # Create a mapping of actual to expected columns
        column_mapping = {}
        for i, col in enumerate(df.columns):
            if i < len(expected_columns):
                column_mapping[col] = expected_columns[i]
        
        # Rename existing columns and add missing ones with NaN values
        df = df.rename(columns=column_mapping)
        for col in expected_columns:
            if col not in df.columns:
                df[col] = pd.NA
                logging.warning(f"Added missing column {col} with NA values")
        
        # Ensure columns are in the expected order
        df = df[expected_columns]
        
        logging.info(f"Final DataFrame columns: {df.columns.tolist()}")
        df.to_csv(file_path, header=True, index=False)"""
        
        def convert_date_format(date_str):
            if isinstance(date_str, str):
                # patrons de dates
                patterns = [
                    (r'\d{2}/\d{2}/\d{4} \d{1}:\d{2}:\d{2}', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'),
                    (r'\d{2}/\d{2}/\d{4} \d{1}:\d{2}', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M:%S'),
                    (r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'),
                    (r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', '%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M:%S'),
                    (r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}', '%d-%m-%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'),
                    (r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}', '%d-%m-%Y %H:%M', '%Y-%m-%d %H:%M:%S')
                ]
                
                for pattern, input_format, output_format in patterns:
                    if re.match(pattern, date_str):
                        try:
                            date_obj = datetime.strptime(date_str, input_format)
                            return date_obj.strftime(output_format)
                        except ValueError:
                            continue
                return date_str
            return date_str

        def process_csv(input_file, output_file):
            try:
                # Read the csv
                df = pd.read_csv(input_file)
                
                date_columns = ['First_time', 'End_time']
                
                # Apply date format conversion only to date columns that exist and have data
                for col in date_columns:
                    if col in df.columns and not df[col].isna().all():
                        df[col] = df[col].map(convert_date_format)
                
                df.to_csv(output_file, index=False)
                logging.info(f"CSV processing completed successfully for {output_file}")
            except Exception as e:
                logging.error(f"Error processing CSV: {str(e)}")
                raise

        # Process the CSV
        process_csv(file_path, file_path)

        logging.info('CSV data saved successfully')
        logging.info(f"CSV file processed and saved at: {file_path}")
        return jsonify({'message': 'JSON data saved successfully', "file_path": file_path})

def grabar_individual(cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final):
    print("date inicial:-----------------", date_inicial)
    try:
        logging.info(f"Starting grabar_individual with selects: {selects}")
        logging.info(f"ruta_csv: {ruta_csv}")

        if "XBT" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.xbt.funcio_xbt(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" xbt")
        else:
            print("no hi ha select de XBT")

        if "CTD" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.ctd.funcio_ctd(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" ctd")
        else:
            print("no hi ha select de CTD")

        if "CTD_ROS" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.ctd_ros.funcio_ctd_ros(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" ctd_ros")
        else:
            print("no hi ha select de CTD_ROS")   

        if "CTD_ROS_LADCP" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, date_inicial,ruta_csv, selects, date_final)
            scripts.ctd_ros_ladcp.funcio_ctd_ros_ladcp(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print("Acabats ctd_ros_ladcp")
        else:
            print("no hi ha select de CTD_ROS_LADCP")  

        if "CTD_UND" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.ctd_und.funcio_ctd_und(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" ctd_UND")
        else:
            print("no hi ha select de CTD_UND")  
                     
        if "DRE" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.dre.funcio_dre(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" dre")
        else:
            print("no hi ha select de DRE")
        
        if "SVP" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.svp.funcio_svp(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" svp")
        else:
            print("no hi ha select de SVP")
        
        if "XSV" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.xsv.funcio_xsv(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" xsv")
        else:
            print("no hi ha select de XSV")
        
        if "TRA" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.tra.funcio_tra(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" tra")
        else:
            print("no hi ha select de TRA")
        
        if "MOC" in selects:
            scripts.generalweb.general(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.moc.funcio_moc(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" moc")
        else:
            print("no hi ha select de MOC")

        if "OBS" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.obs.funcio_obs(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print("obs")
        else:
            print("no hi ha select de OBS")

        if "ROV" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.rov.funcio_rov(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
        else: 
            print ("No rov")    

        if "ISP" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.isp.funcio_isp(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
        else: 
            print ("No isp")

        if "MSC" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.msc.funcio_msc(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
        else: 
            print ("No msc")

        if "NET" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.net.funcio_net(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
        else: 
            print ("No net")

        if "COR" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.cor.funcio_cor(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
        else: 
            print ("No cor")

        if "MOO" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.moo.funcio_moo(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" MOO")
        else:
            print("no hi ha select de MOO") 

        if "PIES" in selects:
            scripts.generalweb.general_sense_sensor(cruise_id, cruise_name, vessel_input, valor_org, csr_code, ruta_csv, selects, date_inicial, date_final)
            scripts.pies.funcio_pies(cruise_id, cruise_name, vessel_input, ruta_csv, date_inicial, date_final)
            print(" Hi ha PIES")
        else:
            print("no PIES")                  
        if "ADCP" in selects:
            scripts.globalweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.adcp.funcio_adcp(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No adcp")

        if "FFE" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.ffe.funcio_ffe(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No ffe")   

        if "MAG" in selects:
            scripts.globalweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.mag.funcio_mag(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mag")

        if "MBE" in selects:
            scripts.globalweb.underway_general(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.mbe.funcio_mbe(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mbe")

        if "MCS" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.mcs.funcio_mcs(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No mcs") 

        if "SSS" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.sss.funcio_sss(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No sss")

        if "SRS" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.srs.funcio_srs(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No srs")

        if "SBP" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.sbp.funcio_sbp(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No sbp")

        if "AUV" in selects:
            scripts.globalweb.underway_general_sense_sensor(cruise_id, cruise_name, date_inicial, date_final, vessel_input, valor_org, csr_code)
            scripts.auv.funcio_auv(cruise_id, cruise_name, date_inicial, date_final, vessel_input)
        else: 
            print ("No auv")          

        cdi_general = cruise_id + "_general.xml"
        if path.exists(cdi_general):
            remove(cdi_general)  

    except Exception as e:
        logging.error(f"Error in grabar_individual: {str(e)}")
        raise

@app.route('/download_step1', methods=['POST', 'GET'])
def download_step1():
    try:
        filename = None
        ruta_csv = None
        
        if request.method == 'POST':
            # Retrieve name_csv from server logs
            log_file = 'record.log'
            try:
                with open(log_file, 'r') as file:
                    log_content = file.read()
                    match = re.findall(r'name_csv:\s*(\d+\.csv)', log_content)
                    if match:
                        filename = match[-1]  # Get the last name_csv value
                        logging.info(f"Found filename in logs: {filename}")
                    else:
                        logging.error("No name_csv found in logs")
                        return jsonify({"error": "No CSV file found in logs"}), 400
            except Exception as e:
                logging.error(f"Error reading log file: {str(e)}")
                return jsonify({"error": "Error reading log file"}), 500

            if filename is not None:
                try:
                    ruta_csv = f"https://datahub.utm.csic.es/cdigen/static/csv/{filename}"
                    logging.info(f"Constructed ruta_csv: {ruta_csv}")
                except Exception as e:
                    logging.error(f"Error constructing ruta_csv: {str(e)}")
                    return jsonify({"error": "Error constructing file path"}), 500
            else:
                logging.error("Filename is None. Unable to construct ruta_csv.")
                return jsonify({"error": "No filename available"}), 400

            cruise_id = request.values.get('cruise_id')
            if not cruise_id:
                return jsonify({"error": "cruise_id is required"}), 400
                
            csr_code = request.values.get("cdSelect")
            if not csr_code:
                return jsonify({"error": "csr_code is required"}), 400
                
            url_org = request.values.get("organizacion")
            if not url_org:
                return jsonify({"error": "organization is required"}), 400
                
            vessel_input = request.values.get("vessel_input")
            if not vessel_input:
                return jsonify({"error": "vessel_input is required"}), 400
                
            cruise_name = request.values.get("cruise_name")
            if not cruise_name:
                return jsonify({"error": "cruise_name is required"}), 400
                
            valor_org = url_org

            if vessel_input == "sdg":
                vessel_reduit = 'sdg' 
            elif vessel_input == "hes": 
                vessel_reduit = "hes"
            else:
                return jsonify({"error": "Invalid vessel_input"}), 400

            date_inicial_input = request.values.get("date_inicial")
            if not date_inicial_input:
                return jsonify({"error": "date_inicial is required"}), 400
                
            año, mes, dia = date_inicial_input.split("-")
            date_inicial = "{}/{}/{} 00:00:00".format(dia, mes, año)

            date_final_input = request.values.get("date_final")
            if not date_final_input:
                return jsonify({"error": "date_final is required"}), 400
                
            año, mes, dia = date_final_input.split("-")
            date_final = "{}/{}/{} 00:00:00".format(dia, mes, año)

            contadorselects = 10  # Maximum number of CDI types that can be generated

            selects = []
            for i in range(contadorselects):
                select_value = request.values.get('select-' + str(i))
                if select_value:
                    selects.append(select_value)

            if not selects:
                return jsonify({"error": "No instrument types selected"}), 400

            logging.info(f"Processing with selects: {selects}")
            grabar_individual(cruise_id, cruise_name, vessel_input, valor_org, csr_code, selects, ruta_csv, date_inicial, date_final)

            source_folder = os.path.abspath(cruise_id)
            zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
            
            if path.exists(zip_filename):
                remove(zip_filename)
        
            # Compress the folder into a ZIP file
            zip_filename = os.path.join(ZIP_FOLDER, f'{cruise_id}.zip')
            logging.info(f"Creating zip file: {zip_filename}")
            shutil.make_archive(zip_filename[:-4], 'zip', source_folder)

            # Delete the original folder from portfo folder
            shutil.rmtree(source_folder)

            return render_template('service.html', cruise_id=cruise_id)
            
    except Exception as e:
        logging.error(f"Error in download_step1: {str(e)}")
        return jsonify({"error": str(e)}), 500

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

@app.route('/fetch_sparql_results', methods=['GET'])
def fetch_sparql_results():
    csrcodelist.fetch_and_save_sparql_results()
    return "Organization list fetch updated successfully."

@app.route('/download_data', methods=['POST', 'GET'])
def download_data():
    if request.method == "POST" or request.method == "GET":
        date_inicial_input = request.values.get("date_inicial")
        año, mes, dia = date_inicial_input.split("-")
        date_inicial = "{}/{}/{} 00:00:00".format(dia, mes, año)

        date_final_input = request.values.get("date_final")
        año, mes, dia = date_final_input.split("-")
        date_final = "{}/{}/{} 00:00:00".format(dia, mes, año)

        vessel_input = request.values.get("vessel_input")
        ejecutar = 'ejecutar' in request.form

        if ejecutar:
            try:
                # Ejecutamos el script para generar los archivos
                result = subprocess.run(
                    ['python3', '3_fitxers.py', vessel_input, date_inicial, date_final],
                    check=True,  # Esto lanzará una excepción si el script no se ejecuta correctamente
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                return render_template('data.html',download_success=True)


            except Exception as e:
                print(f"Ocurrió un error al ejecutar el script: {str(e)}")
                print({"error": "Hubo un error al ejecutar el script."})
                return render_template('data.html', download_success=False)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
