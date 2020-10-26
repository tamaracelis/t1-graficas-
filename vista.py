"""
Visualizador.
"""

import csv
import glfw
from OpenGL.GL import *
import numpy as np
import sys

import transformations as tr
import easy_shaders as es

from modelo import Mono, Fondo, Barra, BarraCreator, Fondobaja, Pasto
from controller import Controller

def monkey_jump(structure):
    if __name__ == '__main__':

        # Initialize glfw
        if not glfw.init():
            sys.exit()

        width = 700
        height = 700

        window = glfw.create_window(width, height, 'Saltarin', None, None)

        if not window:
            glfw.terminate()
            sys.exit()

        glfw.make_context_current(window)

        # Creamos el controlador
        controlador = Controller()

        # Connecting the callback function 'on_key' to handle keyboard events
        glfw.set_key_callback(window, controlador.on_key)

        # Creating shader programs for textures and for colors
        texture = es.SimpleTextureTransformShaderProgram()
        color = es.SimpleTransformShaderProgram()
    

        # Setting up the clear screen color
        glClearColor(0.15, 0.15, 0.15, 1.0)

   
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND )

        # Creamos los objetos
        fondo = Fondobaja()
        mono = Mono("parado.png")
        pasto=Pasto()
        
        # Leemos el csv
        def leer(estructura):
                with open(estructura) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    r=[]
                    for row in csv_reader:
                        r.append(row[0])
                return r
        r=leer(structure)
        #creamos las barras a partir del csv
        barra = BarraCreator(r, mono)
            
        controlador.set_model(mono)
        controlador.set_barra(barra)
        controlador.set_fondo(fondo)

    
        t0=0
        while not glfw.window_should_close(window):

            # Using GLFW to check for input events
            glfw.poll_events()
            
            # Filling or not the shapes depending on the controller state
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            
            
            # Clearing the screen in both, color and depth
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Dibujamos
            ti = glfw.get_time()
            dt = ti - t0
            t0 = ti
            
            #dibujamos el fondo y hacemos que se mueva
            fondo.create_fondo()
            fondo.update(0.2 * dt)
            fondo.draw(texture)
            
            #Dibujamos el pasto al al comienzo y se comienza a mover
            pasto.update(0.2*dt)
            pasto.draw(texture)
            
            #Dibujamos las barras
            barra.create_barra()  
            barra.update(0.4 * dt)
            
            #se revisan las barras creadas para que el mono salte en ellas y se dibuja el mono
            mono.jump(barra) 
            mono.draw(texture)
            
            #se dibujan las barras
            barra.draw(color)
            
            #si el mono perdió, se pone la pantalla como game over 
            if mono.loser:
                mono=Mono("gameover.png")
                mono.loser=True
                monoTransform=  tr.uniformScale(1.7)
                mono.tra = monoTransform
            
            #si el mono ganó, se indica la victoria 
            elif mono.winner :
                mono=Mono("victory2.png")
                monoTransform=  tr.uniformScale(1.7)
                mono.tra = monoTransform
            
        

            # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
            glfw.swap_buffers(window)

        glfw.terminate()
