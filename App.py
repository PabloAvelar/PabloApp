# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:21:49 2023

@author: Avelar
"""

"""

De aquí van a heredar las clases:
    Facebook
    Instagram
    YouTube

"""
import os
# from tkinter import filedialog

class App:
    def __init__(self, link) -> None:
        """
        Este activará la barra de carga indeterminada con multihilo
        """
        self.link = link


    def download(link:str) -> bool:
        """

        Parameters
        ----------
        link : str
            El link del video a descargar.

        Returns
        -------
        bool
            Regresa True si el video logró descargarse con éxito.

        """

        raise NotImplementedError
