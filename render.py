#!/usr/bin/python

import pygame
from geometry import *

class PygameRender:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 480)) 

    def render(self,e):
        if isinstance(e,Arc):
            pygame.draw.arc(self.window,(255,255,255),
                    pygame.Rect(320-e.radius,240-e.radius,2*e.radius,2*e.radius),
                    e.start,e.stop,e.weight)
        elif isinstance(e,Circle):
            pygame.draw.circle(self.window,(255,255,255),
                    (int(320-e.center[0]),int(240-e.center[1])),
                               int(e.radius),int(e.weight))
        pygame.display.flip() 
