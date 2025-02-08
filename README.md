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

```
passenger console - subnmit a request
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/

all passenger requests
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/get_all

Passangers and luggage
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/driver

Manager console
http://ec2-44-202-55-203.compute-1.amazonaws.com:5000/manager
```


### 3). Restart in AWS
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

### 4). Curl command to add new request to the traxx server:

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