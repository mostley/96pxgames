import sys, os

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

SCREEN_SIZE = [800, 600]

def init(size, caption="PyGL2D App", flags=DOUBLEBUF, bg=(0.0, 0.0, 0.0, 0.0)):
    """Initialise pygame and pyopengl <- return None
    """
    
    global SCREEN_SIZE
    SCREEN_SIZE = size
    
    flags |= OPENGL
    
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode(SCREEN_SIZE, flags)
    
    init_gl(bg)

def begin_draw():
    """Begin drawing <- return None
    """
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    enable2D( (0, SCREEN_SIZE[0], 0, SCREEN_SIZE[1]) )

def end_draw():
    """End drawing <- return None
    """
    pygame.display.flip()

def get_size():
    """Get the size of the window <- return tuple
    """
    
    return pygame.display.get_surface().get_size()


######################################################
###################### INTERNAL ######################
######################################################

def init_gl(bg):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glClearColor(bg[0], bg[1], bg[2], bg[3])
    
def enable2D(rect):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(rect[0],rect[0]+rect[1],rect[2]+rect[3],rect[2], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_ALPHA_TEST)

