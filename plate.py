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

    def almucantar(self,declination,weight):
        "Generate an almucantar for the given declination"
        rl = fundamental(self.rEq,declination+((math.pi/2)-self.lat))
        ru = -fundamental(self.rEq,declination-((math.pi/2)-self.lat))
        c = (rl+ru)/2
        r = abs(ru - c)
        return Circle(Point(0,-c),r,weight)

    def tropics(self):
        "Generate circles for the tropics and equator."
        self.rCap = self.radius
        self.rEq = self.rCap * math.tan(math.pi/4.0 - self.tilt/2.0)
        self.rCan = self.rEq * math.tan(math.pi/4.0 - self.tilt/2.0)
        self.capricorn = Circle(Point(0,0),self.rCap,weight=4)
        self.equator = Circle(Point(0,0),self.rEq,weight=2)
        self.cancer = Circle(Point(0,0),self.rCan,weight=2)
        self.horizon = self.almucantar(0,0)
        return [self.capricorn, self.cancer, self.equator]

    def almucantars(self):
        "Generate curves for the almucantars."
        # create circles
        a = [self.almucantar(math.radians(d),2) for d in range(0,90,10)]
        a = a + [self.almucantar(math.radians(d),1) for d in range(0,80,2)]
        # clip at capricorn
        return a

    def meridians(self):
        "Generate lines for the prime meridian and right ascension."
        return []

    def azimuths(self):
        "Generate curves for the azimuths."
        # compute zenith
        zenith = fundamental(self.rEq,self.lat)
        nadir = fundamental(self.rEq,math.pi+self.lat)
        cline = (zenith+nadir)/2
        yaz = zenith - cline
        print zenith, nadir, cline
        def azimuth(az,weight):
            "Generate a curve for the given azimuth"
            left = yaz * math.tan(az)
            r = yaz / math.cos(az)
            return Circle(Point(-left,cline),r,weight)
        a = [azimuth(math.radians(d),0.5) for d in range(0,361,10)]
        # clip at horizon
        return a #sum([x.clip(self.horizon) for x in a],[])


for lat in range(0,91,9):
    p = Plate(350,math.radians(lat),math.radians(23))
    r = CairoRender()
    for arc in p.tropics():
        r.render(arc)
    for a in p.almucantars():
        l = a.clip(p.capricorn)
        for al in l:
            r.render(al)
    for a in p.azimuths():
        l = a.clip(p.capricorn)
        for al in l:
            r.render(al)
    r.output("plate{0:02d}.png".format(lat))
