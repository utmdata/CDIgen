# CDIgen Flask Application

CDIgen is a Flask web application designed to facilitate the generation and submission of oceanographic metadata in compliance with SeaDataNet (SDN) standards. The application allows users to create Common Data Index (CDI) files for oceanographic cruises, enabling efficient data management and sharing within the community.

This web application will continue to evolve and be improved over time. Although currently tailored to UTM Data Centre, our ultimate objective is to create a fully customizable CDI generator. This would enable Data Centers worldwide utilizing SDN standardized vocabularies to customize, create, and download their CDIs, thereby simplifying the submission process to the SeaDataNet CDI catalog. Our aim is to foster community engagement and facilitate participation in the SDN community by offering an intuitive, user-friendly approach.

## Features

- **Metadata Generation**: CDIgen provides a user-friendly interface for creating CDI files by inputting cruise details and selecting relevant data parameters.
  
- **Automatic CSR Code List Update**: The application automatically fetches and updates the CSR code list XML file from the SeaDataNet website, ensuring compliance with the latest standards.
  
- **Data Processing**: CDIgen processes user inputs and generates CDI files for various data types, including underway, meteorological, temperature-salinity, and others.
  
- **Downloadable Metadata**: Once generated, users can download the CDI files as ZIP archives for submission to the SeaDataNet catalog.

## Usage

### Installation

1. Clone the CDIgen repository to your local machine.
   ```bash
   git clone https://github.com/utmdata/CDIgen.git
   ```

2. Navigate to the CDIgen directory.
   ```bash
   cd CDIgen
   ```

3. Install the required dependencies using pip.
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Launch the Flask application by running the following command in the terminal.
   ```bash
   python portfo.py
   ```

2. The application will start running on http://localhost:5000.

### Accessing the Web Interface

1. Open a web browser and navigate to http://localhost:5000 to access the CDIgen web interface.

### Generating Metadata

1. Enter cruise details, select data parameters, and submit the form to generate CDI files for the specified cruise.

### Downloading Metadata

1. After generation, CDI files can be downloaded as ZIP archives for submission to SeaDataNet.

## Contributing

Contributions to CDIgen are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/utmdata/CDIgen).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
