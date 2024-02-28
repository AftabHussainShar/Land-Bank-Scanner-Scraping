from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize the geocoder with a user_agent, e.g., "myGeocoder"
geolocator = Nominatim(user_agent="myGeocoder")


def get_coordinates(address):
    """
    Convert an address to latitude and longitude coordinates.

    Parameters:
    - address: A string containing the address to geocode.

    Returns:
    - A tuple (latitude, longitude) of the geocoded address, or (None, None) if geocoding fails.
    """
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except Exception as e:
        print(f"Error geocoding address {address}: {e}")
        return (None, None)


def calculate_distance(address, target_coordinates=(33.383579662070005, -84.25380479849588)):
    """
    Calculate the distance in kilometers from the address to the target coordinates.

    Parameters:
    - address: A string containing the address.
    - target_coordinates: A tuple (latitude, longitude) representing the target location.

    Returns:
    - The distance in kilometers as a float, or None if the address could not be geocoded.
    """
    address_coordinates = get_coordinates(address)
    if None not in address_coordinates:
        distance = geodesic(address_coordinates, target_coordinates).kilometers
        return distance
    else:
        return None

# Example usage:
# address = "1600 Pennsylvania Ave NW, Washington, DC 20500"
# distance = calculate_distance(address)
# print(f"Distance: {distance} kilometers")
