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
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tkinter import messagebox
from selenium import webdriver
import time

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
        print("Download started!")
        print("Link provided: ", self.link)
        print("Path for the videos: ", self.path)

        if "facebook.com" in self.link:
            print("App: Facebook")
            self.facebook()             
        elif "instagram.com" in self.link:
            print("App: Instagram")
            self.link = self.link.replace("reels", "reel")
            self.instagram()
        elif "youtube.com" in self.link:
            print("App: YouTube")
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
        #     f.write(BeautifulSoup(response.content, 'lxml').prettify())
        # return
        source = re.search(r'src&quot;:&quot;(.*?)&quot;', str(response.content))
        print(source)
        if source != None:
            source = source.group(1)
            source = source.replace('\\', '').replace('&amp;', '&')
            filename = re.search(r'[=|/](\d{15})', self.link).group(1)
            video_source = s.get(source, stream=True)
            print("filename: ", filename)

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
        def url_cleaner(url):
            return url.replace('&amp;', "&")

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
        driver.get(self.link)

        # Tiempo para que cargue la página en el webdriver
        time.sleep(4)

        # Para hacer web scraping con la petición del webdriver
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Encuentra el tag del video y asigna un nombre al archivo del video
        video_tag = soup.find('video')
        search_filename = re.search(r'(reel|p)/(.*)/', self.link)
        if video_tag is None:
            self.show_alert('error', "No se encontró el video")

        if search_filename is None:
            self.show_alert('error', "No se pudo asignar un nombre de archivo")

        filename = search_filename.group(2) + ".mp4"

        url_video = url_cleaner(video_tag['src'])
        print("Video was found!")
        print("URL: ", url_video)
        print("Filename: ", filename)

        # Proceso de descarga del video
        try:
            r_source = requests.get(url_video)
            with open(f'{self.path}/{filename}', 'wb') as video:
                print("Direct Path: ", f'{self.path}/{filename}.mp4')
                for data in r_source.iter_content(chunk_size=None):
                    video.write(data)
                    print("Descargando...")

            print("Se ha descargado el video!")
            self.show_alert('success')

        except Exception as e:
            print("Error al descargar el video: ", e)
            self.show_alert('error', e)
        finally:
            print("Proceso IG terminado.")
            self.loading_window.destroy()


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
        soup = BeautifulSoup(content, 'lxml')

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
