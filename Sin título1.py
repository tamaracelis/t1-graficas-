# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 02:49:55 2020

@author: tceli
"""
import csv 

def leer(estructura):
    with open(estructura) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        r=[]
        for row in csv_reader:
            print(row)
            r.append(row)
        print(len(r))
leer("estructura.csv")