# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 13:49:45 2023

@author: Avelar
"""

#"Estamos mejorando: C:/Users/Avelar/Documents/portafolio\python/aplicaciones/pabloapp/pabloapp_optimizada_2"


"""


Aquí definiremos en qué app arrancar:
    Facebook
    Instagram
    YouTube
    
En este caso, arrancaremos con Facebook al iniciar el programa.

Aquí se crearán las interfaces gráficas y así poder cambiarlas dependiendo
la aplicación, sin cerrar procesos o algo así. Así sin cerrar ventanas y eso

"""

import tkinter as tk
from tkinter import ttk
import SocialMedia as sm
import os

class UI(tk.Tk):
    def __init__(self, title, size):
        # Main setup
        super().__init__()

        _x_win = (self.winfo_screenwidth() // 2) - (size[0]//2)
        _y_win = (self.winfo_screenheight() // 2) - (size[1]//2)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}+{_x_win}+{_y_win}')
        
        # Recursos #
        self.bg_color = "#1e1e1e"
        self.frame_color = "#292929"

        self.resources = {
            "header": tk.PhotoImage(file='img/logo/pabloapp_texto.png'),
            "logo_fb": tk.PhotoImage(file='img/redes/fblogo.png'),
            "logo_ig": tk.PhotoImage(file='img/redes/iglogo.png'),
            "logo_yt": tk.PhotoImage(file='img/redes/ytlogo.png'),
            "open": tk.PhotoImage(file='img/botones/abrir.png'),
            "download": tk.PhotoImage(file='img/botones/descargar.png'),
            "socialmedia": tk.PhotoImage(file='img/botones/redes.png')
        }
        
        
        # self.resizable(False, False)
        self.iconbitmap('img/logo/icono_app.ico')
        
        
        # Creando el menú de la ventana
        self.menu = Menu(self)

        # Configuraciones
        self.config(bg=self.bg_color, menu=self.menu)

        # El header de la app
        self.header = Header(self)

        # Formulario para descargar el contenido
        self.form = Form(self)

        # El footer de la app
        self.footer = Footer(self)

        # El frame de la derecha con las apps
        self.apps = Apps(self)

        # Arrancar
        self.mainloop()

        

    
    @property
    def path(self) -> str:
        """ Devuelve: la ruta donde se descargan los videos -> str"""
        directory = os.getcwd()+"\\Downloads" # Es el directorio por defecto DONDE ESTÁ UBICADO EL PROGRAMA
        with open(os.getcwd()+"\\dir\\dir.txt", "w+") as f:
            if len(f.read()) == 0:
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

    def open_in_explorer(self) -> None:
        """ Abre el directorio en el explorador de archivos """
        os.startfile(self.path)

class Menu(tk.Menu):
    """
    Este es el menú desplegable de la ventana
    """

    def __init__(self, parent):
        super().__init__(parent)
        
        # Creando secciones del menú
        self.create_section()
        
    def create_section(self):
        # Asignamos una sección con cascada
        tools = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Configuración", menu=tools)
        
        # Creamos elementos para ese menú
        tools.add_command(label="Abrir ruta de descargas", command=lambda:self.open_in_explorer())
        tools.add_command(label="Cambiar ruta de descargas", command=lambda:print("Cambiar ruta"))
        tools.add_command(label="Acerca de", command=lambda:print("Acerca de"))



class Form(ttk.Frame):
    """
    Muestra en la interfaz gráfica un campo de texto y un botón
    para que el usuario ingrese el link de su video y pueda
    iniciar su descarga.

    Aquí se detectará si el link es de:
    -Facebook
    -Instagram
    -YouTube

    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # self.config(bg=parent.frame_color) #bg=parent.bg_color, , width=150, height=_y*4.2
        # self.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.15, anchor="c")
        self.grid(row=1, column=1)
        
        self.create_widgets()

    def create_widgets(self):
        # Creamos el campo de texto para que el usuario ingrese el link
        url = tk.StringVar()
        entry = tk.Entry(self, textvariable=url)
        entry.config(width=50, font=("Open Sans", 12), borderwidth=10, relief=tk.FLAT) #int((self.w_win*0.05))
        entry.grid(row=1, column=1, columnspan=3, padx=15, pady=20)

        # Creamos un botón para que el usuario comience su descarga
        def thing():
            pass
        img_download = tk.PhotoImage(file='img/botones/online/download.png')
        btn_download = tk.Button(self, image=img_download, command=thing)
        btn_download.config(borderwidth=0, bg=self.parent.frame_color, activebackground=self.parent.frame_color, cursor="hand2")
        btn_download.image = img_download
        btn_download.grid(row=2, column=2, pady=10)

class Apps(ttk.Frame):
    """
    Muestra en la interfaz gráfica los botones
    para cambiar de aplicación.
    Returns
    -------
    None
    """
    def __init__(self, parent):
        super().__init__(parent)
        # self.config(bg=parent.frame_color)
        self.grid(row=1, column=0)

        _x = 1_000 * 0.04
        _y = 600 / 3
        
        fb_app = tk.Label(self,
                               image=parent.resources["logo_fb"], 
                               bg=parent.bg_color
                               )
        fb_app.place(x=_x, y=_y)

        ig_app = tk.Label(self,
                               image=parent.resources["logo_ig"],
                               bg=parent.bg_color
                               )
        _y += 100
        ig_app.place(x=_x, y = _y)

        yt_app = tk.Label(self,
                               image=parent.resources["logo_yt"],
                               bg=parent.bg_color
                               )
        _y += 100
        yt_app.place(x=_x, y = _y)

class Header(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=0, column=1)
        logo = tk.Label(self,
                 image=parent.resources["header"],
                 bg=parent.bg_color)
        logo.pack()

class Footer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # self.config(bg=parent.frame_color)
        self.grid(row=2, column=1, columnspan=3)

        tk.Label(self, text="hola").pack()

if __name__ == '__main__':
    UI('PabloApp', (1_000, 600))