#!/usr/bin/python
import math
from geometry import *
from render import CairoRender

# Create lines for plate with given parameters
class Plate:
    """
    Create the circles and lines for a plate for the given latitude,
    angle of the ecliptic, and plate radius.
    Ecliptic and latitude are given in radians.
    """
    def __init__(self, radius, latitude, ecliptic):
        self.radius = float(radius)
        self.lat = float(latitude)
        self.tilt = float(ecliptic)

    def tropics(self):
        "Generate circles for the tropics and equator."
        self.rCap = self.radius
        self.rEq = self.rCap * math.tan(math.pi/4.0 - self.tilt/2.0)
        self.rCan = self.rEq * math.tan(math.pi/4.0 - self.tilt/2.0)
        self.capricorn = Circle(Point(0,0),self.rCap,weight=4)
        self.equator = Circle(Point(0,0),self.rEq,weight=2)
        self.cancer = Circle(Point(0,0),self.rCan,weight=2)
        return [self.capricorn, self.cancer, self.equator]

    def almucantars(self):
        "Generate curves for the almucantars."
        def almucantar(declination,weight):
            "Generate an almucantar for the given declination"
            rl = fundamental(self.rEq,declination+((math.pi/4)-self.lat))
            ru = -fundamental(self.rEq,declination-((math.pi/4)-self.lat))
            c = (rl+ru)/2
            r = abs(ru - c)
            return Circle(Point(0,-c),r,weight)
        # create circles
        a = [almucantar(math.radians(d),2) for d in range(0,90,10)]
        a = a + [almucantar(math.radians(d),1) for d in range(0,80,2)]
        # clip at outer radius
        return a

    def meridians(self):
        "Generate lines for the prime meridian and right ascension."
        return []

    def azimuths(self):
        "Generate curves for the azimuths."
        return []

p = Plate(350,math.radians(0),math.radians(23))

r = CairoRender()
import time

for arc in p.tropics():
    r.render(arc)
for a in p.almucantars():
    l = a.clip(p.capricorn)
    for al in l:
        r.render(al)

r.output("plate.png")
