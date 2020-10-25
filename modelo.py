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
        
class Fondobaja(object):
    fondo: List['fondo']
    def __init__(self):
        self.fondo = [Fondo(0, 1),Fondo(2, -1)]
        self.count=1
        
    def create_fondo(self):
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


class Monoparado(object):

    def __init__(self):
        monop = es.toGPUShape(bs.createTextureQuad("parado.png", 1, 1), GL_REPEAT, GL_LINEAR)
        monopTransform= tr.matmul([tr.translate(0, -0.7, 0), tr.uniformScale(0.5)])
        self.model = monop
        self.tra = monopTransform
        self.pos = 0
        

    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.tra)
        pipeline.drawShape(self.model)
     
    def move_left(self):
        if self.pos == 0:
            self.tra= tr.matmul([tr.translate(-0.7, -0.7, 0), tr.uniformScale(0.5)])
            self.pos = -1
        if self.pos == 1:
            self.tra= tr.matmul([tr.translate(0, -0.7, 0), tr.uniformScale(0.5)])
            self.pos = 0
                

    def move_right(self):
        if self.pos == 0:
            self.tra = tr.matmul([tr.translate(0.7, -0.7, 0), tr.uniformScale(0.5)])
            self.pos = 1
        if self.pos == -1:
            self.tra = tr.matmul([tr.translate(0, -0.7, 0), tr.uniformScale(0.5)])
            self.pos = 0

    def move_front(self):
        if self.pos==-1:
            self.tra= tr.matmul([tr.translate(-0.7, -0.2 , 0), tr.uniformScale(0.5)])
        if self.pos==0:
            self.tra= tr.matmul([tr.translate(0, -0.2 , 0), tr.uniformScale(0.5)])
        if self.pos==1:
            self.tra= tr.matmul([tr.translate(0.7, -0.2, 0), tr.uniformScale(0.5)])
        
class Monoagachado(object):
    def __init__(self):
        monoa = es.toGPUShape(bs.createTextureQuad("agachado.png", 1, 1), GL_REPEAT, GL_LINEAR)
        monoaTransform= tr.uniformScale(0.8)
        self.model = monoa
        self.tra = monoaTransform
        
       

    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.tra)
        pipeline.drawShape(self.model)
        
class Barra(object):
    def __init__(self, r):
        gpu_barra = es.toGPUShape(bs.createColorQuad(0.5, 0.5, 0.5))
        
        barra = sg.SceneGraphNode('barra')
        barra.transform = tr.matmul([tr.scale(0.7,0.1, 1), tr.translate(0, 10, 0)])
        barra.childs += [gpu_barra]

        transform_barra1 = sg.SceneGraphNode('chanseyTR')
        transform_barra1.childs += [barra]

        self.model = transform_barra1
        self.posicion = 0
        self.pos_y = 1
        self.pos_x=1
    
        if len(r)!=0:
            p=r.pop(0)
            if p[0]=="1":
                self.pos_x=-1
            if p[2]=="1":
                self.pos_x=0
            if p[4]=="1":
                self.pos_x=1
                
        self.r=r
                
    def update(self, dt):
        self.pos_y -= dt
        

    def draw(self, pipeline):  
        self.model.transform = tr.translate(0.7 * self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

class BarraCreator(object):
    barra: List['barra']
    def __init__(self,r):
        self.barra = [Barra(r)]
        self.count=0
        
    def create_barra(self):
        if self.barra[self.count].pos_y<=0.3 and len(self.barra[self.count].r)>0:
            self.barra.append(Barra(self.barra[self.count].r))
            self.count+=1
            
            
    def draw(self, pipeline):
        for k in self.barra:
            k.draw(pipeline)

    def update(self, dt):
        for k in self.barra:
            k.update(dt)