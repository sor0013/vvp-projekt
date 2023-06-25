import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as w
from numba import jit

@jit(nopython=True)
def mandelbrot_set(mal_set, Z, C, k):
    for i in range(k):
        Z = Z**2 + C
        mal_set += 1 * (np.abs(Z) < 2)
    
    return mal_set

@jit(nopython=True)
def julia_set(jul_set, Z, C, k):    
    for i in range(k):
        Z = Z**2 + C
        jul_set += 1 * (np.abs(Z) < 2)
    
    return jul_set

class Fractal:
    """Třída Fractal, jeden parametr 
a to je n, které udává rozměr matice,
která představuje množinu."""
    def __init__(self, n: int):
        self.__S__ = {"x" : 0.0, "y" : 0.0}
        self.__r__ = 2.0
        self.__n__ = n
        self.__k__ = 50
        self.__c_re__ = 0.0
        self.__c_im__ = 0.0
        self.__col__ = "hot"
        self.__fig__, self.__ax__ = plt.subplots()
        self.__im__ = self.__ax__.imshow(self.__mandelbrot_set__(), cmap="hot", extent=(-2.0, 2.0, -2.0, 2.0))
        self.__fun_name__ = self.__mandelbrot_set__
        
    def __mandelbrot_set__(self):
        x_min = self.__S__["x"] - self.__r__
        x_max = self.__S__["x"] + self.__r__
        y_min = self.__S__["y"] - self.__r__
        y_max = self.__S__["y"] + self.__r__
        x = np.linspace(x_min, x_max, self.__n__)
        y = np.linspace(y_min, y_max, self.__n__)
        X, Y = np.meshgrid(x, y)
        C = X + Y*1j
        Z = np.zeros(C.shape, dtype=complex)
        mal_set = np.zeros(Z.shape)
    
        return mandelbrot_set(mal_set, Z, C, self.__k__)
    
    def __julia_set__(self):
        x_min = self.__S__["x"] - self.__r__
        x_max = self.__S__["x"] + self.__r__
        y_min = self.__S__["y"] - self.__r__
        y_max = self.__S__["y"] + self.__r__
        x = np.linspace(x_min, x_max,self.__n__)
        y = np.linspace(y_min, y_max, self.__n__)
        X, Y = np.meshgrid(x, y)
        Z = X + Y*1j
        c = self.__c_re__ + self.__c_im__*1j
        C = np.ones(Z.shape)*c
        jul_set = np.zeros(Z.shape)
        return julia_set(jul_set, Z, C, self.__k__)
    
    """Callback funkce pro radio buttony,
    které nastavují barevné mapování."""
    
    def __set_color__(self, event):
        if event == "hot":
            self.__col__ = "hot"
            self.__im__.set_cmap("hot")
            plt.draw()
        elif event == "magma":
            self.__col__ = "magma"
            self.__im__.set_cmap("magma")
            plt.draw()
        elif event == "jet":
            self.__col__ = "jet"
            self.__im__.set_cmap("jet")
            plt.draw()
        elif event == "rainbow":
            self.__col__ = "rainbow"
            self.__im__.set_cmap("rainbow")
            plt.draw()
            
    """Metody nastavující hodnotu atributu k, c_re a c_im 
    (počet iterací, reálná a imaginnární část c) na hodnotu v textboxech."""
    
    def __set_k__(self, k):
        self.__k__ = int(k)
        
    def __set_c_re__(self, c_re):
        self.__c_re__ = float(c_re)
        
    def __set_c_im__(self, c_im):
        self.__c_re__ = float(c_im)
        
    def __update__(self, event):
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        M = self.__fun_name__()
        self.__im__ = self.__ax__.imshow(M, cmap=self.__col__, extent=(x_min, x_max, y_min, y_max))
        plt.draw()
        
    def __update_re__(self, event):
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        M = self.__fun_name__()
        self.__im__ = self.__ax__.imshow(M, cmap=self.__col__, extent=(x_min, x_max, y_min, y_max))
        plt.draw()
        
    def __update_im__(self, event):
        M = self.__fun_name__()
        self.__im__ = self.__ax__.imshow(M, cmap=self.__col__)
        plt.draw()
        
    def __zoom__(self, event):
        if event.button == 'up':
            # Přibližování fraktálu
            self.__r__ *= 0.5
        elif event.button == 'down':
            # Oddalování fraktálu
            self.__r__ *= 2.0
        M = self.__fun_name__()
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        self.__im__.set_data(M)
        self.__ax__.set_xlim(x_min, x_max)
        self.__ax__.set_ylim(y_min, y_max)
        plt.draw()
    
    def __on_key__(self, event):
        """Zpracovává událost klávesnice a provádí
        funkci move_fractal ve směru dle stisknuté klávesy."""
        if event.key == 'up':
            self.__move_fractal__('up')
        elif event.key == 'down':
            self.__move_fractal__('down')
        elif event.key == 'left':
            self.__move_fractal__('left')
        elif event.key == 'right':
            self.__move_fractal__('right')
    
    def __move_fractal__(self, direction):
        """Pohybuje fraktálem v daném směru."""
        if direction == 'up':
            self.__S__["y"] -= (0.1*self.__r__)
        elif direction == 'down':
            self.__S__["y"] += (0.1*self.__r__)
        elif direction == 'left':
            self.__S__["x"] -= (0.1*self.__r__)
        elif direction == 'right':
            self.__S__["x"] += (0.1*self.__r__)
        # Generování nového fraktálu a aktualizace zobrazení
        M = self.__fun_name__()
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        self.__im__.set_data(M)
        self.__ax__.set_xlim(x_min, x_max)
        self.__ax__.set_ylim(y_min, y_max)
        plt.draw()
        
    def mand_fractal(self):
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        self.__fun_name__ = self.__mandelbrot_set__
        self.__im__ = self.__ax__.imshow(self.__fun_name__(), cmap="hot", extent=(x_min, x_max, y_min, y_max))
        plt.subplots_adjust(bottom=0.2)
        
        text_box_ax = plt.axes([0.2, 0.1, 0.2, 0.05])
        text_box = w.TextBox(text_box_ax, 'iterations: ', initial=str(self.__k__))
        text_box.on_submit(self.__set_k__)
        button_ax = plt.axes([0.4, 0.1, 0.1, 0.05])
        button = w.Button(button_ax, 'submit')
        button.on_clicked(self.__update__)
        
        radio_ax = plt.axes([0.01, 0.8, 0.15, 0.15])
        radio_buttons = w.RadioButtons(radio_ax, ['hot', 'magma', 'jet', 'rainbow'])
        radio_buttons.on_clicked(self.__set_color__)
        
        self.__fig__.canvas.mpl_connect('key_press_event', self.__on_key__)
        self.__fig__.canvas.mpl_connect('scroll_event', self.__zoom__)
        plt.show()
        
    def jul_fractal(self):
        x_min, x_max = self.__S__["x"] - self.__r__, self.__S__["x"] + self.__r__
        y_min, y_max = self.__S__["y"] - self.__r__, self.__S__["y"] + self.__r__
        self.__fun_name__ = self.__julia_set__
        self.im = self.__ax__.imshow(self.__julia_set__(), cmap="hot", extent=(x_min, x_max, y_min, y_max))
        plt.subplots_adjust(bottom=0.2)
        
        text_box_it = plt.axes([0.2, 0.1, 0.07, 0.05])
        text_box = w.TextBox(text_box_it, 'iterations: ', initial=str(self.__k__))
        text_box.on_submit(self.__set_k__)
        
        button_it = plt.axes([0.27, 0.1, 0.1, 0.05])
        sub_it_button = w.Button(button_it, 'submit')
        sub_it_button.on_clicked(self.__update__)
        
        text_box_c_re = plt.axes([0.45, 0.1, 0.07, 0.05])
        text_box_re = w.TextBox(text_box_c_re, 'c_re: ', initial=str(self.__c_re__))
        text_box_re.on_submit(self.__set_c_re__)
        
        button_c_re = plt.axes([0.52, 0.1, 0.1, 0.05])
        button_re = w.Button(button_c_re, 'submit')
        button_re.on_clicked(self.__update_re__)
        
        
        text_box_c_im = plt.axes([0.7, 0.1, 0.07, 0.05])
        text_box_im = w.TextBox(text_box_c_im , 'c_im', initial=str(self.__c_im__))
        text_box_im.on_submit(self.__set_c_re__)
        
        button_c_im = plt.axes([0.77, 0.1, 0.1, 0.05])
        button_im = w.Button(button_c_im, 'submit')
        button_im.on_clicked(self.__update_im__)
        
        radio_ax = plt.axes([0.0, 0.7, 0.2, 0.15])
        radio_buttons = w.RadioButtons(radio_ax, ['hot', 'magma', 'jet', 'rainbow'])
        radio_buttons.on_clicked(self.__set_color__)
        self.__fig__.canvas.mpl_connect('key_press_event', self.__on_key__)
        self.__fig__.canvas.mpl_connect('scroll_event', self.__zoom__)
        plt.show()

if __name__ == "__main__":
    test = Fractal(1000)
    test.jul_fractal()