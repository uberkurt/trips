#!/usr/bin/python
from UberTrip import Trip
import random

triplist = []
simultrips = 10

# initialize a number of simultaneous trips
for count in xrange(simultrips):
    newtrip = Trip()
    triplist.append(newtrip)

# Uber never stops!
while (True):
    print 'There are ', Trip.tripCount, ' trips in progress'
    if Trip.tripCount < simultrips:
        # always have max number of simultaneous trips in progress, so bump +1 now
        newtrip = Trip()
        triplist.append(newtrip)

    # iterate all trips, and move / end them
    for trip in triplist:
        trip.move()
        # print debug / info
        print trip.id, ": ", trip.status, " @", trip.lat, '/', trip.lon
        if random.randint(1, 100) == 100:
            trip.finish()
            triplist.remove(trip)

sys.exit(0)

