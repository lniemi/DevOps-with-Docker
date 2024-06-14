import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '../components/Home';  // Updated path
// Import the other components if they exist, like About and NotFound
// import About from '../components/About';
//import NotFound from '../components/NotFound';
import NotFound from '../components/NotFound'; // Correct the path as necessary

const Router = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      {/* Uncomment or update the following routes as needed */}
      {/* <Route path="/about" element={<About />} /> */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  </BrowserRouter>
);

export default Router;
