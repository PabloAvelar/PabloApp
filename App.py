# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:21:49 2023

@author: Avelar
"""

"""

Downloader for PabloApp
Algorithms to download the content from:
    Facebook
    YouTube
    Instagram
"""
import re
import requests
from bs4 import BeautifulSoup as Bs
from fake_useragent import UserAgent
from tkinter import messagebox

class App:
    def __init__(self, link=None, path=None, loading_window=None) -> None:
        """
        Este activará la barra de carga indeterminada con multihilo
        """
        self.link = link
        self.path = path
        self.loading_window = loading_window

    def show_alert(self, type_, error=None):
        if type_ == 'success':
            messagebox.showinfo('Aviso', 'El video ha sido descargado.')
        elif type_ == 'error':
            messagebox.showerror('Error', 'No se pudo descargar el video: '+error)

    def download(self) -> None:
        """
        Returning True if the download has finished
        """
        if "facebook.com" in self.link:
            self.facebook()             
        elif "instagram.com" in self.link:
            self.instagram()
        elif "youtube.com" in self.link:
            self.youtube()
        else:
            self.loading_window.destroy()
            raise ValueError("Link inválido")

    def facebook(self) -> None:
        """
        Algorithm for Facebook videos

        We have to change the User-Agent in order not to Facebook can block us and treat us
        like a robot.
        """

        headers = {
            'User-Agent': UserAgent().chrome
        }

        s = requests.Session()
        response = s.get(self.link, headers=headers)
        # with open('mierda.html', 'w', encoding='utf-8') as f:
        #     f.write(Bs(response.content, 'lxml').prettify())
        # return
        source = re.search(r'src&quot;:&quot;(.*?)&quot;', str(response.content))
        print(source)
        if source != None:
            source = source.group(1)
            source = source.replace('\\', '').replace('&amp;', '&')
            filename = re.search(r'[=|/](\d{15})', self.link).group(1)
            video_source = s.get(source, stream=True)

            try:
                with open(f'{self.path}/{filename}.mp4', 'wb') as video:
                    for data in video_source.iter_content(chunk_size=None):
                        video.write(data)
                        print("Downloading...")
                    print("Se descargó el video!")
                    self.show_alert('success')
            except Exception as e:
                print("Error al descargar el video: "+e)
                self.show_alert('error', e)
            finally:
                print("Proceso FB terminado.")
                self.loading_window.destroy()
        else:
            self.loading_window.destroy()
            self.show_alert('error', 'El video no es público.')
            raise ValueError("Couldn't find the video source URL")

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
            self.loading_window.destroy()
            self.show_alert('error', 'No se pudo acceder al video.')
            raise requests.exceptions.ConnectionError
            
        if url_video != None:
            try:
                with open(f'{self.path}/{getName()}.mp4', 'wb') as video:
                    for data in url_video.iter_content(chunk_size=None):
                        video.write(data)
                        print("Writing data into the video...")
                print("The download is finished!")
                self.show_alert('success')
            except Exception as e:
                print("Error: the download has failed: ", e)
                self.show_alert('error', e)
            finally:
                self.loading_window.destroy()
        else:
            self.loading_window.destroy()
            self.show_alert('error', 'No se pudo acceder al video.')
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
        # url = re.sub(r'[www]?(you)', '000', self.link)

        # Sending a request to the tool webpage and getting its content.
        tool_website = 'https://10downloader.com/download'

        # Creating a Session object in order to make multiple requests
        s = requests.Session()
        response = s.get(tool_website, params={'v': self.link})
        content = response.text

        # Beautiful Soup will be used for scrape the content
        soup = Bs(content, 'lxml')

        # Getting the first downloable link (The Highest Quality)
        try:
            tag_highest_quality = soup.find_all('a', 'downloadBtn')[0]
            url_to_download = tag_highest_quality.get('href')
        except IndexError:
            print("Couldn't find the quality list")
            self.loading_window.destroy()
            self.show_alert('error', 'No se pudo acceder al video')
            return

        # Getting the filename and making it a valid filename
        invalid = '<>:"/\|?* '
        filename = tag_highest_quality.get('download')
        for char in invalid:
            filename = filename.replace(char, '')

        # Sending another request to the source URL video
        download_url = s.get(url_to_download, stream=True)

        # Downloading the video from its source URL
        try:
            with open(f'{self.path}/{filename}.mp4', 'wb') as video:
                for data in download_url.iter_content(chunk_size=None):
                    video.write(data)
                self.show_alert('success')
        except Exception as e:
            print('Error al descargar el video: ', e)
            self.show_alert('error', e)
        finally:
            print("Proceso terminado.")
            self.loading_window.destroy()
