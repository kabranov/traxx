import geohash

def get_geohash(latitude, longitude, precision=8):
    """
    Generate a geohash for the given latitude and longitude.

    Arguments:
    latitude -- Latitude of the location (float)
    longitude -- Longitude of the location (float)
    precision -- Number of characters in the geohash (default is 8)

    Returns:
    A geohash string.
    """
    return geohash.encode(latitude, longitude, precision)

# Example Usage
if __name__ == "__main__":
    # Coordinates for the location (example: San Francisco)
    latitude = 37.774929
    longitude = -122.419418

    # Get geohash
    geohash_result = get_geohash(latitude, longitude, precision=8)

    print(f"The geohash for the location ({latitude}, {longitude}) is: {geohash_result}")

