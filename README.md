# AirQualityMap_Bits
Project developed by Sergi Flores, Clàudia Gallego, Weihao Lin and Jiahui Chen for the BitsxLaMarató Hackathon, a really special hackathon due to its charity nature. 

## Random Forest Regressor
Mapa d'alta resolució de la qualitat d'aire en Catalunya. #BitsxLaMarató 2024

Our solution focused on interpolating the points we aimed to predict using IDW (Inverse Distance Weighting) combined with the 1 km resolution data from the CALIOPE system. Next, we trained a model using air quality station data and their nearest roads to refine the results based on road-specific characteristics. Additionally, we developed a temporal model to adjust the outcomes according to the desired hour and day and created a simple website that provides air quality forecasts for the main cities in Catalonia.
