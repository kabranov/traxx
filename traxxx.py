from flask import Flask, request, render_template,jsonify
#from geopy.geocoders import Nominatim
import geocoder
import math

app = Flask(__name__)


start_coordinates=[]
dest_coordinates=[]
coordinates={}
num_requests={}
num_requests = {"num_requests":0}

@app.route('/')
def hello():
    return render_template('index6.html')

@app.route('/offer/',methods=['GET'])
def offer():
    return render_template('offerForm.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    sAddress = request.form['sAddress']
    eAddress = request.form['eAddress']
    print(sAddress)
    print(eAddress)
    geolocator = Nominatim(user_agent="my_geopy_app")
    start_address = geolocator.geocode(sAddress).address
    end_address = geolocator.geocode(eAddress).address
    print(start_address)
    print(end_address)
    start_coord = (geolocator.geocode(sAddress).latitude, geolocator.geocode(sAddress).longitude)
    print(start_coord)
    end_coord = (geolocator.geocode(eAddress).latitude, geolocator.geocode(eAddress).longitude)
    print(end_coord)

    with open('./templates/coordinates.txt', 'a') as a:
             a.write('%s,%s,%s,%s\n' % (start_coord[0],start_coord[1],end_coord[0],end_coord[1]))

    return render_template('index1.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Flask!'}
    with open('./templates/coordinates.txt', 'r') as file:
        file_content = file.read()
    data = {'message': file_content}
    print('+++')
    print(data)
    return jsonify(data)

@app.route('/get_all', methods=['GET'])
def get_all():
    print('+++')
    print(coordinates)
    return jsonify(coordinates)


@app.route('/saveCoordinates', methods=['POST'])
def save_coordinates():
    try:
        data = request.get_json()
        print("====>new data")
        print(data)
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        required_fields = ["start_address","dest_address"]
        if not all(field in data for field in required_fields):
            missing_fields = [field for field in required_fields if field not in data]
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        try:
            start_address = data["start_address"]
            start_postal_code=data["start_postal-code"]
            start_city= data["start_city"]
            start_state = data["start_state"]

            dest_address = data["dest_address"]
            dest_postal_code=data["dest_postal-code"]
            dest_city= data["dest_city"]
            dest_state = data["dest_state"]

            selected_time = data["selected_date_time"]

        except (ValueError, TypeError):
            return jsonify({"error": "Invalid data types for long or lat. Must be numbers"}), 400

        start_address_string="{0} {1} {2} {3} {4}".format(start_address, start_city,start_state, start_postal_code, selected_time)
        coords_start = get_coordinates(start_address_string)

        dest_address_string="{0} {1} {2} {3}".format(dest_address, dest_city,dest_state, dest_postal_code)
        coords_dest = get_coordinates(dest_address_string)

        print(coords_start)
        print(coords_dest)

        lat_start, long_start =  coords_start
        lat_dest, long_dest =  coords_dest


        distance = haversine(lat_start, long_start, lat_dest, long_dest)
        string_disctance = "{:.1f}".format(float(distance))
        print(string_disctance)


        new_coordinate_start = {
            "long": coords_start[1],
            "lat":coords_start[0],
            "address": start_address_string,
            "postal-code":start_postal_code,
            "city":start_city,
            "state":start_state,
            "starttime":selected_time
        }

        new_coordinate_dest = {
            "long": coords_dest[1],
            "lat":coords_dest[0],
            "address": dest_address_string,
            "postal-code":dest_postal_code,
            "city":dest_city,
            "state":dest_state,
            "route":string_disctance
        }

        new_coordinate = new_coordinate_start,new_coordinate_dest


        start_coordinates.append(new_coordinate_start)
        dest_coordinates.append(new_coordinate_dest)

        num_requests["num_requests"] =  num_requests["num_requests"]+1
        coordinates[num_requests["num_requests"]]=new_coordinate
        print("new_coordinate="+ str(num_requests["num_requests"]))



        #return jsonify({"message": "Coordinates saved successfully", "data": (str(num_requests["num_requests"]), new_coordinate)}), 201
        #return "Ihre Bestellnummer ist ="+str(num_requests["num_requests"])+"=  Bitte zeigen Sie diese Bestellnummer dem Fahrer am Abholort.  Ihre Abholzeut ist "+ selected_time + ".", 201
        return "Die Entfernung zwischen Start- und Zielort beträgt " + string_disctance+ " km",201


    except Exception as e:
        print(f"An error occurred: {e}") # Log the error for debugging
        return jsonify({"error": "An internal server error occurred"}), 500


def get_coordinates( address:str)-> [str, str]:
    """This function takes a name as input and returns a tuple of strings."""
    #greeting = "Hello, " + name
    #farewell = "Goodbye, " + name
    #return greeting, farewell

    g = geocoder.mapbox(address, key='pk.eyJ1Ijoib2thYnJhbm92IiwiYSI6ImNtNW5oc2FwazBiNWUybHE1ZGE0Z2hvMG8ifQ.waPPu_t4BN-s2cF6UObqcA')
    if g.ok:
        latitude = g.lat
        longitude = g.lng
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("Geocoding failed.")
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            return jsonify({"error": "Invalid longitude or latitude values"}), 400

    return latitude,longitude


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Earth in kilometers (mean radius = 6,371 km)
    radius = 6371.0
    return radius * c


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)