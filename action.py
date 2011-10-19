#action.py: The Action class!

class Action:
    
    def __init__(self, type, desc, startTime, duration, params):
        """Actions are of different types, have a description, parameters based on type, and a start time and duration"""
        self.type = type
        self.desc = desc
        self.startTime = startTime
        self.duration = duration
        #Deal with params here:
        self.params = params
        #TODO: DO MORE HERE
        
        
    def isDone(self, currTime):
        return self.startTime + self.duration <= currTime