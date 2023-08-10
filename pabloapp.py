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
import threading

class UI(ctk.CTk):
    def __init__(self, title, size):
        # Main setup
        super().__init__(fg_color="#1e1e1e")

        # App instance
        self.app = App()

        self.download_thread = None

        # This shows the window in the middle of the screen
        _x_win = (self.winfo_screenwidth() // 2) - (size[0]//2)
        _y_win = (self.winfo_screenheight() // 2) - (size[1]//2)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}+{_x_win}+{_y_win}')
        self.minsize(size[0], size[1])

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

        # TopLevel for the Loading Window
        self.loading_window = None

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

    def open_loading_window(self) -> None:

        if self.loading_window is None or not self.loading_window.winfo_ismapped():
            # Creating a frame to show the loading bar
            self.loading_window = LoadingWindow(self)
            # Showing widgets from the loading window
            self.loading_window.showing_frame()
            
            # Passing this frame to the App downloader to be destroyed as soon as it finish its process
            self.app.loading_window = self.loading_window

    def startDownload(self, url:str, valid_url:bool) -> None:
        # Re-assigning values to the App instance.
        self.app.link = url
        self.app.path = self.path

        # Checking if the URL is valid in order to create the toplevel
        if valid_url:
            if self.loading_window is None or not self.loading_window.winfo_ismapped():
                # Initializing the download thread
                self.download_thread = threading.Thread(target=self.app.download, daemon=True)
                self.download_thread.start()
                print("hilo nuevo")

                # Initializing the Loading Window
                self.open_loading_window()
        

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
        """ It opens the directory where the videos are saved """
        os.startfile(path)

    def changeDirectory(self) -> None:
        """
        It changes the directory where videos will be saved
        """

        # Asking for the new directory
        new_path = tk.filedialog.askdirectory()

        # Changing the directory
        self.parent.path = new_path
        
    @property
    def checkTread(self):
        return self.parent.app.flag

    def create_section(self):
        # Asignamos una sección con cascada
        tools = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Configuración", menu=tools)
        
        # Creamos elementos para ese menú
        tools.add_command(label="Abrir ruta de descargas", command=lambda:Menu.open_in_explorer(self.parent.path))
        tools.add_command(label="Cambiar ruta de descargas", command=lambda:self.changeDirectory())
        tools.add_command(label="Acerca de", command=lambda:print("Acerca de"))
        tools.add_command(label="Is thread alive", command=lambda:print("flag: ", self.checkTread))

class LoadingWindow(ctk.CTkFrame):
    """
    The loading frame shows when the user press click on the Download button
    or when the user press Enter.

    This window only appearse when the URL is correct.
    """

    def __init__(self, main_window):
        super().__init__(main_window, fg_color='#1e1e1e')
        self.parent = main_window
        
        self.configure(width=self.parent.winfo_width(), height=self.parent.winfo_height())
        
        self.displayWidgets()
        # This make the frame the same size as the main window
        self.parent.bind('<Configure>', lambda e:self.setSize())

    class LoadingBar(ctk.CTkProgressBar):
        def __init__(self, parent):
            super().__init__(parent, orientation="horizontal")
            self.configure(
                mode="determinate",
                width=350,
                height=15,
                progress_color="green",
                indeterminate_speed=0.13
            )

            # self.pack(expand=True)
            self.place(relx=0.5, rely=0.6, anchor='center')
            
        def __repr__(self):
            return "Loading bar class"

    def setSize(self):
        self.configure(width=self.parent.winfo_width(), height=self.parent.winfo_height())

    def displayWidgets(self):
        font = ctk.CTkFont(
            family="Arial",
            size=25,
            weight="bold"
        )

        # Labels #
        label = ctk.CTkLabel(self, text="Tu video está siendo descargado...")
        label.configure(
            text_color=self.parent.fg_color,
            font=font
        )
        error = ctk.CTkLabel(self, text='')
        error.configure(
            text_color=self.parent.fg_color,
            font = self.parent.subtitle_font
        )

        # Button #

        return_button = ctk.CTkButton(self)
        return_button.configure(
            fg_color="#900000",
            hover_color="#760000",
            text_color=self.parent.fg_color,
            font=self.parent.title_font,
            text="Regresar",
            corner_radius=8,
            border_spacing=13,
            cursor=None
        )

        # Alert Images

        check_img = ctk.CTkImage(light_image=Image.open('img/alerts/check.png'), size=(128,128))
        error_img = ctk.CTkImage(light_image=Image.open('img/alerts/error.png'), size=(128,128))

        # Label for these images
        check_label = ctk.CTkLabel(self, text='', fg_color='transparent', image=check_img)
        error_label = ctk.CTkLabel(self, text='', fg_color='transparent', image=error_img)

        # Placing widgets
        label.place(relx=0.5, rely=0.5, anchor='center')
        # error.place(relx=0.5, rely=0.6, anchor='center')
        # return_button.place(relx=0.5, rely=0.8, anchor='center')
        # alert_label.place(relx=0.5, rely=0.8, anchor='center')

        # These widgets will be changed from App
        self.parent.app.alert_txt = label
        self.parent.app.error_txt = error
        self.parent.app.return_button = return_button
        self.parent.app.check_label = check_label
        self.parent.app.error_label = error_label

        
        self.loading_bar = self.LoadingBar(self)
        self.loading_bar.start()

        self.parent.app.loading_bar = self.loading_bar

    def showing_frame(self):
        self.place(x=0, y=0)
        

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

        self.valid_url = False
        self.toplevel = False
        
        self.create_widgets()

    # def download(self, url) -> None:
    #     # Re-assigning values to the App instance.
    #     self.parent.app.link = url
    #     self.parent.app.path = self.parent.path

    #     # Checking if the URL is valid in order to create the toplevel
    #     if self.valid_url:
    #         # Initializing the download thread
    #         self.parent.download_thread = threading.Thread(target=self.parent.app.startDownload, daemon=True)
    #         self.parent.download_thread.start()

    #         # Initializing the Loading Window
    #         self.parent.open_loading_window()

    def create_widgets(self):

        # Form label
        txt = ctk.CTkLabel(self, text="Ingresa el link de tu video")
        txt.configure(
                   text_color=self.parent.fg_color,
                   font=self.parent.title_font
                   )
        txt.pack(pady=18)

        # Creating the Entry to request a link
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


        # Download button
        btn_download = ctk.CTkButton(self)
        btn_download.configure(
                            fg_color="#33b249",
                            hover_color="#2D9A40",
                            text_color=self.parent.fg_color,
                            font=self.parent.title_font,
                            text="Descargar",
                            corner_radius=8,
                            border_spacing=13,
                            cursor=None,
                            command=lambda:self.parent.startDownload(url.get(), self.valid_url)
                            )
        btn_download.pack(side="left", padx=18, pady=18)

        # Button color changer
        def checkURL() -> None:
            if "facebook.co" in url.get():
                self.valid_url = True
                btn_download.configure(fg_color=self.parent.fg_fb, hover_color=self.parent.fg_hover_fb)
            elif "instagram.co" in url.get():
                self.valid_url = True
                btn_download.configure(fg_color=self.parent.fg_ig, hover_color=self.parent.fg_hover_ig)
            elif "youtube.co" in url.get():
                self.valid_url = True
                btn_download.configure(fg_color=self.parent.fg_yt, hover_color=self.parent.fg_hover_yt)
            else:
                self.valid_url = False
                btn_download.configure(fg_color="#33b249")

        # This detects when the user paste their link or they press Enter
        entry.bind("<KeyRelease>", lambda event:checkURL())
        entry.bind("<Return>", lambda e:self.parent.startDownload(url.get(), self.valid_url))

class Apps(ctk.CTkFrame):
    """
    Only to show the cute icons on the left side
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
                 text_color=parent.fg_color,
                 font=parent.subtitle_font,
                 underline=True,
                 cursor="hand2"
                 )
        _disclaimer.pack(pady=5)

        _disclaimer.bind('<Button-1>', lambda e: webbrowser.open_new("https://pabloavelar.mx/"))


if __name__ == '__main__':
    UI('PabloApp', (900, 600))