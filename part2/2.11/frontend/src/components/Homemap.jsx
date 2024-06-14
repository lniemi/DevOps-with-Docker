import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, LayersControl, Polygon, LayerGroup } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import '../css/Homemap.css';
import "react-leaflet-fullscreen/styles.css";
import { FullscreenControl } from "react-leaflet-fullscreen";

function Homemap() {
    const [uaFrontlinesPoints, setUaFrontlinesPoints] = useState([]); // State for UA Frontlines points
    const [blackBirdGroupPolygons, setBlackBirdGroupPolygons] = useState([]); // State for BlackBird Group polygons
    const position = [49.8388, 35.1396]; // Default position

    useEffect(() => {
        // Fetch data from UA Frontlines API
        axios.get('http://localhost:8000/api/ua_frontlines/')
            .then(response => {
                setUaFrontlinesPoints(response.data.features);
                console.log('UA Frontlines data:', response.data);
            })
            .catch(error => console.log('Error fetching UA Frontlines data:', error));

        // Fetch polygon data from BlackBird Group API
        axios.get('http://localhost:8000/api/blackbird_group/')
            .then(response => {
                setBlackBirdGroupPolygons(response.data.features);
                console.log('BlackBird Group polygons:', response.data);
            })
            .catch(error => console.log('Error fetching BlackBird Group polygon data:', error));
    }, []);

    return (
        <MapContainer center={position} zoom={6.15} style={{ height: '70vh', width: '80%', margin: 'auto' }} zoomControl={false}>
            <LayersControl position="topright">
                <LayersControl.BaseLayer checked name="OpenStreetMap">
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="Black and White">
                    <TileLayer
                        url="http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="Cyclosm mimic">
                    <TileLayer
                        url="https://api.mapbox.com/styles/v1/lniemi/clumnjlqm002o01r552v5ej96/tiles/256/{z}/{x}/{y}@2x?access_token=REPLACE_ME_WITH_YOUR_MAPBOX_ACCESS_TOKEN"
                        attribution='&copy; <a href="https://www.mapbox.com/">Mapbox</a> contributors'
                    />
                </LayersControl.BaseLayer>
                <LayersControl.Overlay name="Railways">
                    <TileLayer
                        url="https://tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png"
                        attribution='&copy; <a href="https://www.openrailwaymap.org/">OpenRailwayMap</a> contributors'
                    />
                </LayersControl.Overlay>
                <LayersControl.Overlay checked name="UA Frontlines Markers">
                    {uaFrontlinesPoints.map(point => (
                        <Marker key={point.id} position={[point.geometry.coordinates[1], point.geometry.coordinates[0]]}>
                            <Popup>
                                {point.properties.name} - {point.properties.description}
                            </Popup>
                        </Marker>
                    ))}
                </LayersControl.Overlay>
                <LayersControl.Overlay checked name="Black Bird Group">
                    <LayerGroup>
                        {blackBirdGroupPolygons.map((feature, index) => (
                            feature.geometry.type === "Polygon" ?
                            <Polygon key={index} positions={feature.geometry.coordinates.map(ring => ring.map(coord => [coord[1], coord[0]]))} color="red">
                                <Popup>
                                    {feature.properties.name} - {feature.properties.description}
                                </Popup>
                            </Polygon> :
                            feature.geometry.type === "MultiPolygon" &&
                            feature.geometry.coordinates.map((polygon, polyIndex) => (
                                <Polygon key={`${index}-${polyIndex}`} positions={polygon.map(ring => ring.map(coord => [coord[1], coord[0]]))} color="red">
                                    <Popup>
                                        {feature.properties.name} - {feature.properties.description}
                                    </Popup>
                                </Polygon>
                            ))
                        ))}
                    </LayerGroup>
                </LayersControl.Overlay>
            </LayersControl>
            <FullscreenControl position="topleft" />
        </MapContainer>
    );
}

export default Homemap; 
