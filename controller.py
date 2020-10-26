"""
Contralor de la aplicación.
"""

import glfw
import sys
from typing import Union
import easy_shaders as es
#from modelo import Monoparado, Fondo, Monoagachado, Barra, BarraCreator, Fondobaja

class Controller(object):

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
        
        #si se presiona la A el modelo se mueve a la izquierda
        if key == glfw.KEY_A and action == glfw.PRESS:
            self.model.move_left()
        
        #si se presiona la D el modelo se mueve a la derecha
        if key == glfw.KEY_D and action == glfw.PRESS:
            self.model.move_right()
            
        #si se presiona la W el modelo salta 
        if key == glfw.KEY_W and action == glfw.PRESS:
            self.model.update()
            
        
        


