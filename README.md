# TRAXX 
### Backend server implementation.

This is the server side of the traxx project. 
The prototype is based on Flask server https://flask.palletsprojects.com/en/stable/ 
and JavaScript. 

At the moment we offer a minimalistic demo application, 
which is work in progress


### 1).Execution in local environment

```
flask --app traxxx.py run --debug
```
### 2).Links to the prototype web app

#### 2.1). Steps end to end
```

1). Passenger(s) submits a ride request
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/

 please note the passsenger request Id

2). Driver(s) offers ride (NEW). Detour and distances available
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver_offer

please note the driver request Id

3). Passenger selects a driver offer from all offers
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/passenger_select_driver

please use the request Id from step 1

4). Driver sees passenger confirmation
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver_notify

please use the request Id from step 2

```

### 3). All available APIs

```
passenger console - passenger submits a request
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/

all passenger requests
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/get_all

Driver offer Passangers and luggage (DEPRICATED)
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver

Driver offers ride (NEW)
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver_offer

Manager console (observe requests)
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/manager

Example search box (find Point of Interest)
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/offer/

Example passenger selects driver
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/passenger_select_driver

Example - distance between requests from http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/get_all
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/get_distance?startId=2&destId=1

Driver confirms booking:
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver_notify

```
Application in Google store
https://play.google.com/apps/internaltest/4701729781484107278
```

```


### 4). Restart in AWS
```
ubuntu    101783       1  0 Jan22 ?        00:00:10 python3 traxxx.py
ubuntu    105337  105327  0 06:31 pts/0    00:00:00 grep --color=auto traxx
ubuntu@ip-172-31-95-98:~$ kill -9 101783
```

```
ubuntu@ip-172-31-95-98:~$ python3 -m venv venv
ubuntu@ip-172-31-95-98:~$ source venv/bin/activate
(venv) ubuntu@ip-172-31-95-98:~$ pip3 install geocoder
```

### 5). Curl command to add new request to the traxx server:

```
curl --location 'http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/saveCoordinates' \
--header 'Content-Type: application/json' \
--data '{
"start_address": "Reichendorferstraße 62",
"start_postal-code": "8212",
"start_city": "Pischelsdorf am Kulm",
"start_state": "",
"selected_date_time": "03.02.2025 12: 45",
"dest_address": "Straße Der Nationen 62",
"dest_postal-code": "09111",
"dest_city": "Chemnitz",
"dest_state": "",
"base64_encoded_image_passenger":"VGhpcyBpcyBwZXJzb24gaW1hZ2UgYmFzZSA2NA==",
"base64_encoded_image_luggage":"VGhpcyBpcyBhIHRlc3QgYmFzZTY0IHN0cmluZw=="

}'
```

response:
```
{
    "distance": "646.7",
    "message": "Ihre Bestellnummer ist =4.\nDie Entfernung zwischen Start- und Zielort beträgt 646.7 km",
    "refId": "4"
}
```

### 6). Curl command for ride offers

Driver with ID 3 want to add passengers 2 and 1 to the database.

```
curl --location 'http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/rideOffers' \
--header 'Content-Type: application/json' \
--data '{
    "driver": "3",
    "passengers": [
        "2",
        "1"
    ]
}'
```

### 7). Curl command to get the matching riders for a driver offer

Driver with ID 3 sees a list of passengers matching his offer.

```
curl --location 'http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/get_matches?driverId=3'
```
example response

```
{
    "1": [
        {
            "acceptedRideOfferFrom": 3,
            "offersFrom": [
                "3",
                "4"
            ],
            "request_number": 1,
            "type": "passenger"
        },
        {
            "address": "Uhlandstraße 13 Selbitz  95152",
            "city": "Selbitz",
            "lat": 50.319763,
            "long": 11.754905,
            "postal-code": "95152",
            "starttime": "11.04.2025 12:00",
            "state": ""
        },
        {
            "address": "Kronacher Straße 7 Naila  95119",
            "city": "Naila",
            "lat": 50.328577,
            "long": 11.709326,
            "postal-code": "95119",
            "state": ""
        },
        {
            "detour": "1.0",
            "distance": "4.8",
            "offerFromDriver": "3",
            "price": 0
        }
    ],
    "2": [
        {
            "acceptedRideOfferFrom": 4,
            "offersFrom": [
                "3",
                "4"
            ],
            "request_number": 2,
            "type": "passenger"
        },
        {
            "address": "Am Galgenberg 30 Selbitz  95152",
            "city": "Selbitz",
            "lat": 50.321399,
            "long": 11.755483,
            "postal-code": "95152",
            "starttime": "11.04.2025 12:00",
            "state": ""
        },
        {
            "address": "Weststraße 8 Naila  95119",
            "city": "Naila",
            "lat": 50.329731,
            "long": 11.706246,
            "postal-code": "95119",
            "state": ""
        },
        {
            "detour": "1.3",
            "distance": "5.6",
            "offerFromDriver": "3",
            "price": 0
        }
    ]
}
```




### 8). Project progress

#### DONE     
```
1). Passenger submits start/destination
2). Driver submits start/destination
3). Driver sees passenger requests
4). Driver  submits offer
5). Passenger sees driver offer 
6). Passenger books
7). Driver confirms booking (NO CHAT at the moment)

```
#### IN PROGRESS
```
8). App notificatis/web page.  - Page works, fixing bugs
```

#### TO DO
```
8). App notificatis/web page.
```

#### DID NOT DISCUSS YET
```
9).  Logins
10). Security
11). Optimization
```
