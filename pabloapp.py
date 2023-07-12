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
    def __init__(self):
        super().__init__()
        
        self.w_win = 800
        self.h_win = 600
        _x_win = (self.winfo_screenwidth() // 2) - (self.w_win//2)
        _y_win = (self.winfo_screenheight() // 2) - (self.h_win//2)
        
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
        
        self.geometry(f'{self.w_win}x{self.h_win}+{_x_win}+{_y_win}')
        # self.resizable(False, False)
        self.iconbitmap('img/logo/icono_app.ico')
        self.title('PabloApp')
        
        self.config(bg=UI.bg_color)
        
        # Creando el menú de la ventana
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)

        # Le ponemos una sección y lo asignamos al menú de la ventana
        tools = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Archivo", menu=tools) # En formato de cascada!

        # Creamos elementos para ese menú
        tools.add_command(label="Abrir ruta de descargas", command=lambda:self.open_in_explorer())
        tools.add_command(label="Cambiar ruta de descargas", command=lambda:print("Cambiar ruta"))
        tools.add_command(label="Acerca de", command=lambda:print("Acerca de"))

        self.showApps()
        self.showForm()

    
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
        form.config(bg=UI.bg_color, width=self.w_win, height=_y*4.2) #bg=UI.bg_color
        form.pack(padx=_x, pady=_y)

        # Creamos el campo de texto para que el usuario ingrese el link
        url = tk.StringVar()
        entry = tk.Entry(form, textvariable=url)
        entry.config(width=int(self.w_win*0.8), font=("Georgia", 15))
        entry.pack(pady=_y*2)

        # Creamos un botón para que el usuario comience su descarga
        

    def showApps(self) -> None:
        """
            Muestra en la interfaz gráfica los botones
            para cambiar de aplicación.
        Returns
        -------
        None
        """
        
        _x = self.w_win * 0.04
        _y = self.h_win / 3
        
        self.header = tk.Label(self,
                 image=self.resources["header"],
                 bg=UI.bg_color)
        self.header.pack()
        
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
        
            
if __name__ == '__main__':
    root = UI()
    root.mainloop()
        
        