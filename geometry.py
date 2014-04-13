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
    def normalized(self):
        d=self.len()
        return Point(self.x/d,self.y/d)
    def cross(self,v):
        return self.x*v.y - self.y*v.x
    def __add__(self,v):
        return Point(self.x+v.x,self.y+v.y)
    def __sub__(self,v):
        return Point(self.x-v.x,self.y-v.y)
    def __mul__(self,c):
        return Point(self.x*c,self.y*c)
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
    def clip(self,clippedTo):
        "Return a version of this object, clipped to the given object"
        raise NotImplementedError()

class Line(Element):
    def __init__(self,center,direction,weight=1,start=-1000.0,stop=1000.0):
        Element.__init__(self,weight)
        self.center = center
        self.direction = direction
        self.start = start
        self.stop = stop
    def start_point(self):
        return self.center + (self.direction*self.start)
    def stop_point(self):
        return self.center + (self.direction*self.stop)
    def clip(self,e):
        "Clip to given element"
        l=Line(self.center,self.direction,self.weight,self.start,self.stop)
        if isinstance(e,Line):
            c=l.direction.cross(e.direction)
            if c == 0.0:
                return [] #parallel lines
            else:
                t = -(self.center - e.center).cross(e.direction) / c
                l.start = max(l.start,t)
                return [l]
        else:
            return []

class Circle(Element):
    def __init__(self,center,radius,weight=1):
        Element.__init__(self,weight)
        self.center = center
        self.radius = radius
    def clip(self,c):
        "Clip to given circle, return list of results"
        if isinstance(c,Line):
            return []
        d = self.center.diff(c.center)
        if d.len() >= self.radius+c.radius:
            return []
        elif self.radius+d.len() <= c.radius:
            return [self]
        else:
            # find theta of distance
            alpha = d.theta()
            beta = findVertexAngle(d.len(),self.radius,c.radius)
            s2 = alpha+math.pi-beta
            e2 = alpha+math.pi+beta
            try:
                s2 = max(s2,self.start)
                e2 = min(e2,self.stop)
            except:
                pass
            return [Arc(self.center,self.radius,
                        s2, e2, self.weight)]

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
    return rEq * math.tan( ((math.pi/2) - declination)/2 )

