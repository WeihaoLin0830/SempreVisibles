# AirQualityMap: High-Resolution Air Quality Forecasting for Catalonia

## 🏆 BSC Challenge Winners - BitsxLaMarató Hackathon

AirQualityMap is an air quality prediction system that downscales regional pollution data to street-level resolution across Catalonia, developed for the "Fem visible l'invisible!" challenge by Barcelona Supercomputing Center.

<img src="/img/photo1.jpg" alt="Catalonia Air Quality Map" width="400"/>

## Project Overview

AirQualityMap transforms low-resolution (1km×1km) air quality predictions from the CALIOPE system into highly detailed street-level pollution maps. By combining advanced spatial interpolation techniques with machine learning models that incorporate traffic patterns and local measurements, we provide citizens with accurate, hyper-local air quality forecasts.

<img src="/img/photo2.jpg" alt="Catalonia Air Quality Map" width="700"/>

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
  - Distance to major pollution sources
- Performed feature importance analysis to identify key pollution predictors

#### 3. Temporal Adjustment Layer
- Trained a **LightGBM** model to account for:
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
