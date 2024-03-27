CDIgen Flask Application
CDIgen is a Flask web application designed to facilitate the generation and submission of oceanographic metadata in compliance with SeaDataNet (SDN) standards. The application allows users to create Common Data Index (CDI) files for oceanographic cruises, enabling efficient data management and sharing within the community.

This web application will continue to evolve and be improved over time. Although currently tailored to UTM Data Centre, our ultimate objective is to create a fully customizable CDI generator. This would enable Data Centers worldwide utilizing SDN standardized vocabularies to customize, create, and download their CDIs, thereby simplifying the submission process to the SeaDataNet CDI catalog. Our aim is to foster community engagement and facilitate participation in the SDN community by offering an intuitive, user-friendly approach.

Features
Metadata Generation: CDIgen provides a user-friendly interface for creating CDI files by inputting cruise details and selecting relevant data parameters.
Automatic CSR Code List Update: The application automatically fetches and updates the CSR code list XML file from the SeaDataNet website, ensuring compliance with the latest standards.
Data Processing: CDIgen processes user inputs and generates CDI files for various data types, including underway, meteorological, temperature-salinity, and others.
Downloadable Metadata: Once generated, users can download the CDI files as ZIP archives for submission to the SeaDataNet catalog.
Usage
Installation: Clone the CDIgen repository to your local machine and install the required dependencies using pip install -r requirements.txt.

Running the Application: Launch the Flask application by running python portfo.py in the terminal. The application will start running on http://localhost:5000.

Accessing the Web Interface: Open a web browser and navigate to http://localhost:5000 to access the CDIgen web interface.

Generating Metadata: Enter cruise details, select data parameters, and submit the form to generate CDI files for the specified cruise.

Downloading Metadata: After generation, CDI files can be downloaded as ZIP archives for submission to SeaDataNet.

Contributing
Contributions to CDIgen are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the GitHub repository.

License
This project is licensed under the MIT License - see the LICENSE file for details.
