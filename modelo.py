"""
Hacemos los modelos
"""
import glfw
import scene_graph as sg
import basic_shapes as bs
import transformations as tr
import easy_shaders as es
import numpy as np
from OpenGL.GL import *
import csv
import random
from typing import List
import easy_shaders as es

#Clase para la implementación del fondo

class Fondo(object):

    def __init__(self, pos, orientation):
        fondo = es.toGPUShape(bs.createTextureQuad("liana.jpg", 1, 1), GL_REPEAT, GL_LINEAR)
        fondoTransform= tr.uniformScale(2)
        self.model = fondo
        self.tra = fondoTransform
        self.pos = pos
        self.orientation = orientation
        
    def draw(self, pipeline):
        self.tra= tr.matmul([tr.translate(0, self.pos, 0),tr.uniformScale(2), tr.scale(1, self.orientation, 1)])
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.tra)
        pipeline.drawShape(self.model)
        
    def update(self, dt):
        self.pos -= dt
   
#Clase para la implementación para la bajada del fondo     
class Fondobaja(object):
    fondo: List['fondo']
    def __init__(self):
        self.fondo = [Fondo(0, 1),Fondo(2, -1)] #se crean fondos en una lista 
        self.count=1
        
    def create_fondo(self): #agrega fondos a la lista dependiendo de la posición de los fondos anteriores
        if self.fondo[self.count].pos<=0:
            if self.count%2==0:
                self.fondo.append(Fondo(2,-1))
            else:
                self.fondo.append(Fondo(2,1))
            self.count+=1
            
            
    def draw(self, pipeline):
        for k in self.fondo:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.fondo:
            k.update(dt)

#Clase para la implementación del pasto inicial
class Pasto(object):

    def __init__(self):
        pasto = es.toGPUShape(bs.createTextureQuad("Pasto.png", 1, 1), GL_REPEAT, GL_LINEAR)
        pastoTransform= tr.uniformScale(2)
        self.model = pasto
        self.tra = pastoTransform
        self.pos = 0.1
        

    def draw(self, pipeline):
        self.tra= tr.matmul([tr.translate(0, self.pos, 0),tr.uniformScale(2), tr.scale(-1, -1, 1)])
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.tra)
        pipeline.drawShape(self.model)
        
    def update(self, dt):
        self.pos -= dt   
        
#Clase para la implementación del mono
class Mono(object):

    def __init__(self, texture):
        self.texture = texture
        monop = es.toGPUShape(bs.createTextureQuad(self.texture, 1, 1), GL_REPEAT, GL_LINEAR)
        self.model = monop
        self.pos_x = 0
        self.pos_y = -0.7
        self.pos=-0.7
        monopTransform= tr.matmul([tr.translate(self.pos_x, self.pos_y, 0), tr.uniformScale(0.5)])
        self.tra = monopTransform
        self.winner = False #aun no gana
        self.loser = False #aun no pierde  
    
        
    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.tra)
        pipeline.drawShape(self.model)
     
    #Para que se mueva a la izquierda
    def move_left(self):
        if self.pos_x == 0:
            self.pos_x = -0.7
        elif self.pos_x == 0.7:
            self.pos_x = 0   
        self.tra= tr.matmul([tr.translate(self.pos_x, self.pos_y, 0), tr.uniformScale(0.5)])
                      
    #Para que se mueva a la derecha
    def move_right(self):
        if self.pos_x == 0:
            self.pos_x = 0.7
        elif self.pos_x == -0.7:
            self.pos_x = 0
        self.tra= tr.matmul([tr.translate(self.pos_x, self.pos_y, 0), tr.uniformScale(0.5)])
        
    #Para saltar     
    def update(self):
        if self.pos_y<0.4:
            self.pos=self.pos_y
            self.pos_y += 0.6
            self.tra= tr.matmul([tr.translate(self.pos_x, self.pos_y, 0), tr.uniformScale(0.5)])
    
    #Para saltar hacia una barra 
    def jump(self, barra: 'BarraCreator'):  
        for b in barra.copy:
            #si la barra esta más abajo que el mono en y, en la misma posicion en x, la barra aun no sale de la pantalla 
            #y además la barra esta sobre el punto en el que salto inicialmente el mono
            if b.pos_y <= self.pos_y  and b.pos_x == self.pos_x and b.pos_y>-1.1 and self.pos>=b.pos_y-0.28:
                self.pos_y=b.pos_y+0.278
                self.tra= tr.matmul([tr.translate(self.pos_x, self.pos_y, 0), tr.uniformScale(0.5)])
                #si el mono bajo mucho pierde
                if self.pos_y<-0.7 and len(barra.copy)>1: 
                    self.loser=True
                    return
            #se van sacando de la lista las barras que ya bajaron
            if b.pos_y<=-0.98 :
                barra.copy.remove(b)
            #si no quedan barras que mostrar gana
            if len(barra.copy)==0 :
                self.winner = True
    
#Clase para la implementación de una barra
class Barra(object):
    def __init__(self, r):
        gpu_barra = es.toGPUShape(bs.createColorQuad(0.5, 0.5, 0.5)) #creamos un cuadrado
        
        barra = sg.SceneGraphNode('barra') #generamos un nodo para el cuadrado
        barra.transform = tr.scale(0.7,0.1, 1) #lo escalamos al tamaño que queremos 
        barra.childs += [gpu_barra]

        transform_barra1 = sg.SceneGraphNode('barraTR')# generamos un nodo para el objeto barra
        transform_barra1.childs += [barra]

        self.model = transform_barra1
        self.pos_y = 1
        
        #con esto se lee el lo que traia el archivo structure.csv y coloca barras en los unos 
        if len(r)!=0:
            p=r.pop(0)
            if p[0]=="1":
                self.pos_x=-0.7
            if p[2]=="1":
                self.pos_x=0
            if p[4]=="1":
                self.pos_x=0.7   
        self.r=r
                
    def update(self, dt):
        self.pos_y -= dt
        

    def draw(self, pipeline):  
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

#Clase para la implementación de la caida de las barras 
class BarraCreator(object):
    barra: List['Barra']
    def __init__(self,r, mono):
        self.barra = [Barra(r)] #se crea una lista de barras 
        self.count = 0 #indica cual fue el indice de la ultima barra agregada 
        self.copy = self.barra[:] #una copia de la lista anterior que se encarga de eliminar las barras que cayeron
        self.mono=mono #el mono que salta en las barras
        
    def create_barra(self):
        if self.mono.loser: #si el mono pierde no se generan más barras 
            return 
        #se agregan barras a la lista, en funcion al "r" de la ultima barra agregada, es decir las barras que aun no son creadas
        elif self.barra[self.count].pos_y<=0.3 and len(self.barra[self.count].r)>0:
            self.barra.append(Barra(self.barra[self.count].r))
            self.copy=self.barra[:]
            self.count+=1
                   
            
    def draw(self, pipeline):
        for k in self.barra:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.barra:
            k.update(dt)