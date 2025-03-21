from flask import Flask, request, render_template,jsonify, send_from_directory,redirect,url_for
#from geopy.geocoders import Nominatim
import os
import geocoder
import math
import requests
import base64

app = Flask(__name__)

IMAGE_DIR = os.getcwd()


start_coordinates=[]
dest_coordinates=[]
coordinates={}
num_requests={}
route_detour={}
num_requests = {"num_requests":0}

ACCESS_TOKEN = "pk.eyJ1Ijoib2thYnJhbm92IiwiYSI6ImNtNW5oc2FwazBiNWUybHE1ZGE0Z2hvMG8ifQ.waPPu_t4BN-s2cF6UObqcA";

@app.route('/')
def hello():
    return render_template('index6.html')

@app.route('/driver')
def driver():
    return render_template('index.html')

@app.route('/manager')
def manager():
    return render_template('index_manager.html')

@app.route('/passenger_choice')
def passanger_choice():
    query = request.args.get('driverId')  # Get query parameter `q`
    print(f"Search query: {query}")  # Print in server logs
    return render_template('index_passanger_choice.html')

@app.route('/passenger_select_driver')
def passenger_select_driver():
    #query = request.args.get('driverId')  # Get query parameter `q`
    #print(f"Search query: {query}")  # Print in server logs
    return render_template('passanger_select_driver.html')


@app.route('/get_distance')
def distance_between():
    startId = request.args.get('startId')  # Get query parameter `q`
    destId = request.args.get('destId')  # Get query parameter `q`
    print(f"startId: {startId}")  # Print in server logs
    print(f"destId: {destId}")  # Print in server logs
    #return render_template('index_passanger_choice.html',startId=startId,destId=destId)
    result = get_distance_request(startId,destId)
    print("distance_between="+str(result))
    return jsonify(str(result))


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
    print(coordinates)
    return jsonify(coordinates)

@app.route('/images')
def list_images():


    IMAGE_FOLDER = IMAGE_DIR +'/images'
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.jpg') or f.endswith('.jpeg')]
    return jsonify(images)


