#!/usr/bin/python
import math

class Point:
    def __init__(self,x=0.0,y=0.0):
        self.x = x
        self.y = y
    def len(self):
        return math.sqrt(self.x**2 + self.y**2)
    def diff(self,b):
        return Point(self.x-b.x,self.y-b.y)
    def theta(self):
        return math.atan2(self.y,self.x)
    def __getitem__(self,key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise KeyError(key)

def findVertexAngle(a,b,c):
    "Find the angle of the vertex opposite side c of a triangle."
    return math.acos((a**2+b**2-c**2)/(2*a*b))

class Element:
    def __init__(self,weight=1):
        self.weight = weight

class Circle(Element):
    def __init__(self,center,radius,weight=1):
        Element.__init__(self,weight)
        self.center = center
        self.radius = radius
    def clip(self,c):
        "Clip to given circle, return list of results"
        d = self.center.diff(c.center)
        if d.len() >= self.radius+c.radius:
            return []
        elif self.radius+d.len() <= c.radius:
            return [self]
        else:
            # find theta of distance
            alpha = d.theta()
            beta = findVertexAngle(d.len(),self.radius,c.radius)
            return [Arc(self.center,self.radius,
                        alpha+math.pi-beta,
                        alpha+math.pi+beta,self.weight)]
            #return [Circle(self.center,self.radius,self.weight)]

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

