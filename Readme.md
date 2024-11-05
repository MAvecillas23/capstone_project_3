How Dangerous is My City

This program lets user enter a location and retrieves data about earthquake activity, flood risk, and air 
pollution for that area.

Features

1.Earthquake Data

- Description: Retrieves earthquake information within a 15-mile radius of the specified location.
    
*Data Returned:*
- Date of each earthquake
- Magnitude (3.0 or higher)
- Location (relative to the specified city, including coordinates or nearby landmarks)
    
- Timeframe: Covers earthquakes from the last 3 years.

2.Flood Risk
    
- Description: Evaluates flood risk for the specified location based on FEMA's National Flood Data.

*Data Returned:*
- Flood Zone level: The program returns whether the are is "safe","not safe" or "unknown flood risk"

3.Air Pollution

- Description: Retrieves data on various air pollutants at the specified location.

*Pollutants*
- Carbon monoxide (CO)
- Nitrogen monoxide (NO)
- Nitrogen dioxide (NO2)
- Ozone (O3)
- Sulphur dioxide (SO2)
- Ammonia (NH3)

*Air Quality Index: Returns an air quality index (AQI) score from 1 to 5.*
- Good air quality is 1
- Very poor air quality is 5


Installation

- Python 3.12 or later version
- Install Flask and Requests
- Set up API keys
    
Dependencies: Python >=3.12

macOS/Linux:
1. Run  python -m venv venv 
        source venv/bin/activate 
        pip install -r requirements.txt
2. Set environment variables for Open Weather Map, and Flooding API keys:
   ```bash
    export OWM_API_KEY=api key
    export FEMA_API_KEY=api key
   ```
4. Run `python app.py` and access `http://localhost:5000`.

Windows:
1. Run
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. set environment variables for Open Weather Map, and Flooding API keys:
   ```
   set OWM_API_KEY=api key
   set FEMA_API_KEY=api key
   ```
5. Run `python app.py` and access `http://localhost:5000`.
