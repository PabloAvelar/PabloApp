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
import requests

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

        # It'll be the source URL of the video.
        url_video = None

        # Trying to get content from the link
        def prepare_url(url):
                url = url.replace('\\/', '/')
                url = url.replace("\\u0025", "%")
                
                return url
        
        def getName():
            return "".join(re.findall(r'[l|p]/(.{11})/?', self.link))
        
        try:
            # Getting access and content
            r = requests.get(self.link)
            content = r.text

            # Getting the URL from the source of the actual video from the post
            get_url = re.findall(r'"contentUrl":"([^"]+)"', content)[0]

            # Preparing the url 
            url = prepare_url(get_url)
            url_video = requests.get(url)

        except:
            raise requests.exceptions.ConnectionError


        if url_video != None:
            try:
                with open(f'{self.path}/{getName()}.mp4', 'wb') as video:
                    for data in url_video.iter_content(chunk_size=None):
                        video.write(data)
                        print("Writing data into the video...")
                print("The download is finished!")
            except Exception as e:
                raise requests.exceptions.ContentDecodingError
        else:
            raise requests.exceptions.URLRequired