@app.route('/images/<filename>')
def get_image(filename):
    """Serves the requested image."""
    IMAGE_FOLDER = IMAGE_DIR +'/images'
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/rideOffers', methods=['POST'])
def handle_ride():
    try:
        data = request.get_json()

        # Extract driver and passengers
        driver_id = data.get("driver")
        passengers = data.get("passengers")
        print(driver_id)
        print(passengers)
        if not driver_id or not isinstance(passengers, list):
            return jsonify({"error": "Invalid input format"}), 400

        print("driverId=", coordinates.get(int(driver_id))[0])
        passIdList = list(map(int, passengers))

        print("passIdList=", passIdList)


        coordinates.get(int(driver_id))[0]["offersSentTo"] = passIdList
        print("offersSentTo:",coordinates.get(int(driver_id))[0]["offersSentTo"])
        print("passIdList=", passIdList)
        for passId in passIdList:
            print("passId:",passId)
            print("==>passId:",coordinates.get(int(passId))[0])
            print("==>passId:",coordinates.get(int(passId))[0].get("type"))
            #print("==>offersFrom:",coordinates.get(int(passId))[0]["offersFrom"])
            if coordinates.get(int(passId))[0].get("offersFrom") == None:
                coordinates.get(int(passId))[0]["offersFrom"] = []
            coordinates.get(int(passId))[0].get("offersFrom").append(driver_id)


        # Example response
        response = {
            "message": "Ride request received",
            "driver": driver_id
            #"passengers": list
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/saveCoordinates', methods=['POST'])
def save_coordinates():
    try:
        data = request.get_json()
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

            base64_encoded_passenger_image=""
            base64_encoded_luggage_image=""
            if "base64_encoded_image_passenger" in data :
                base64_encoded_passenger_image = data["base64_encoded_image_passenger"]
            if "base64_encoded_image_luggage" in data :
                base64_encoded_luggage_image = data["base64_encoded_image_luggage"]

        except (ValueError, TypeError):
            return jsonify({"error": "Invalid data types for long or lat. Must be numbers"}), 400

        start_address_string="{0} {1} {2} {3}".format(start_address, start_city,start_state, start_postal_code)
        coords_start = get_coordinates(start_address_string)

        dest_address_string="{0} {1} {2} {3}".format(dest_address, dest_city,dest_state, dest_postal_code)
        coords_dest = get_coordinates(dest_address_string)

        print(coords_start)
        print(coords_dest)

        lat_start, long_start =  coords_start
        lat_dest, long_dest =  coords_dest


        distance = haversine(lat_start, long_start, lat_dest, long_dest)
        string_disctance = "{:.1f}".format(float(distance))
        print("distance:"+string_disctance)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'access_token': 'pk.eyJ1Ijoib2thYnJhbm92IiwiYSI6ImNtNW5oc2FwazBiNWUybHE1ZGE0Z2hvMG8ifQ.waPPu_t4BN-s2cF6UObqcA',
        }

        data = 'coordinates='+str(long_start)+','+str(lat_start)+';'+str(long_dest)+','+str(lat_dest)+'&steps=true&waypoints=0;1&waypoint_names=Home;Work&banner_instructions=true'
        print(data)

        response = requests.post('https://api.mapbox.com/directions/v5/mapbox/driving', params=params, headers=headers, data=data)

        json_map = response.json()

        if not 'routes' in json_map or len(json_map['routes'])==0:
            return "Keine Route zwischen Start und Ziel existiert. Bitte überprüfen Sie Ihre Start- und Zieladresse. ",201

        map_distance_json = json_map['routes'][0].get('distance')
        map_distance_float = float(map_distance_json)/1000.0
        map_distance_str = "{:.1f}".format(float(map_distance_float))

        print(json_map['routes'][0].get('distance'))

        pass_data = {
            "request_number" : num_requests["num_requests"]+1,
            "type":"passenger"
        }
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
            "state":dest_state
        }
        route_data = {
            "distance" : map_distance_str,
            "price":0
        }


        # Processing of data

        new_coordinate = pass_data,new_coordinate_start,new_coordinate_dest,route_data


        start_coordinates.append(new_coordinate_start)
        dest_coordinates.append(new_coordinate_dest)

        num_requests["num_requests"] =  num_requests["num_requests"]+1

        passenger_image = b''
        luggage_image = b''
        if base64_encoded_passenger_image:
            passenger_image = base64.b64decode(base64_encoded_passenger_image)

        if base64_encoded_luggage_image:
            luggage_image = base64.b64decode(base64_encoded_luggage_image)

        print("passenger_image:"+str(passenger_image))
        print("luggage_image:"+str(luggage_image))

        # Save the decoded data to a file

        if passenger_image and not passenger_image == b'':
            passenger_image_name = IMAGE_DIR+"/images/"+"passenger_image_"+str(num_requests["num_requests"])+".jpeg"
            with open(passenger_image_name, "wb") as file:
                file.write(passenger_image)

        if luggage_image and not luggage_image == b'':
            luggage_image_name = IMAGE_DIR+"/images/"+"luggage_image_"+str(num_requests["num_requests"])+".jpeg"
            with open(luggage_image_name, "wb") as file:
                file.write(luggage_image)

        # Save in the database hash
        coordinates[num_requests["num_requests"]]=new_coordinate
        print("new_coordinate="+ str(num_requests["num_requests"]))

        #return jsonify({"message": "Coordinates saved successfully", "data": (str(num_requests["num_requests"]), new_coordinate)}), 201
        #return "Ihre Bestellnummer ist ="+str(num_requests["num_requests"])+"=  Bitte zeigen Sie diese Bestellnummer dem Fahrer am Abholort.  Ihre Abholzeut ist "+ selected_time + ".", 201
        #return "Die Entfernung zwischen Start- und Zielort beträgt " + string_disctance+ " km",201

        #return "Die Entfernung zwischen Start- und Zielort beträgt " + map_distance_str+ " km",201
        return "Ihre Bestellnummer ist ="+str(num_requests["num_requests"])+"."+'\n'+"Die Entfernung zwischen Start- und Zielort beträgt " + map_distance_str+ " km",201

    except Exception as e:
        print(f"An error occurred: {e}") # Log the error for debugging
        return jsonify({"error": "An internal server error occurred"}), 500



