# Rintama

So this project and synergies it has basically is the biggest reason I wanted to learn docker and docker-compose. I wanted to learn how to deploy a full stack geospatial application without having to worry about the dependencies and the environment which is a pain in the ass with some of the needed libraries if you have them already installed them separately and on a bigger scale on the main host machine. Good example of such library is GDAL and for the sake of having QGIS Desktop installed on my machine it required previously quite much path and environment configuring.

## Introduction

This is a small project to demonstrate the use of Geodjango, PostGIS, QGIS Server (NOT YET INTEGRATED) and GDAL.
The idea is to fetch from popular Ukraine OSINT maps the latest frontline information. So far the only fully working "wrapper" is done for fetching data from "The War in Ukraine" Scribble Maps project updated by Finnish OSINT collective Black Bird Group. In the future there might be other OSINT map api's that will be used as well. Some well known OSINT maps have public api's or databases where to look from for the latest information.

## Installation & requirements

Only requirement: Docker installed

setting the service running:

run docker-compose up at the root direcory

There is one basemap that needs to have mapbox access token. This can be obtained from mapbox.com. The token is added to the frontend/.env file or simply added to the Homemap.jsx file in the frontend/src/components directory.

# Development

Currently I have set the development so that when changes are being made to the code on backend or frontend and being saved, the changes occure immediately. In proudction mode (maybe in the future) backend and frontend configurations must be changed.

I must however note that even though changes occur immediately in the docker container when files are saved on the backend, the same does yet not work with frontend. There is a temporary solution to this, but it is not the best one. The solution is to disable (commenting out) frontend build in the docker-compose up command. This is done by adding a # in front of the frontend build command. This is not the best solution, but it works for now and the frontend runs simply outside the container by running npm run dev in the frontend directory. 