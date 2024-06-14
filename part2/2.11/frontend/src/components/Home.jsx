import React from 'react';
import Homemap from './Homemap';  // Ensure correct relative path
import GeoJsonuploader from './GeoJsonUploader';  // Ensure correct relative path
import BBGRefresher from './BBGRefresher';  // Ensure correct relative path

const Home = () => {
  return (
    <div>
      <h1>Home</h1>
      <Homemap />  // This will render the map on the Home page
      <GeoJsonuploader />  // This will render the GeoJsonuploader on the Home page
      <BBGRefresher /> // This will render the BBGrefresher on the Home page
    </div>
  );
};

export default Home;
