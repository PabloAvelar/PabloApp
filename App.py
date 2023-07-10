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

    @property
    def path(cls) -> str:
        """ Devuelve: la ruta donde se descargan los videos -> str"""

        directory = os.getcwd()+"\\Downloads" # Es el directorio por defecto
        with open(os.getcwd()+"\\Downloads\\dir.txt", "w+") as f:
            if len(f.read) == 0:
                # Si no hay nada, se pone el directorio por defecto
                # Esto se suele hacer cuando es la primera vez que se abre el programa.
                f.write(directory)
            else:
                # Si ya tenemos el directorio en un archivo, cambiamos el valor
                # de "directory", que será lo que devolverá esta función.
                directory = f.read()
            
            f.close()

        return directory
    
    @path.setter
    def path(self, new_path) -> None:
        """ Reescribe la nueva ruta para los videos descargados 

            Recibe: filedialog.askdirectory() -> str
            Devuelve: nada
        """
        if len(new_path) > 0:
            with open(os.getcwd()+"\\Downloads\\dir.txt", "w") as f:
                f.write(new_path)
                f.close()

    @staticmethod
    def open_in_explorer() -> None:
        """ Abre el directorio en el explorador de archivos """
        os.startfile(App.path)


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
