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
```


### 3. Restart in AWS
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
