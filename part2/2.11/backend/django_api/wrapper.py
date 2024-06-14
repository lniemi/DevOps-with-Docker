import requests
import datetime
from osgeo import ogr, osr
import os
import json
import re
from dateutil.parser import parse

# URL to download the KML
url = "https://www.scribblemaps.com/api/maps/091194/kml"

# Set today's date in the format used in your layer names
today_date = datetime.datetime.now().strftime('%d.%m.%y')

# Function to extract date from the layer name
def extract_date(layer_name):
    date_pattern = r'\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})\b'
    match = re.search(date_pattern, layer_name)
    if match:
        try:
            return parse(match.group(1), dayfirst=True)
        except ValueError:
            return None
    return None


# Function to download KML from the given URL
def download_kml(url, filename='downloaded.kml'):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
            print("File downloaded successfully.")
        return filename
    else:
        print("Failed to download the file.")
        return None

# Function to write layer to specified format (KML or GeoJSON)
def write_layer(layer, file_name, format):
    if format == 'kml':
        driver = ogr.GetDriverByName('KML')
    elif format == 'geojson':
        driver = ogr.GetDriverByName('GeoJSON')
    else:
        print("Unsupported format")
        return

    if os.path.exists(file_name):
        driver.DeleteDataSource(file_name)  # If the file exists, delete it

    out_data_source = driver.CreateDataSource(file_name)
    out_layer = out_data_source.CreateLayer(str(layer.GetName()), geom_type=ogr.wkbUnknown)

    # Copy features from the source layer to the new layer
    for feature in layer:
        out_layer.CreateFeature(feature)

    del out_data_source  # Save and close the new file


# Download the KML file
downloaded_file = download_kml(url)


if downloaded_file:
    # Ask user for the desired output format
    print("Select the output format:")
    print("1: KML")
    print("2: GeoJSON")
    #format_choice = input("Enter your choice (1 or 2): ")
    format_choice = "2"
    format_dict = {'1': 'kml', '2': 'geojson'}
    output_format = format_dict.get(format_choice, 'kml')  # Default to KML if invalid input

    # Open the downloaded KML file using GDAL/OGR
    driver = ogr.GetDriverByName('KML')
    kml_data_source = driver.Open(downloaded_file, 0)  # 0 means read-only mode

    if kml_data_source:
        layer_count = kml_data_source.GetLayerCount()
        latest_date = None
        latest_layer = None

        for i in range(layer_count):
            layer = kml_data_source.GetLayerByIndex(i)
            layer_name = layer.GetName()
            layer_date = extract_date(layer_name)

            if layer_date:
                if not latest_date or layer_date > latest_date:
                    latest_date = layer_date
                    latest_layer = layer

        if latest_layer:
            print(f"Extracting layer: {latest_layer.GetName()}")
            output_file_name = f"Extracted_{latest_layer.GetName().replace('/', '_')}.{output_format}"
            write_layer(latest_layer, output_file_name, output_format)
            print(f"Layer saved as: {output_file_name}")
        else:
            print("No layers found with a valid date in the name.")

        del kml_data_source  # Close the data source
    else:
        print("Failed to open the downloaded KML file.")
else:
    print("Download failed or file is not accessible.")

# Clean up the downloaded file
if os.path.exists(downloaded_file):
    os.remove(downloaded_file)  # Delete the downloaded file
    print("Downloaded file cleaned up.")