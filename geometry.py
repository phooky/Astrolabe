#!/usr/bin/python
import math

class Element:
    def __init__(self,weight=1):
        self.weight = weight

class Circle(Element):
    def __init__(self,center,radius,weight=1):
        Element.__init__(self,weight)
        self.center = center
        self.radius = radius

class Arc(Circle):
    def __init__(self,center,radius,start=0,stop=math.pi*2.1,weight=1):
        Circle.__init__(self,center,radius,weight)
        self.start = start
        self.stop = stop

def fundamental(rEq,declination):
    """
    Project a point at the given declination on the celestial sphere
    onto a plane at the equator.
    """
    # Seems a little grandiose to call this the fundamental equation
    # of the astrolabe, but okey dokey
    return rEq * math.tan( (math.pi/4) - declination/2 )

