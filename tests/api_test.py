import os
import sys
import requests

# Add the parent directory to Python path to find the constants module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import GOOGLE_MAPS_API_KEY

def test_geocoding_api():
    """Test the Geocoding API"""
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": "London",
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        print("\nGeocoding API Test:")
        print(f"Status: {data['status']}")
        if data['status'] == 'OK':
            print("✓ Geocoding API is working")
            location = data['results'][0]['geometry']['location']
            print(f"Sample result - London coordinates: {location}")
        else:
            print("✗ Geocoding API error:", data.get('error_message', 'Unknown error'))
            
    except Exception as e:
        print("✗ Request failed:", str(e))

def test_maps_javascript_api():
    """Test the Maps JavaScript API"""
    base_url = f"https://maps.googleapis.com/maps/api/js"
    params = {
        "key": GOOGLE_MAPS_API_KEY
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        print("\nMaps JavaScript API Test:")
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("✓ Maps JavaScript API is working")
        else:
            print("✗ Maps JavaScript API error:", response.text)
            
    except Exception as e:
        print("✗ Request failed:", str(e))

if __name__ == "__main__":
    print("Testing Google Maps APIs...")
    print("API Key:", GOOGLE_MAPS_API_KEY[:10] + "..." if GOOGLE_MAPS_API_KEY else "Not set")
    
    test_geocoding_api()
    test_maps_javascript_api() 