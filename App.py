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
from bs4 import BeautifulSoup as BS

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
        elif "youtube.com" in self.link:
            self.youtube()
        else:
            raise ValueError("Link inválido")


    def facebook(self) -> None:
        """
        Algorithm for Facebook videos
        """

        # Because YouTubeDL cannot download reels from facebook,
        # web scraping will be the solution, replacing "www" with "m" from the given link.
        if 'reel' in self.link:
            self.link = self.link.replace("www", "m")
            
            url_reel = requests.get(self.link)
            content = url_reel.content

            
            return
        name = "".join(re.findall('\d{15}', self.link))
        options = {
            'outtmpl': f'{self.path}/{name}.mp4'
        }

        with youtube_dl.YoutubeDL(options) as ytdl:
            ytdl.download([self.link])
  
    def instagram(self) -> None:

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
        
    def youtube(self) -> None:
        """
        Algorithm for YouTube videos.
        In this case, the algorithm will perform a web scrape to a webpage that provides those
        URL videos to be downloaded. It extracts the first link from the that webpage
        in order to download the video with the highest quality possible.

        This may change in the future. 

        This webpage is: https://10downloader.com/
        """

        # Replacing "you" (from 'youtube.com') with "000" to be redirect to the tool webpage.
        url = re.sub(r'[www]?(you)', '000', self.link)

        # Sending a request to the tool webpage and getting its content.
        tool_website = requests.get(url)
        content = tool_website.text

        # Beautiful Soup will be used for scrape the content
        soup = BS(content, 'lxml')

        # Getting the first downloable link (The Highest Quality)
        tag_highest_quality = soup.find_all('a', 'downloadBtn')[0]
        url_to_download = tag_highest_quality.get('href')

        # Getting the filename and making it a valid filename
        invalid = '<>:"/\|?* '
        filename = tag_highest_quality.get('download')
        for char in invalid:
            filename = filename.replace(char, '')

        # Sending another request to the source URL video
        download_url = requests.get(url_to_download, stream=True)

        # Downloading the video from its source URL
        try:
            with open(f'{self.path}/{filename}.mp4', 'wb') as video:
                for data in download_url.iter_content(chunk_size=None):
                    video.write(data)
        except Exception as e:
            print('Error al descargar el video: ', e)
        finally:
            print("Proceso terminado.")
