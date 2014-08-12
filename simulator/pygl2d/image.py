# -*- coding: utf-8 -*-
#PyGL2D - A 2D library for PyGame and PyOpenGL
#Copyright (C) 2008 - PyMike

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import window
from math import *

WRAP = 0
FILTER = 1
MIPMAP = 2

def closest_power_of_two ( x ):
	return ( pow(2, floor ( ( log ( x ) /log ( 2.0 ) ) + 0.5 ) ) );

def next_power_of_two ( x ):
	return ( pow(2, ceil ( ( log ( x ) /log ( 2.0 ) ) ) ) );

def previous_power_of_two ( x ):
	return ( pow(2, floor ( ( log ( x ) /log ( 2.0 ) ) ) ) );

#returns closest power of 2 which is greater than x_current. Max value is texSize.
def wanted_size ( texSize, x_current ):
	x_wanted=next_power_of_two ( x_current );
	if ( x_wanted > texSize ): x_wanted = texSize;
	return ( x_wanted );

def resize ( image, texSize ):
	H1=image.get_height()
	W1=image.get_width()
	H2=wanted_size(texSize,H1)
	W2=wanted_size(texSize,W1)
	if ( H1 != H2 ) or ( H2 != W2 ):
	    dst_rect = pygame.Rect(0,0,W2,H2)
	    dest=pygame.Surface((W2,H2), 0, image)
	    dest.blit(image, (0,0), dst_rect)
	    return dest
	else:
	    return image

#Thanks Ian Mallett!
def Texture(surface,filters):
    texture = glGenTextures(1)
    Data = pygame.image.tostring(surface,"RGBA",1)
    
    glBindTexture(GL_TEXTURE_2D,texture)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,surface.get_width(),surface.get_height(),0,GL_RGBA,GL_UNSIGNED_BYTE,Data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    if filters == None:
        return texture
    
    for f in filters:
        if f == FILTER:
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        elif f == WRAP:
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        elif f == MIPMAP:
            glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE )
            gluBuild2DMipmaps(GL_TEXTURE_2D,3,surface.get_width(),surface.get_height(),GL_RGB,GL_UNSIGNED_BYTE,Data)
            if FILTER in filters:
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            else:
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return texture

#Again, thanks Ian :)
class Image:
    
    def __init__(self, filename, filters=[FILTER]):
        """Load an image for drawing. <- return None
        """
        
        #load pygame image
        if type("") is type(filename):
            image = pygame.image.load(filename)
        else:
            image = filename
        self.image = image
        
	texSize=glGetIntegerv ( GL_MAX_TEXTURE_SIZE)
	oldH= image.get_height()
	oldW= image.get_width()
	image2=resize(image,texSize)
	newH= image2.get_height()
	newW= image2.get_width()
	fracH=oldH/float(newH)
	fracW=oldW/float(newW)

        #convert to GL texture
        self.texture = Texture(image2, filters)
        
        #image dimensions
        self.width = self.w = image.get_width()
        self.height = self.h = image.get_height()
        self.size = image.get_size()
   
        #image mods
        self.rotation = 0
        self.scalar = 1.0
        self.color = [1.0, 1.0, 1.0, 1.0]
        self.ox, self.oy = self.image.get_width()/2, self.image.get_height()/2
        
        #crazy gl stuff :)
        self.dl = glGenLists(1)
        glNewList(self.dl, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1.); glVertex3f(-self.width/2.0,-self.height/2.0,0)
        glTexCoord2f(fracW, 1.); glVertex3f( self.width/2.0,-self.height/2.0,0)
        glTexCoord2f(fracW, 1.-fracH); glVertex3f( self.width/2.0, self.height/2.0,0)
        glTexCoord2f(0, 1.-fracH); glVertex3f(-self.width/2.0, self.height/2.0,0)
        glEnd()
        glEndList()
    
    def delete(self):
        glRemoveTextures([self.texture])
        del self
   
    def scale(self, scale):
        """Scale the image on a ratio of 0.0 to 1.0 <- return None
        """
        
        self.scalar = scale
    
    def rotate(self, rotation):
        """Rotate the image on a ratio of 0.0 to 360 <- return None
        """
        
        self.rotation = rotation
    
    def colorize(self, (r, g, b), a=255):
        """Color an image on a RGBA (0-255) scale. <- return None
        """
        
        self.color = (r/255.0, g/255.0, b/255.0, a/255.0)
    
    def get_width(self):
        """Returns the width of the image. <- return int
        """
        
        return self.image.get_width()*self.scalar
    
    def get_height(self):
        """Returns the height of the image. <- return int
        """
        
        return self.image.get_height()*self.scalar
    
    def get_rect(self):
        """Get the rect of the image. <- return rect.Rect
        """
        
        return rect.Rect(0, 0, self.get_width(), self.get_height())
        
    def draw(self, pos, rotation=None):
        """Draw the image to a certain position <- return None
        """
        if rotation is None: rotation = self.rotation

        glPushMatrix()
        glTranslatef(pos[0]+self.ox, pos[1] - self.oy, 0)
        glColor4f(*self.color)
        glRotatef(rotation, 0, 0, 1)
        glScalef(self.scalar, self.scalar, self.scalar)
        glCallList(self.dl)
        glPopMatrix()

    def draw_part(self, (x, y), (left, top, right, bottom)):
        glPushMatrix()
        glTranslatef(x+self.ox, y - self.oy, 0)
        glColor4f(*self.color)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scalar, self.scalar, self.scalar)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        l = left/float(self.w)
        r = right/float(self.w)
        b = 1. - top/float(self.h)
        t = 1. - bottom/float(self.h)
        w = (right-left)/2.0
        h = (bottom-top)/2.0
        glTexCoord2f(l, b); glVertex3f(-w,-h,0)
        glTexCoord2f(r, b); glVertex3f( w,-h,0)
        glTexCoord2f(r, t); glVertex3f( w, h,0)
        glTexCoord2f(l, t); glVertex3f(-w, h,0)
        glEnd()

        glPopMatrix()
