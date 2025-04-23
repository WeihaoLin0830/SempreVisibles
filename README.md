# AirQualityMap_Bits
Project developed by Sergi Flores, Clàudia Gallego, Weihao Lin and Jiahui Chen for the BitsxLaMarató Hackathon, a really special hackathon due to its charity nature. 

## Random Forest Regressor
Mapa d'alta resolució de la qualitat d'aire en Catalunya. #BitsxLaMarató 2024

Our solution focused on interpolating the points we aimed to predict using IDW (Inverse Distance Weighting) combined with the 1 km resolution data from the CALIOPE system. Next, we trained a model using air quality station data and their nearest roads to refine the results based on road-specific characteristics. Additionally, we developed a temporal model to adjust the outcomes according to the desired hour and day and created a simple website that provides air quality forecasts for the main cities in Catalonia.



# AirQualityMap: High-Resolution Air Quality Forecasting for Catalonia

![Catalonia Air Quality Map](/img/photo1.jpg)

## 🏆 BSC Challenge Winners - BitsxLaMarató Hackathon

AirQualityMap is a sophisticated air quality prediction system that downscales regional pollution data to street-level resolution across Catalonia, developed for the "Fem visible l'invisible!" challenge by Barcelona Supercomputing Center.

![Web Interface Preview](/img/photo2.jpg)

## Project Overview

AirQualityMap transforms low-resolution (1km×1km) air quality predictions from the CALIOPE system into highly detailed street-level pollution maps. By combining advanced spatial interpolation techniques with machine learning models that incorporate traffic patterns and local measurements, we provide citizens with accurate, hyper-local air quality forecasts.

## Technical Approach

### Data Sources Integration
- **CALIOPE System Data**: 1km×1km resolution NO₂ pollution predictions across Catalonia
- **XVPCA Stations**: Ground-truth air quality measurements from land monitoring stations
- **Traffic Patterns**: Road network data with traffic intensity information
- **Temporal Factors**: Historical patterns of pollution variation by hour and day

### Modeling Pipeline

#### 1. Spatial Interpolation
- Implemented **Inverse Distance Weighting (IDW)** to create a baseline high-resolution pollution map
- Interpolated values from CALIOPE grid points to target prediction areas
- Applied distance-decay functions to weight the influence of nearby measurement points

#### 2. Road-based Refinement Model
- Extracted features from road networks near air quality stations
- Trained a **Random Forest Regressor** to adjust pollution estimates based on:
  - Road width and type
  - Traffic intensity
  - Surrounding building density
  - Distance to major pollution sources
- Performed feature importance analysis to identify key pollution predictors

#### 3. Temporal Adjustment Layer
- Developed time-series models to account for:
  - Hourly pollution variations (rush hour patterns)
  - Daily patterns (weekday vs. weekend differences)
  - Seasonal trends
- Created adjustment factors to modify base predictions according to specific forecast times

#### 4. Model Validation
- Employed cross-validation techniques to ensure prediction accuracy
- Validated against held-out XVPCA station data
- Optimized hyperparameters for both spatial and temporal components

### Web Application Development
- Created an intuitive interface for accessing high-resolution pollution maps
- Implemented city selection for major Catalan urban areas
- Developed interactive visualization of pollution levels with color-coded indicators
- Enabled time-based forecasting capabilities

## Implementation Details

### Technology Stack
- **Data Processing**: Python, Pandas, NumPy, GeoPandas
- **Machine Learning**: Scikit-learn, Random Forest Regressors
- **Geospatial Analysis**: PostGIS, QGIS
- **Visualization**: Leaflet.js, D3.js
- **Web Development**: Flask, HTML/CSS, JavaScript

### Key Achievements
- Successfully downscaled 1km² resolution data to street-level detail
- Created an accurate predictive model despite limited training data
- Developed a system capable of real-time air quality forecasting
- Produced intuitive visualizations that make pollution patterns easily understandable for citizens

## Team Members
- Sergi Flores
- Clàudia Gallego
- Weihao Lin
- Jiahui Chen

## Social Impact

This project directly supports La Marató de TV3's efforts in fighting respiratory diseases by:
- Raising awareness about air pollution and its health impacts
- Providing citizens with actionable information about local air quality
- Enabling better decision-making about outdoor activities and travel routes
- Supporting public health initiatives through improved environmental monitoring

## Acknowledgements

Special thanks to:
- Barcelona Supercomputing Center for providing the CALIOPE system data and expert guidance
- BitsxLaMarató organization team for creating this meaningful hackathon experience
- La Marató de TV3 for their ongoing work in the fight against respiratory diseases

## Project Relevance

AirQualityMap demonstrates how advanced data science techniques can transform environmental monitoring, making invisible pollution visible and actionable for everyday citizens across Catalonia.

#BitsxLaMarató #AirQuality #DataScience #MachineLearning #EnvironmentalMonitoring