@app.route('/saveCoordinatesDriver', methods=['POST'])
def save_coordinates_driver():
    try:
        data = request.get_json()
        print("saveCoordinatesDriver")
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

            base64_encoded_passenger_image=""
            base64_encoded_luggage_image=""
            if "base64_encoded_image_passenger" in data :
                base64_encoded_passenger_image = data["base64_encoded_image_passenger"]
            if "base64_encoded_image_luggage" in data :
                base64_encoded_luggage_image = data["base64_encoded_image_luggage"]

        except (ValueError, TypeError):
            return jsonify({"error": "Invalid data types for long or lat. Must be numbers"}), 400

        start_address_string="{0} {1} {2} {3}".format(start_address, start_city,start_state, start_postal_code)
        coords_start = get_coordinates(start_address_string)

        dest_address_string="{0} {1} {2} {3}".format(dest_address, dest_city,dest_state, dest_postal_code)
        coords_dest = get_coordinates(dest_address_string)

        print(coords_start)
        print(coords_dest)

        lat_start, long_start =  coords_start
        lat_dest, long_dest =  coords_dest


        distance = haversine(lat_start, long_start, lat_dest, long_dest)
        string_disctance = "{:.1f}".format(float(distance))
        print("distance:"+string_disctance)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'access_token': 'pk.eyJ1Ijoib2thYnJhbm92IiwiYSI6ImNtNW5oc2FwazBiNWUybHE1ZGE0Z2hvMG8ifQ.waPPu_t4BN-s2cF6UObqcA',
        }

        data = 'coordinates='+str(long_start)+','+str(lat_start)+';'+str(long_dest)+','+str(lat_dest)+'&steps=true&waypoints=0;1&waypoint_names=Home;Work&banner_instructions=true'
        print(data)

        response = requests.post('https://api.mapbox.com/directions/v5/mapbox/driving', params=params, headers=headers, data=data)

        json_map = response.json()

        if not 'routes' in json_map or len(json_map['routes'])==0:
            return "Keine Route zwischen Start und Ziel existiert. Bitte überprüfen Sie Ihre Start- und Zieladresse. ",201

        map_distance_json = json_map['routes'][0].get('distance')
        map_distance_float = float(map_distance_json)/1000.0
        map_distance_str = "{:.1f}".format(float(map_distance_float))

        print(json_map['routes'][0].get('distance'))

        pass_data = {
            "request_number" : num_requests["num_requests"]+1,
            "type":"driver"
        }
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
            "state":dest_state
        }
        route_data = {
            "distance" : string_disctance,
            "price":0
        }

        # Processing of data

        new_coordinate = pass_data,new_coordinate_start,new_coordinate_dest,route_data


        start_coordinates.append(new_coordinate_start)
        dest_coordinates.append(new_coordinate_dest)

        num_requests["num_requests"] =  num_requests["num_requests"]+1

        passenger_image = b''
        luggage_image = b''
        if base64_encoded_passenger_image:
            passenger_image = base64.b64decode(base64_encoded_passenger_image)

        if base64_encoded_luggage_image:
            luggage_image = base64.b64decode(base64_encoded_luggage_image)

        print("passenger_image:"+str(passenger_image))
        print("luggage_image:"+str(luggage_image))

        # Save the decoded data to a file

        if passenger_image and not passenger_image == b'':
            passenger_image_name = IMAGE_DIR+"/images/"+"passenger_image_"+str(num_requests["num_requests"])+".jpeg"
            with open(passenger_image_name, "wb") as file:
                file.write(passenger_image)

        if luggage_image and not luggage_image == b'':
            luggage_image_name = IMAGE_DIR+"/images/"+"luggage_image_"+str(num_requests["num_requests"])+".jpeg"
            with open(luggage_image_name, "wb") as file:
                file.write(luggage_image)

        # Save in the database hash
        coordinates[num_requests["num_requests"]]=new_coordinate
        print("new_coordinate="+ str(num_requests["num_requests"]))

        #return jsonify({"message": "Coordinates saved successfully", "data": (str(num_requests["num_requests"]), new_coordinate)}), 201
        #return "Ihre Bestellnummer ist ="+str(num_requests["num_requests"])+"=  Bitte zeigen Sie diese Bestellnummer dem Fahrer am Abholort.  Ihre Abholzeut ist "+ selected_time + ".", 201
        #return "Die Entfernung zwischen Start- und Zielort beträgt " + string_disctance+ " km",201

        ###return "Die Entfernung zwischen Start- und Zielort beträgt " + map_distance_str+ " km "+ "request="+str(num_requests["num_requests"]),201
        return str(num_requests["num_requests"]),201
        #print("======================== Rendering")
        #return render_template('index_manager.html',title='Driver Page')
        #return redirect(url_for("manager"))

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

