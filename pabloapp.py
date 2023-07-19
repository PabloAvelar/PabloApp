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
import SocialMedia as sm
import os

class UI(tk.Tk):
    bg_color = "#1e1e1e"
    frame_color = "#292929"
    def __init__(self, title, size):
        super().__init__()

        _x_win = (self.winfo_screenwidth() // 2) - (size[0]//2)
        _y_win = (self.winfo_screenheight() // 2) - (size[1]//2)

        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}+{_x_win}+{_y_win}')
        
        # Recursos #
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
        
        
        self.config(bg=UI.bg_color)
        
        # Creando el menú de la ventana
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)

        # Le ponemos una sección y lo asignamos al menú de la ventana
        tools = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Configuración", menu=tools) # En formato de cascada!

        # Creamos elementos para ese menú
        tools.add_command(label="Abrir ruta de descargas", command=lambda:self.open_in_explorer())
        tools.add_command(label="Cambiar ruta de descargas", command=lambda:print("Cambiar ruta"))
        tools.add_command(label="Acerca de", command=lambda:print("Acerca de"))

        self.showHeader()
        self.showApps()
        self.showForm()
        self.showFooter()

    
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


    def showForm(self) -> None:
        """
            Muestra en la interfaz gráfica un campo de texto y un botón
            para que el usuario ingrese el link de su video y pueda
            iniciar su descarga.

            Aquí se detectará si el link es de:
                -Facebook
                -Instagram
                -YouTube

        """

        # Le damos forma al frame del formulario
        _x = self.w_win // 4 
        _y = self.h_win // 10

        form = tk.Frame(self)
        form.config(bg=UI.frame_color) #bg=UI.bg_color, , width=150, height=_y*4.2
        # form.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.15, anchor="c")
        # form.pack(pady=self.h_win//4)
        form.grid(row=1, column=1)

        # Creamos el campo de texto para que el usuario ingrese el link
        url = tk.StringVar()
        entry = tk.Entry(form, textvariable=url)
        entry.config(width=50, font=("Open Sans", 12), borderwidth=10, relief=tk.FLAT) #int((self.w_win*0.05))
        # entry.place(relx=0.5, rely=0.5, anchor="c")
        entry.grid(row=1, column=1, columnspan=3, padx=15, pady=20)
        # entry.pack(pady=_y*2)

        # Creamos un botón para que el usuario comience su descarga
        def thing():
            pass
        img_download = tk.PhotoImage(file='img/botones/online/download.png')
        btn_download = tk.Button(form, image=img_download, command=thing)
        btn_download.config(borderwidth=0, bg=UI.frame_color, activebackground=UI.frame_color, cursor="hand2")
        # btn_download.place(relx=0.5, rely=0.5, anchor="c")
        btn_download.image = img_download
        btn_download.grid(row=2, column=2, pady=10)
        # btn_download.pack()

    def showApps(self) -> None:
        """
            Muestra en la interfaz gráfica los botones
            para cambiar de aplicación.
        Returns
        -------
        None
        """
        
        apps = tk.Frame(self)
        apps.config(bg=UI.frame_color)
        apps.grid(row=1, column=0)

        _x = self.w_win * 0.04
        _y = self.h_win / 3
        
        self.fb_app = tk.Label(self,
                               image=self.resources["logo_fb"], 
                               bg=UI.bg_color
                               )
        self.fb_app.place(x=_x, y=_y)

        self.ig_app = tk.Label(self,
                               image=self.resources["logo_ig"],
                               bg=UI.bg_color
                               )
        _y += 100
        self.ig_app.place(x=_x, y = _y)

        self.yt_app = tk.Label(self,
                               image=self.resources["logo_yt"],
                               bg=UI.bg_color
                               )
        _y += 100
        self.yt_app.place(x=_x, y = _y)
        

    def showHeader(self):
        header = tk.Frame(self)
        header.grid(row=0, column=1)

        logo = tk.Label(header,
                 image=self.resources["header"],
                 bg=UI.bg_color)
        logo.pack()

    def showFooter(self):
        footer = tk.Frame(self)
        footer.config(bg=UI.frame_color)
        footer.grid(row=2, column=1, columnspan=3)

        tk.Label(footer, text="hola").pack()

if __name__ == '__main__':
    root = UI('PabloApp', (600, 1_000))
    root.mainloop()
        
        