#!/usr/bin/python

import Adafruit_DHT
import socket

### CONFIG ###
# fhem's telnet port
host = 'localhost'
port = 7072

sensors = [
    {
        'name': 'DHT22',
        'type': Adafruit_DHT.DHT22,
        'pin':  5
    },
]

# retry in case of error
retries = 2
delay = 2


## config reference:
# sensors = [
#     {
#         'name': 'DHT22',
#         'type': Adafruit_DHT.DHT22,
#         'pin':  4
#     },
#     {
#         'name': 'DHT11',
#         'type': Adafruit_DHT.DHT11,
#         'pin':  4
#     },
#     {
#         'name': 'AM2302',
#         'type': Adafruit_DHT.AM2302,
#         'pin':  4
#     },
# ]

### END CONFIG ###

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
    if data:
        print "Received:", repr(data)
    s.close()

# empty netcat string
s = "";

for sensor in sensors:
    humidity, temperature = Adafruit_DHT.read_retry(sensor['type'], sensor['pin'], retries, delay)

    if humidity is not None and temperature is not None:
            s += 'setreading {0} Temperature {1:0.1f}\n'.format(sensor['name'], temperature)
            s += 'setreading {0} Humidity {1:0.1f}\n'.format(sensor['name'], humidity)
            s += 'setreading {0} Error 0\n'.format(sensor['name'])
    else:
            s += 'setreading {0} Error 1\n'.format(sensor['name'])

s += "quit"

netcat(host, port, s)
