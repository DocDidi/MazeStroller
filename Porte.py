#! /usr/bin/env python3
# coding: utf-8

from var import *

class Porte:
    def __init__(self, y, x, fin = False):
        self.x = x
        self.y = y
        self.revealed = False
        self.fin = fin

    def __str__(self):
        return ("{0}\033[{1};{2}H{3}".format\
        (GREEN_TEXT,self.y+1,self.x+1,SYMBOLEPORTE))