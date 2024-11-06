# How Dangerous is My City

This program lets user enter a location and retrieves data about earthquake activity, flood risk, and air 
pollution for that area.

# Features

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


# Installation

- Python 3.12 or later version
- Install Flask and Requests
- Set up API keys
    
Dependencies: Python >=3.12

macOS/Linux:
1. Run
   ```bash
   python -m venv venv 
   source venv/bin/activate 
   pip install -r requirements.txt
3. Set environment variables for Open Weather Map, and Flooding API keys:
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

### Unit tests
Ensure environment variables are set as above, then run `python tests.py`.

# Screenshots
## Installation and Setup
### Activating Environment and Running Application
*Activating the environment and running python app.py*
![image](https://github.com/user-attachments/assets/70f3bda2-3da4-4906-abf0-ef0d69cd364c)

### Homepage
*Description: The main screen where users enter a location.*
![image](https://github.com/user-attachments/assets/7d5a7a4c-7044-4ec3-8038-0168d41e5457)
![image](https://github.com/user-attachments/assets/f5199fc8-c72e-40a7-ad6c-e1bd43334739)

### Result page
*Description: A sample results page showing flood risk assessment, air quality levels, and earthquake data.*

![image](https://github.com/user-attachments/assets/79d131b4-9adf-4578-9d14-a24a2956498c)
![image](https://github.com/user-attachments/assets/966cff1d-386c-4e11-9d26-68e8e1b2b36f)

### Location not found
*If an invalid or unrecognized location is entered, the user will see an error page with a message indicating that the location was not found. They will then have the option to return to the home page*
![image](https://github.com/user-attachments/assets/00632bbd-7a87-4198-8995-17feb2265a1c)
![image](https://github.com/user-attachments/assets/375a9539-54f6-4867-8581-770606d95d2f)

## Bookmarks
*A snapshots of the bookmarks feature, showing saved items and details.*
![image](https://github.com/user-attachments/assets/6d2f0548-b7fc-4ec4-8771-8028ec44cc8e)
![image](https://github.com/user-attachments/assets/1f30dd01-10aa-4b5f-afad-c4eee623b9b6)
![image](https://github.com/user-attachments/assets/f139aa92-5d8f-4c2f-b6ba-35d3a4e3966d)












