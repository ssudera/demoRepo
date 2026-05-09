# import required modules
import requests, json

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_city_coordinates(city_name):
    """
    Get latitude and longitude of a city using OpenStreetMap's Nominatim API.
    """
    try:
        # Create a geolocator object with a custom user agent
        geolocator = Nominatim(user_agent="geoapi_example")

        # Geocode the city name
        location = geolocator.geocode(city_name, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"City '{city_name}' not found.")
            return None

    except GeocoderTimedOut:
        print("Request timed out. Please try again.")
        return None
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def get_Weather(Latitude,Longitude):
  base_url = "https://api.open-meteo.com/v1/forecast"
  complete_url = base_url + "?latitude=" + str(Latitude) + "&longitude=" + str(Longitude) + "&current_weather=true" # Convert floats to strings here
  response = requests.get(complete_url)
  x = response.json()
  print(f"{city}'s LATITUDE {x['latitude']}")
  print(f"longitude {x['longitude']}")
  print(f"elevation {x['elevation']}")
  print(f"Temperature {x['current_weather']['temperature']} {x['current_weather_units']['temperature']}")
  print(f"Windspeed {x['current_weather']['windspeed']} {x['current_weather_units']['windspeed']}")
  print(f"Winddirection {x['current_weather']['winddirection']} {x['current_weather_units']['winddirection']}")

  # Example usage
if __name__ == "__main__":
    city = input("Enter city name: ").strip()
    coords = get_city_coordinates(city)
    print(f"Cordinates:{coords}")
    # These assignments are not strictly necessary if get_Weather converts internally,
    # but they don't hurt. The key is that the *arguments* passed to get_Weather are floats.
    # Latitude=str(coords[0]) 
    # Longitude=str(coords[1]) 
    if coords:
        print(f"Coordinates of {city}: Latitude={coords[0]}, Longitude={coords[1]}")
        get_Weather(coords[0],coords[1]) # Pass floats directly
    else:
        print("Invalid City Name")
