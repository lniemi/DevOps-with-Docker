import json
import os
from django.http import JsonResponse
from django.db import connection
import django.views.decorators.csrf
from django.contrib.gis.geos import GEOSGeometry
from .models import UserGeoData
from .models import BlackBirdGroup
from django.views.decorators.csrf import csrf_exempt
import subprocess
from django.utils import timezone
from time import sleep
import random
import string

### Here starts the data fetching FROM the database ###
# This is a very basic test to see if the API is working
def ua_frontlines_geojson(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(geom)::json,
                        'properties', json_build_object(
                            'id', id,
                            'name', name,
                            'description', description
                        )
                    )
                )
            ) FROM ua_frontlines;
        """)
        geojson = cursor.fetchone()[0]  # fetchone returns a tuple, [0] gets the JSON from the tuple

    return JsonResponse(geojson, safe=False)  # `safe=False` is required to allow top-level arrays

# This query fetches the latest data from the BlackBirdGroup table and
# defines latest as as the layers with the most recent date and time and decides that
# all those layers must be returned that are added to the database at the timeframe of varying
# max 5 minutes.
def blackbird_group_geojson(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH AggregatedData AS (
                SELECT
                    ST_Union(geom) AS unified_geom,  -- Combine all geometries into one
                    string_agg(CAST(layer_id AS TEXT), ', ') AS aggregated_ids,  -- Aggregate all layer IDs
                    string_agg(CAST(category_id AS TEXT), ', ') AS aggregated_category_ids,  -- Aggregate all category IDs
                    string_agg(layer_name, '; ') AS aggregated_names,  -- Concatenate all layer names
                    MAX(date) AS latest_date,  -- Get the maximum date
                    string_agg(description, ' | ') AS aggregated_descriptions  -- Concatenate all descriptions
                FROM django_api_blackbirdgroup
                WHERE date >= (SELECT MAX(date) - INTERVAL '5 minutes' FROM django_api_blackbirdgroup)  -- Condition to filter data
            )
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(unified_geom)::json,  -- Convert unified geometry to GeoJSON
                        'properties', json_build_object(
                            'id', aggregated_ids,
                            'category_id', aggregated_category_ids,  -- Use the correct variable name here
                            'name', aggregated_names,
                            'date', latest_date,  -- Correct variable name for the latest date
                            'description', aggregated_descriptions
                        )
                    )
                )
            ) FROM AggregatedData;
        """)
        result = cursor.fetchone()[0]

    return JsonResponse(result, safe=False)


    return JsonResponse(result, safe=False)



### Here starts the data uploading TO the database ###

# User can upload OWN GeoJSON file
@csrf_exempt
def upload_geojson(request):
    if request.method == 'POST':
        geojson_file = request.FILES.get('file')
        geojson_data = json.load(geojson_file)

        features = geojson_data.get('features', [])
        for feature in features:
            geom = GEOSGeometry(json.dumps(feature['geometry']))
            properties = feature['properties']
            UserGeoData.objects.create(
                name=properties.get('name'),
                description=properties.get('description'),
                geom=geom
            )

        return JsonResponse({'status': 'success', 'message': 'Data uploaded successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# Fetch and upload data from the BlackBirdGroup
@csrf_exempt
def fetch_and_upload_bbg_data(request):
    # Specify the full path to the wrapper.py script within the Docker container
    wrapper_script_path = '/app/django_api/wrapper.py'

    # Execute the wrapper script to generate the GeoJSON file
    try:
        subprocess.run(["python", wrapper_script_path], timeout=30)
    except subprocess.TimeoutExpired:
        return JsonResponse({'status': 'error', 'message': 'Script execution timed out'}, status=408)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # Assuming the GeoJSON files start with 'Extracted' and are in the same directory
    directory = '/app'
    geojson_files = [f for f in os.listdir(directory) if f.startswith('Extracted') and f.endswith('.geojson')]

    if not geojson_files:
        return JsonResponse({'status': 'error', 'message': 'No GeoJSON file found'}, status=404)

    # Assuming there's only one file, or taking the first file found
    geojson_path = os.path.join(directory, geojson_files[0])

    # Read and parse the GeoJSON file
    with open(geojson_path, 'r') as file:
        geojson_data = json.load(file)

    # Upload each feature to the database
    for feature in geojson_data.get('features', []):
        geom = GEOSGeometry(json.dumps(feature['geometry']))
        properties = feature['properties']
        random_number = ''.join(random.choices(string.digits, k=8))

        BlackBirdGroup.objects.create(
            layer_id=properties.get('id', random_number),
            category_id=properties.get('category_id', 1),
            layer_name=os.path.splitext(os.path.basename(geojson_path))[0],
            date=timezone.now(),
            description="Russian occupied area",
            geom=geom
        )

    # Optional: Clean up the GeoJSON file after uploading its data
    os.remove(geojson_path)

    return JsonResponse({'status': 'success', 'message': f'Data from {geojson_path} uploaded successfully.'})