#!/usr/bin/python

import cairo
from geometry import *

class CairoRender:
    def __init__(self):
        size = Point(800,800)
        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24,size.x,size.y)
        self.ctx = cairo.Context(self.surf)
        # fill everyting with white
        self.ctx.new_path()
        self.ctx.set_source_rgb(0.9,0.9,0.9)
        self.ctx.rectangle(0,0,size.x,size.y)
        self.ctx.fill()  # fill current path

    def render(self,e):
        self.ctx.set_source_rgb(0,0.0,0.0)
        self.ctx.set_line_width(e.weight)
        if isinstance(e,Arc):
            # draw a circle in the center
            self.ctx.new_path()
            self.ctx.arc(400+e.center.x,400+e.center.y,
                         e.radius,e.start,e.stop)
            self.ctx.stroke()  # stroke current path
        elif isinstance(e,Circle):
            self.ctx.new_path()
            self.ctx.arc(400+e.center.x,400+e.center.y,
                         e.radius,0,2*math.pi)
            self.ctx.stroke()
        elif isinstance(e,Line):
            self.ctx.new_path()
            start = e.start_point()
            end = e.stop_point()
            self.ctx.move_to(400+start.x,400+start.y)
            self.ctx.line_to(400+end.x,400+end.y)
            self.ctx.stroke()

    def output(self,path):
        # save to PNG
        self.surf.write_to_png(path)


