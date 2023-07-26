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
import customtkinter as ctk
from PIL import Image
from App import App
import webbrowser
import os

class UI(ctk.CTk):
    def __init__(self, title, size):
        # Main setup
        super().__init__(fg_color="#1e1e1e")

        
        # Para que la ventana aparezca en medio de la pantalla
        _x_win = (self.winfo_screenwidth() // 2) - (size[0]//2)
        _y_win = (self.winfo_screenheight() // 2) - (size[1]//2)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}+{_x_win}+{_y_win}')
        self.minsize(size[0], size[1])
        # self.maxsize(1_000, 650)

        # Recursos #
        self.bg_color = "#1e1e1e"
        self.fg_color = "#F7F7F7"
        self.fg2_color = "#008001"
        self.frame_color = "#292929"

        # Fonts
        self.title_font = ctk.CTkFont(
            family="Arial",
            size=16,
            weight="bold"
        )

        self.subtitle_font = ctk.CTkFont(
            family="Arial",
            size=13,
        )

        # Colores de cada app
        self.fg_ig = "#E4405F"
        self.fg_hover_ig = "#CB3652"

        self.fg_fb = "#1877F2"
        self.fg_hover_fb = "#186EDD"

        self.fg_yt = "#CD201F"
        self.fg_hover_yt = "#B7201F"

        self.resources = {
            "header": ctk.CTkImage(light_image=Image.open('img/logo/pabloapp_texto.png'), size=(300,90)),
            "logo_fb": ctk.CTkImage(light_image=Image.open('img/redes/fblogo.png'), size=(50,50)),
            "logo_ig": ctk.CTkImage(light_image=Image.open('img/redes/iglogo.png'), size=(50,50)),
            "logo_yt": ctk.CTkImage(light_image=Image.open('img/redes/ytlogo.png'), size=(50,50)),
            "open": ctk.CTkImage(light_image=Image.open('img/botones/abrir.png'), size=(50,50)),
            "download": ctk.CTkImage(light_image=Image.open('img/botones/descargar.png'), size=(50,50)),
            "socialmedia": ctk.CTkImage(light_image=Image.open('img/botones/redes.png'), size=(50,50))
        }
        
        
        # self.resizable(False, False)
        self.iconbitmap('img/logo/icono_app.ico')
        
        # El footer de la app con los terminos y condiciones
        self.footer = Footer(self)

        # Creando el menú de la ventana
        self.menu = Menu(self)

        # Configuraciones
        self.configure(menu=self.menu) #fg_color=self.bg_color, 


        # El header de la app
        self.header = Header(self)

        # El frame de la derecha con las apps
        self.apps = Apps(self)
        

        # Formulario para descargar el contenido
        self.form = Form(self)

        # Estilos de los frames ttk
        # _style = ttk.Style()
        # _style.configureure('TFrame', background=self.frame_color)   

        # Arrancar
        self.mainloop()

    @property
    def path(self) -> str:
        """ Devuelve: la ruta donde se descargan los videos -> str"""
        directory = os.getcwd()+"\\Downloads" # Es el directorio por defecto DONDE ESTÁ UBICADO EL PROGRAMA
        with open(os.getcwd()+"\\dir\\dir.txt", "r+") as f:
            _txt = f.read()
            if len(_txt) == 0:
                # Si no hay nada, se pone el directorio por defecto
                # Esto se suele hacer cuando es la primera vez que se abre el programa.
                f.seek(0)
                f.write(directory)
                f.truncate()
            else:
                # Si ya tenemos el directorio en un archivo, cambiamos el valor
                # de "directory", que será lo que devolverá esta función.
                directory = _txt
            
            f.close()
        return directory
    
    @path.setter
    def path(self, new_path) -> None:
        """ Reescribe la nueva ruta para los videos descargados 

            Recibe: filedialog.askdirectory() -> str
            Devuelve: nada
        """
        if len(new_path) > 0:
            with open(os.getcwd()+"\\dir\\dir.txt", "w") as f:
                f.write(new_path)
                f.close()

class Menu(tk.Menu):
    """
    Este es el menú desplegable de la ventana
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Creando secciones del menú
        self.create_section()

    @classmethod
    def open_in_explorer(cls, path:str) -> None:
        """ Abre el directorio en el explorador de archivos """
        os.startfile(path)

    def changeDirectory(self) -> None:
        """
        Cambia el directorio donde se guardarán los videos
        """

        # Abre el explorador de archivos para indicar qué directorio usar
        new_path = tk.filedialog.askdirectory()

        # Cambia la ruta
        self.parent.path = new_path
        
    def create_section(self):
        # Asignamos una sección con cascada
        tools = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Configuración", menu=tools)
        
        # Creamos elementos para ese menú
        tools.add_command(label="Abrir ruta de descargas", command=lambda:Menu.open_in_explorer(self.parent.path))
        tools.add_command(label="Cambiar ruta de descargas", command=lambda:self.changeDirectory())
        tools.add_command(label="Acerca de", command=lambda:print("Acerca de"))

class Form(ctk.CTkFrame):
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
        super().__init__(parent, fg_color=parent.frame_color, corner_radius=8)
        self.parent = parent
        self.pack(side="top", expand=True)
        
        self.create_widgets()

    def create_widgets(self):

        # Etiqueta del formulario
        txt = ctk.CTkLabel(self, text="Ingresa el link de tu video")
        txt.configure(
                    # fg_color=self.parent.frame_color,
                   text_color=self.parent.fg_color,
                   font=self.parent.title_font
                   )
        txt.pack(pady=18)

        # Creamos el campo de texto para que el usuario ingrese el link
        url = tk.StringVar()
        entry = ctk.CTkEntry(self, textvariable=url)
        _width = self.parent.winfo_width()*1.5
        entry.configure(width=_width,
                        height=45,
                        corner_radius=8,
                        text_color="#33b249",
                        font=self.parent.subtitle_font,
                        textvariable=url
                        )
        entry.pack(side="left", padx=18)


        # Creamos un botón para que el usuario comience su descarga
        btn_download = ctk.CTkButton(self)
        btn_download.configure(
                            fg_color="#33b249",
                            hover_color="#2D9A40",
                            text_color=self.parent.fg_color,
                            font=self.parent.title_font,
                            text="Descargar",
                            corner_radius=8,
                            border_spacing=13,
                            cursor="hand2",
                            command=lambda:App(url.get(), self.parent.path)
                            )
        # btn_download.image = img_download
        btn_download.pack(side="left", padx=18, pady=18)

        # Función para que el botón cambie de color
        def checkURL() -> None:
            if "facebook.co" in url.get():
                btn_download.configure(fg_color=self.parent.fg_fb, hover_color=self.parent.fg_hover_fb)
            elif "instagram.co" in url.get():
                btn_download.configure(fg_color=self.parent.fg_ig, hover_color=self.parent.fg_hover_ig)
            elif "youtube.co" in url.get():
                btn_download.configure(fg_color=self.parent.fg_yt, hover_color=self.parent.fg_hover_yt)
            else:
                btn_download.configure(fg_color="#33b249")

        # Para que el botón cambie de color si se detecta algo en la URL
        entry.bind("<KeyRelease>", lambda event:checkURL())
        entry.bind("<Return>", lambda e:App(url.get(), self.parent.path))

class Apps(ctk.CTkFrame):
    """
    Muestra en la interfaz gráfica los botones
    para cambiar de aplicación.
    Returns
    -------
    None
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=parent.frame_color, corner_radius=8)
        self.pack(side="left", fill="y", padx=10, pady=10)

        # Texto informativo sobre este frame
        text = ctk.CTkLabel(self, text="Descarga contenido de:")
        text.configure(
                    # fg_color=parent.frame_color,
                    text_color=parent.fg_color,
                    font=parent.subtitle_font
                    )
        text.pack(padx=15, pady=5, expand="yes")

        # Logos de las redes sociales
        fb_app = ctk.CTkLabel(self,
                               text=None,
                               image=parent.resources["logo_fb"]
                            #    fg_color=parent.frame_color
                               )
        fb_app.pack(padx=15, pady=30)

        ig_app = ctk.CTkLabel(self,
                               text=None,
                               image=parent.resources["logo_ig"]
                            #    fg_color=parent.frame_color
                               )
        ig_app.pack(padx=15, pady=30)

        yt_app = ctk.CTkLabel(self,
                               text=None,
                               image=parent.resources["logo_yt"]
                            #    fg_color=parent.frame_color
                               )
        yt_app.pack(padx=15, pady=30)

class Header(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=parent.frame_color, corner_radius=8)

        # self.grid(row=0, column=1)
        self.pack(side='top', fill="x", padx=10, pady=10)
        logo = ctk.CTkLabel(self,
                 text=None,
                 image=parent.resources["header"],
                 fg_color=parent.frame_color)
        logo.pack()

class Footer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=parent.frame_color, corner_radius=8)
        # self.configure(width=900)
        self.pack(side="bottom", fill="x", padx=10, pady=10) #, fill="x"

        # Etiquetas de texto del footer
        _myname = ctk.CTkLabel(self,
                 text="Pablo Avelar Armenta",
                #  fg_color=parent.frame_color,
                 text_color=parent.fg_color,
                 font=parent.title_font
                 )
        _myname.pack(pady=5)

        _disclaimer = ctk.CTkLabel(self,
                 text="Terminos y condiciones",
                #  fg_color=parent.frame_color,
                 text_color=parent.fg_color,
                 font=parent.subtitle_font,
                 underline=True,
                 cursor="hand2"
                 )
        _disclaimer.pack(pady=5)

        _disclaimer.bind('<Button-1>', lambda e: webbrowser.open_new("https://pabloavelar.mx/"))


if __name__ == '__main__':
    UI('PabloApp', (900, 600))