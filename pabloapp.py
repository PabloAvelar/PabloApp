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
from tkinter.font import Font
import SocialMedia as sm
import webbrowser
import os

class UI(tk.Tk):
    def __init__(self, title, size):
        # Main setup
        super().__init__()

        
        # Para que la ventana aparezca en medio de la pantalla
        _x_win = (self.winfo_screenwidth() // 2) - (size[0]//2)
        _y_win = (self.winfo_screenheight() // 2) - (size[1]//2)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}+{_x_win}+{_y_win}')
        self.minsize(size[0], size[1])
        self.maxsize(1_000, 650)

        # Recursos #
        self.bg_color = "#1e1e1e"
        self.fg_color = "#F7F7F7"
        self.fg2_color = "#008001"
        self.frame_color = "#292929"

        # Fonts
        self.title_font = Font(
            family="Arial",
            size=12,
            weight="bold"
        )

        self.subtitle_font = Font(
            family="Arial",
            size=10,
        )

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
        
        # El footer de la app con los terminos y condiciones
        self.footer = Footer(self)

        # Creando el menú de la ventana
        self.menu = Menu(self)

        # Configuraciones
        self.config(bg=self.bg_color, menu=self.menu)


        # El header de la app
        self.header = Header(self)

        # El frame de la derecha con las apps
        self.apps = Apps(self)
        

        # Formulario para descargar el contenido
        self.form = Form(self)

        # Estilos de los frames ttk
        _style = ttk.Style()
        _style.configure('TFrame', background=self.frame_color)   

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
        self.pack(side="top", expand=True)
        
        self.create_widgets()

    def create_widgets(self):

        # Etiqueta del formulario
        txt = tk.Label(self, text="Ingresa el link de tu video")
        txt.config(bg=self.parent.frame_color,
                   fg=self.parent.fg_color,
                   font=self.parent.title_font
                   )
        txt.pack(pady=18)

        # Creamos el campo de texto para que el usuario ingrese el link
        url = tk.StringVar()
        entry = tk.Entry(self, textvariable=url)
        _width = int(self.parent.winfo_width() * 0.04)
        entry.config(width=_width, fg=self.parent.fg2_color, font=self.parent.subtitle_font, borderwidth=10, relief=tk.FLAT) #int((self.w_win*0.05))
        entry.pack(side="left", padx=18)

        # Creamos un botón para que el usuario comience su descarga
        def thing():
            pass
        # img_download = tk.PhotoImage(file='img/botones/online/download.png')
        btn_download = tk.Button(self, command=thing)
        btn_download.config(borderwidth=0,
                            bg="#006312",
                            fg=self.parent.fg_color,
                            font=self.parent.title_font,
                            text="Descargar",
                            width=14,
                            height=2,
                            activebackground="#006312",
                            cursor="hand2"
                            )
        # btn_download.image = img_download
        btn_download.pack(side="left", padx=18, pady=18)

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
        self.pack(side="left", fill="y", padx=10, pady=10)

        # Texto informativo sobre este frame
        text = tk.Label(self, text="Descarga contenido de:")
        text.config(bg=parent.frame_color,
                    fg=parent.fg_color,
                    font=parent.subtitle_font
                    )
        text.pack(padx=15, pady=5, expand="yes")

        # Logos de las redes sociales
        fb_app = tk.Label(self,
                               image=parent.resources["logo_fb"], 
                               bg=parent.frame_color
                               )
        fb_app.pack(padx=15, pady=30)

        ig_app = tk.Label(self,
                               image=parent.resources["logo_ig"],
                               bg=parent.frame_color
                               )
        ig_app.pack(padx=15, pady=30)

        yt_app = tk.Label(self,
                               image=parent.resources["logo_yt"],
                               bg=parent.frame_color
                               )
        yt_app.pack(padx=15, pady=30)

class Header(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # self.grid(row=0, column=1)
        self.pack(side='top', fill=tk.X, padx=10, pady=10)
        logo = tk.Label(self,
                 image=parent.resources["header"],
                 bg=parent.frame_color)
        logo.pack()

class Footer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # self.config(width=900)
        self.pack(side="bottom", fill="x", padx=10, pady=10) #, fill="x"

        # Etiquetas de texto del footer
        _myname = tk.Label(self,
                 text="Pablo Avelar Armenta",
                 bg=parent.frame_color,
                 fg=parent.fg_color,
                 font=parent.title_font
                 )
        _myname.pack(pady=5)

        _disclaimer = tk.Label(self,
                 text="Terminos y condiciones",
                 bg=parent.frame_color,
                 fg=parent.fg_color,
                 font=parent.subtitle_font,
                 underline=True,
                 cursor="hand2"
                 )
        _disclaimer.pack(pady=5)

        _disclaimer.bind('<Button-1>', lambda e: webbrowser.open_new("https://pabloavelar.mx/"))


if __name__ == '__main__':
    UI('PabloApp', (900, 600))