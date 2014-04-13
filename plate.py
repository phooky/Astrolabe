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
        if declination == 0.0:
            return Line(Point(0,0),Point(1,0),weight)
            print "Warning: almu at 0"
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
        a = [azimuth(math.radians(d),0.5) for d in range(-90,90,10)]
        # clip at horizon
        a  = sum([x.clip(self.horizon) for x in a],[])
        return a #sum([x.clip(self.horizon) for x in a],[])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate astrolabe plate for given latitude')
    parser.add_argument('-l','--latitude',type=float,default=45.0)
    parser.add_argument('-o','--output',default='plate{0:02.2f}.png')
    args = parser.parse_args()

    p = Plate(350,math.radians(args.latitude),math.radians(23))
    r = CairoRender()
    for arc in p.tropics():
        r.render(arc)
    for a in p.almucantars():
        l = a.clip(p.capricorn)
        for al in l:
            r.render(al)
    for a in p.azimuths():
        #r.render(a)
        l = a.clip(p.capricorn)
        for al in l:
            r.render(al)
    l1 = Line(Point(0,-100),Point(2,1).normalized())
    r.render(l1)
    l2 = Line(Point(200,0),Point(4,1).normalized())
    r.render(l2)
    l3 = l1.clip(l2)[0]
    l3.weight = 5
    r.render(l3)
    r.output(args.output.format(args.latitude))
