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

class UI(tk.Tk):
    app = None
    def __init__(self):
        super().__init__()
        
        self.w_win = 800
        self.h_win = 600
        _x_win = (self.winfo_screenwidth() // 2) - (self.w_win//2)
        _y_win = (self.winfo_screenheight() // 2) - (self.h_win//2)
        
        self.bg = {
            "fb": "#3b5999",
            "ig": "#e4405f",
            "yt": "#cd201f"
        }
        
        # Recursos #
        self.resources = {
            "header": tk.PhotoImage(file='img/logo/pabloapp_texto.png'),
            "logo_fb": tk.PhotoImage(file='img/redes/fblogo.png'),
            "logo_ig": tk.PhotoImage(file='img/redes/iglogo.png'),
            "logo_yt": tk.PhotoImage(file='img/redes/ytlogo.png'),
            "open": tk.PhotoImage(file='img/botones/abrir.png'),
            "download": tk.PhotoImage(file='img/botones/descargar.png'),
            "change": tk.PhotoImage(file='img/botones/cambiar.png'),
            "socialmedia": tk.PhotoImage(file='img/botones/redes.png')
        }
        
        self.geometry(f'{self.w_win}x{self.h_win}+{_x_win}+{_y_win}')
        # self.resizable(False, False)
        self.iconbitmap('img/logo/icono_app.ico')
        self.title('PabloApp')
        
        UI.selectApp()
        self.config(bg=self.bg[UI.app])
        
        self.showApps()
        
    @classmethod
    def selectApp(cls, next_app="fb") -> None:
        """
        Se encarga de cambiar de app:
            llama a las instancias de fb, ig, yt
            cambia la variable de clase        
        """

        # Para que no abra la misma app en la que está actualmente
        # Así en el autómata no tenemos lazos en la interfaz.
        if cls.app != next_app:
            cls.app = next_app
            if cls.app == "fb":
                print(sm.Facebook())
            elif cls.app == "ig":
                print(sm.Instagram())
            elif cls.app == "yt":
                print(sm.YouTube())

    def changeInterface(self, app:str) -> None:
        """
        
        Parameters
        ----------
        app : str
            Indica la aplicación a la que se cambiará el usuario.
            Puede ser:
                - YouTube -> yt
                - Instagram -> ig
                - Facebook -> fb

        Returns
        -------
        None
            Cambia el color de la interfaz y usa ahora el módulo
            correspondiente a la aplicación a la que se cambió.

        """
        # Cambiando la aplicación
        UI.selectApp(app)
        
        # Cambiando el color del fondo de la interfaz gráfica
        self.config(bg=self.bg[app])
        
        # Cambiando el color de fondo a cada widget de la interfaz grafica
        for widget in self.winfo_children():
            widget.config(bg=self.bg[app])
        
    def showApps(self) -> None:
        """

        Returns
        -------
        None
            Muestra en la interfaz gráfica los botones
            para cambiar de aplicación.

        """
        
        _background = self.bg[UI.app]
        _x = self.w_win * 0.04
        _y = self.h_win / 3
        
        self.header = tk.Label(self,
                 image=self.resources["header"],
                 bg=_background)
        self.header.pack()
        
        
        self.fb_app = tk.Label(self,
                               image=self.resources["logo_fb"], 
                               bg=_background
                               )
        self.fb_app.config(cursor="hand2")
        self.fb_app.place(x=_x, y=_y)

        self.ig_app = tk.Label(self,
                               image=self.resources["logo_ig"],
                               bg=_background
                               )
        self.ig_app.config(cursor="hand2")
        _y += 100
        self.ig_app.place(x=_x, y = _y)

        self.yt_app = tk.Label(self,
                               image=self.resources["logo_yt"],
                               bg=_background
                               )
        self.yt_app.config(cursor="hand2")
        _y += 100
        self.yt_app.place(x=_x, y = _y)
        
        self.fb_app.bind('<Button-1>', lambda _:self.changeInterface('fb'))
        self.ig_app.bind('<Button-1>', lambda _:self.changeInterface('ig'))
        self.yt_app.bind('<Button-1>', lambda _:self.changeInterface('yt'))
        
            
if __name__ == '__main__':
    root = UI()
    root.mainloop()
        
        