def get_distance_request(id1,id2):


        # driver_start
        # passenger_start
        # passenger_end
        # driver_end
        # detour = distance(driver_start,passenger_start)+distance(passenger_end,driver_end)

        #coordinates
        driver_start_long = coordinates[int(id1)][1].get("long")
        driver_start_lat = coordinates[int(id1)][1].get("lat")
        passenger_start_long = coordinates[int(id2)][1].get("long")
        passenger_start_lat = coordinates[int(id2)][1].get("lat")

        print("driver_start_long=",driver_start_long)
        print("driver_start_lat=",driver_start_lat)
        print("passenger_start_long=",passenger_start_long)
        print("passenger_start_lat=",passenger_start_lat)


        detour1 = 'coordinates='+str(driver_start_long)+','+str(driver_start_lat)+';'+str(passenger_start_long)+','+str(passenger_start_lat)+'&steps=true&waypoints=0;1&waypoint_names=Home;Work&banner_instructions=true'
        print(detour1)

        response1 = call_map_box(detour1)
        json_map1 = response1.json()

        if not 'routes' in json_map1 or len(json_map1['routes'])==0:
            return "Keine Route zwischen Start und Ziel existiert. Bitte überprüfen Sie Ihre Start- und Zieladresse. ",201

        map_distance_json1 = json_map1['routes'][0].get('distance')
        map_distance_float1 = float(map_distance_json1)/1000.0
        map_distance_str1 = "{:.1f}".format(float(map_distance_float1))


        passenger_end_long = coordinates[int(id2)][2].get("long")
        passenger_end_lat = coordinates[int(id2)][2].get("lat")
        driver_end_long = coordinates[int(id1)][2].get("long")
        driver_end_lat = coordinates[int(id1)][2].get("lat")

        detour2= 'coordinates='+str(passenger_end_long)+','+str(passenger_end_lat)+';'+str(driver_end_long)+','+str(driver_end_lat)+'&steps=true&waypoints=0;1&waypoint_names=Home;Work&banner_instructions=true'
        print(detour2)

        response2 = call_map_box(detour2)
        json_map2 = response2.json()

        if not 'routes' in json_map2 or len(json_map2['routes'])==0:
            return "Keine Route zwischen Start und Ziel existiert. Bitte überprüfen Sie Ihre Start- und Zieladresse. ",201

        map_distance_json2 = json_map2['routes'][0].get('distance')
        map_distance_float2 = float(map_distance_json2)/1000.0
        map_distance_str2 = "{:.1f}".format(float(map_distance_float2))

        map_distance_float = map_distance_float1+map_distance_float2
        map_distance_str = "{:.1f}".format(float(map_distance_float))

        print(map_distance_str)
        route_detour["detour"]=map_distance_str

        route= 'coordinates='+str(passenger_start_long)+','+str(passenger_start_lat)+';'+str(passenger_end_long)+','+str(passenger_end_lat)+'&steps=true&waypoints=0;1&waypoint_names=Home;Work&banner_instructions=true'
        print(route)
        response_route = call_map_box(route)
        json_map_route = response_route.json()
        map_route_json = json_map_route['routes'][0].get('distance')
        map_route_float = float(map_route_json)/1000.0
        map_route_str = "{:.1f}".format(float(map_route_float))

        route_detour["route"]=map_route_str
        return route_detour


def  call_map_box(data):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'access_token': 'pk.eyJ1Ijoib2thYnJhbm92IiwiYSI6ImNtNW5oc2FwazBiNWUybHE1ZGE0Z2hvMG8ifQ.waPPu_t4BN-s2cF6UObqcA',
        }
        print("coordinates=",data)
        response = requests.post('https://api.mapbox.com/directions/v5/mapbox/driving', params=params, headers=headers, data=data)


        return response




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)