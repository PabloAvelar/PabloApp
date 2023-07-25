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
import youtube_dl
import re
# from tkinter import filedialog

class App:
    def __init__(self, link, path) -> None:
        """
        Este activará la barra de carga indeterminada con multihilo
        """
        self.link = link
        self.path = path

        if "facebook.com" in self.link:
            self.facebook()
        elif "instagram.com" in self.link:
            self.instagram()
        else:
            raise ValueError("Link inválido")


    def facebook(self):
        """
        Algorithm for Facebook videos
        """
        name = "".join(re.findall('\d{15}', self.link))
        options = {
            'outtmpl': f'{self.path}/{name}.mp4'
        }

        with youtube_dl.YoutubeDL(options) as ytdl:
            ytdl.download([self.link])

    def instagram(self):
        """
        Algorithm for instagram videos
        """
        pass



    # def download(link:str) -> bool:
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

        # raise NotImplementedError
