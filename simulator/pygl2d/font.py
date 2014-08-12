import image
import pygame

from OpenGL.GL import *
from OpenGL.GLU import *

class RenderText(object):
    
    def __init__(self, text, color, font):
        """Create a new font render <- return None
        """
        
        self.font = font
        self.text = text
        self.color = color
        self.ren = image.Image(self.font.render(self.text, 1, self.color))
    
    def change_text(self, text, color="default"):
        """Change the font render's text. <- return None
        """
        if text == self.text:
            return
        
        glDeleteTextures([self.ren.texture])
        del self.ren
        if color == "default":
            color = self.color
        self.color = color
        self.text = text
        self.ren = image.Image(self.font.render(self.text, 1, self.color))
    
    def draw(self, pos):
        """Draw the font rendered image. <- return None
        """
        if self.text:    
            self.ren.draw(pos)
    
    def rotate(self, rotation):
        """Rotate the font rendered image. <- return None
        """
        
        self.ren.rotate(rotation)
    
    def scale(self, scale):
        """Scale the font rendered image. <- return None
        """
        
        self.ren.scale(scale)
    
    def colorize(self, r, g, b, a):
        """Color the font rendered image. <- return None
        """
        
        self.ren.colorize(r, g, b, a)
    
    def delete(self):
        """Delete the font rendered image from the memory. <- return None
        """
        
        self.ren.delete()
        del self
    
    def get_width(self):
        """Returns the width of the font rendered image. <- return int
        """
        
        return self.ren.get_width()*self.ren.scalar
    
    def get_height(self):
        """Returns the height of the font rendered image. <- return int
        """
        
        return self.ren.get_height()*self.ren.scalar
    
