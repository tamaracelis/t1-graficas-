"""
Contralor de la aplicación.
"""

import glfw
import sys
from typing import Union
import easy_shaders as es
#from modelo import Monoparado, Fondo, Monoagachado, Barra, BarraCreator, Fondobaja

class Controller(object):

    model: Union['Mono', None]  # Con esto queremos decir que el tipo de modelo es 'Chansey' (nuestra clase) ó None
    barra: Union['BarraCreator', None]

    def __init__(self):
        self.model = None
        self.barra = None
        self.fillPolygon = True
        self.fondo = None

    def set_model(self, m):
        self.model = m

    def set_barra(self, e):
        self.barra = e

    def set_fondo(self, f):
        self.fondo = f 
    
    def on_key(self, window, key, scancode, action, mods):
        
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        # Controlador modifica al modelo
        if key == glfw.KEY_A and action == glfw.PRESS:
            self.model.move_left()

        if key == glfw.KEY_D and action == glfw.PRESS:
            self.model.move_right()
            
        if key == glfw.KEY_W and action == glfw.PRESS:
            self.model.update()
            
        
        


