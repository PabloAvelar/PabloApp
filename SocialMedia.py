# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 23:07:50 2023

Aquí se encuentra el algoritmo de descarga de videos
de facebook

@author: Avelar
"""

from App import App

class Facebook(App):

    def __repr__(cls) -> str:
        return "facebook"

class Instagram(App):
    def __repr__(cls) -> str:
        return "instagram"

class YouTube(App):

    def __repr__(cls) -> str:
        return "youtube"