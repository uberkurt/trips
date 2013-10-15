import sys
import json
import random
import time
from pyes import *
from datetime import datetime

class Trip:
    # initialize class variable for Elasticsearch connection
    conn = ES('127.0.0.1:9200') 
    # class variable for number of simultaneous trips
    tripCount = 0

    def __init__(self):
        print 'Initializing an exciting Uber trip'
        # clearly, a better method of generating unique tripId is needed
        self.id = random.randint(1, 10000000)
        # generate random pickup location somewhere in San Francisco
        self.set_pickup()
        # Start-of-trip indicator
        self.status = 'BEGIN'
        # haven't gone anywhere yet
        self.moves = 0
        # fare remains $0.00 until the end with this heuristic
        self.fare = 0.0
        # bump class variable
        Trip.tripCount += 1
        # log it to Elasticsearch
        self.log()

    def move(self):
        # find a delta movement for both lat and lon
        latDelta = round(random.uniform(.001, .002), 3)
        lonDelta = round(random.uniform(.001, .002), 3)
        # randomly meander positive or negatively in the delta direction
        self.lat = (self.lat + latDelta) if (random.random() < .5) else (self.lat - latDelta)
        self.lon = (self.lon + lonDelta) if (random.random() < .5) else (self.lon - lonDelta)
        # trip still in progress, as far as we know
        self.moves += 1
        self.status = 'IN_PROGRESS'
        self.log()

        
    def log(self):
        # index this trip's status in ES
        Trip.conn.index({
                "tripId":self.id,
                "status":self.status,
                "fare":self.fare,
                "location" : {
                    "lat":self.lat,
                    "lon":self.lon
                    }
                },
                        "uber", "trips")
        
    def set_pickup(self):
        # pick a point somewhere in San Francisco
        self.lat = round(random.uniform(37.720, 37.785),3)
        self.lon = round(random.uniform(-122.505, -122.392),3)
 
    def finish(self):
        # end-of-trip indicator
        self.status = 'END'
        # just kinda making a stab at calculating fare here
        self.fare = self.moves * .2
        # decrement class variable by 1
        Trip.tripCount -= 1
        # print debug stuff
        print self.status, ":", self.lat, ':', self.lon, ":", self.moves, " moves.", "Fare: ", self.fare
        self.log()
        del self
