# action.py: The Action class!
#
# Some Documentation:
#
# Actions have different types, and these different types have different attributes to go with them
# (Sort of like pygame events)
#
# The constructor format is as follows:
# Action(type (string), description (string), start (datetime), duration (timedelta), params (a list of additional parameters))
#
# The different types are:
# testType: No special parameters (just pass None as params), used for debugging purposes
# movement: When the player moves from one tile to another.
#           params[0] should be a path of tiles to go through,
#           params[1] should be a string representing their method of moving (ie walking, bike, car, etc).
#           The duration field can be None, since it is recalculated based on params[1]
#           After initialisation, self.path is the path, self.method is the method of transport.
# scavenge: When the player is scavenging a tile for supplies.
#           params[0] should be the location.
#           After initialisation, self.location is the location.
# fortify: When the player strengthens the tile to better defend against invading zombies.
#           params[0] should be the location,
#           params[1] should be the list of supplies (or just amount, depends how we implement) used for fortification
#           (or pass None, this makes the player attempt to fortify with what they have).
#           After initialisation, self.location is the location, self.supplies is the list of supplies.
# sweep: When the player "sweeps" an area for zombies
#           params[0] should be the location.
#           After initialisation, self.location is the location.

import math
import datetime

class Action:
    
    def __init__(self, type, desc, startTime, duration, params):
        """Actions are of different types, have a description, parameters based on type, and a start time and duration"""
        self.type = type
        self.desc = desc
        self.startTime = startTime
        self.duration = duration
        self.done = False #A variable so that we store the last call of isDone, to check the doneness
        #TestType
        if self.type == "testType":
            pass
        #Movement
        elif self.type == "movement":
            #Put the params in!
            self.path = params[0] #NOTE: In current implementation, path is only two nodes long... FIX LATER
            self.method = params[1]
            #Calculate the actual duration
            #Currently ignores method
            tilesPerMinute = 1.0
            distance = math.sqrt(math.fabs((self.path[1][0] - self.path[0][0])**2+(self.path[1][1] - self.path[0][1])**2))
            self.duration = datetime.timedelta(minutes = distance/tilesPerMinute)
        #Scavenging
        elif self.type == "scavenge":
            pass
        #Fortification
        elif self.type == "fortify":
            pass
        #Sweep
        elif self.type == "sweep":
            pass
        #Invalid
        else:
            print "Invalid Action Type!"
        
        
    def isDone(self, currTime):
        ans = self.startTime + self.duration <= currTime
        self.done = ans
        return ans
    
    def isStarted(self, currTime):
        return self.startTime < currTime
        
    def timeRemaining(self, currTime):
        return (self.startTime + self.duration) - currTime
        