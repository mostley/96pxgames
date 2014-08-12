#PyGL2D - A 2D library for PyGame and PyOpenGL
#Copyright (C) 2008 - PyMike

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

import window

def line(point1, point2, color, width=1, aa=True, alpha=255.0):
    """Draw a line from point1 to point2 <- return None
    """
    
    glLineWidth(width)
    if aa:
        glEnable(GL_LINE_SMOOTH)
    glDisable(GL_TEXTURE_2D)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    glBegin(GL_LINE_STRIP)
    glVertex3f(point1[0], point1[1], 0)
    glVertex3f(point2[0], point2[1], 0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glEnable(GL_TEXTURE_2D)
    
def lines(points, color, width=1, aa=True, closed=False, alpha=255.0):
    """Draws a series of lines <- return None
    """
    
    glLineWidth(width)
    if aa:
        glEnable(GL_LINE_SMOOTH)
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_LINE_STRIP)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    for p in points:
        glVertex3f(p[0], p[1], 0)
    if closed:
        glVertex3f(points[0][0], points[0][1], 0)
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glDisable(GL_LINE_SMOOTH)
    glEnable(GL_TEXTURE_2D)

def polygon(points, color, aa=True, alpha=255.0):
    """Draw a filled polygon <- return None
    """
    
    glDisable(GL_TEXTURE_2D)
    if aa:
        glEnable(GL_POLYGON_SMOOTH)
    glColor4f(color[0]/255.0, color[1]/255.0, color[2]/255.0, alpha/255.0)
    glBegin(GL_POLYGON)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()
    glColor3f(1.0,1.0,1.0)
    glDisable(GL_POLYGON_SMOOTH)
    glEnable(GL_TEXTURE_2D)

def rect(rect, color, width=0, alpha=255.0, aa=False):
    """Draw a rect <- return None
    """
  
    points = [
        (rect[0], rect[1]),
        (rect[0], rect[3]),
        (rect[2], rect[3]),
        (rect[2], rect[1]) ]
    if not width:
        polygon(points, color, aa=aa, alpha=alpha)
    else:
        lines(points, color, width=width, aa=aa, alpha=alpha, closed=1)

def circle(pos, radius, color, alpha=255.0):
    """Draw a circle <- return None
    """
    w, x, y = color
    w = w / 255.0 if w else 0
    x = x / 255.0 if x else 0
    y = y / 255.0 if y else 0
    z = alpha / 255.0 if alpha else 0
    glDisable(GL_TEXTURE_2D)

    c = gluNewQuadric()
    glColor4f(w, x, y, z)
    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)
    gluDisk(c, 0, radius, 100, 100)
    glPopMatrix()
    glEnable(GL_TEXTURE_2D)
