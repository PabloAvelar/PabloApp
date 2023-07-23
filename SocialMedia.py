# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 23:07:50 2023

Aquí se encuentra el algoritmo de descarga de videos
de facebook

@author: Avelar
"""

from App import App
import youtube_dl

class Facebook(App):

    def __init__(self, link, path) -> None:
        super().__init__(link)
        self.link = link
        self.path = path

    def download(self) -> None:
        options = {
            'outtmpl': f'{self.path}/%(id)s.mp4'
        }
        with youtube_dl.YoutubeDL(options) as video:
            video.download([self.link])

    def __repr__(self) -> str:
        return self.link

class Instagram(App):
    def __repr__(cls) -> str:
        return "instagram"

class YouTube(App):

    def __repr__(cls) -> str:
        return "youtube"