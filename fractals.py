import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as w

class Fractal:
    """Třída Fractal, jeden parametr 
a to je n, které udává rozměr matice,
která představuje množinu."""
    def __init__(self, n):
        self.x_min = -2
        self.x_max = 2
        self.y_min = -2
        self.y_max = 2
        self.n = n
        self.k = 50
        self.c_re = 0.0
        self.c_im = 0.0
        self.col = "hot"
        self.fig, self.ax = plt.subplots()
        self.im = self.ax.imshow(self.mandelbrot_set(), cmap="hot", extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        self.fun_name = self.mandelbrot_set
        
    def mandelbrot_set(self):
        k = self.k
        x, y = np.linspace(self.x_min, self.x_max, self.n), np.linspace(self.y_min, self.y_max, self.n)
        X, Y = np.meshgrid(x, y)
        C = X + Y*1j
        Z = np.zeros(C.shape, dtype=complex)
        mal_set = np.zeros(Z.shape)
        for i in range(k):
            Z = Z**2 + C
            mal_set += 1 * (np.abs(Z)<2)
        
        return mal_set

    def julia_set(self):
        k = self.k
        x, y = np.linspace(self.x_min, self.x_max, self.n), np.linspace(self.y_min, self.y_max, self.n)
        X, Y = np.meshgrid(x, y)
        Z = X + Y*1j
        c = self.c_re + self.c_im*1j
        C = np.ones(Z.shape)*c
        jul_set = np.zeros(Z.shape)
        for i in range(k):
            Z = Z**2 + C
            jul_set += 1 * (np.abs(Z) < 2)
        
        return jul_set
    
    """Callback funkce pro radio buttony,
    které nastavují barevné mapování."""
    
    def set_color(self, event):
        if event == "hot":
            self.col = "hot"
            self.im.set_cmap("hot")
            plt.draw()
        elif event == "magma":
            self.col = "magma"
            self.im.set_cmap("magma")
            plt.draw()
        elif event == "jet":
            self.col = "jet"
            self.im.set_cmap("jet")
            plt.draw()
        elif event == "rainbow":
            self.col = "rainbow"
            self.im.set_cmap("rainbow")
            plt.draw()
            
    """Metody nastavující hodnotu atributu k, c_re a c_im 
    (počet iterací, reálná a imaginnární část c) na hodnotu v textboxech."""
    
    def set_k(self, k):
        self.k = int(k)
        
    def set_c_re(self, c_re):
        self.c_re = float(c_re)
        
    def set_c_im(self, c_im):
        self.c_im = float(c_im)
        
    def update(self, event):
        M = self.fun_name()
        self.im = self.ax.imshow(M, cmap=self.col, extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        plt.draw()
        
    def update_re(self, event):
        M = self.fun_name()
        self.im = self.ax.imshow(M, cmap=self.col, extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        plt.draw()
        
    def update_im(self, event):
        M = self.fun_name()
        self.im = self.ax.imshow(M, cmap=self.col, extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        plt.draw()
        
    def zoom(self, event):
        """Přibližuje nebo oddaluje fraktál na základě scrollování."""
        x_center = (self.x_min + self.x_max) / 2
        y_center = (self.y_min + self.y_max) / 2
        x_dist = (self.x_max - self.x_min) / 2
        y_dist = (self.y_max - self.y_min) / 2
        if event.button == 'up':
            # Přibližování fraktálu
            self.x_min = x_center - x_dist / 2
            self.x_max = x_center + x_dist / 2
            self.y_min = y_center - y_dist / 2
            self.y_max = y_center + y_dist / 2
        elif event.button == 'down':
            # Oddalování fraktálu
            self.x_min = x_center - 2 * x_dist
            self.x_max = x_center + 2 * x_dist
            self.y_min = y_center - 2 * y_dist
            self.y_max = y_center + 2 * y_dist
        M = self.fun_name()
        self.im.set_data(M)
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        plt.draw()
    
    def on_key(self, event):
        """Zpracovává událost klávesnice a provádí
        funkci move_fractal ve směru dle stisknuté klávesy."""
        if event.key == 'up':
            self.move_fractal('up')
        elif event.key == 'down':
            self.move_fractal('down')
        elif event.key == 'left':
            self.move_fractal('left')
        elif event.key == 'right':
            self.move_fractal('right')
    
    def move_fractal(self, direction):
        """Pohybuje fraktálem v daném směru."""
        if direction == 'up':
            self.y_min -= 0.1
            self.y_max -= 0.1
        elif direction == 'down':
            self.y_min += 0.1
            self.y_max += 0.1
        elif direction == 'left':
            self.x_min -= 0.1
            self.x_max -= 0.1
        elif direction == 'right':
            self.x_min += 0.1
            self.x_max += 0.1
        # Generování nového fraktálu a aktualizace zobrazení
        M = self.fun_name()
        self.im.set_data(M)
        self.ax.set_xlim(self.x_min, self.x_max)
        self.ax.set_ylim(self.y_min, self.y_max)
        plt.draw()
        
    def mand_fractal(self):
        self.fun_name = self.mandelbrot_set
        self.im = self.ax.imshow(self.fun_name(), cmap="hot", extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        plt.subplots_adjust(bottom=0.2)
        
        text_box_ax = plt.axes([0.2, 0.1, 0.2, 0.05])
        text_box = w.TextBox(text_box_ax, 'iterations: ', initial=str(self.k))
        text_box.on_submit(self.set_k)
        button_ax = plt.axes([0.4, 0.1, 0.1, 0.05])
        button = w.Button(button_ax, 'submit')
        button.on_clicked(self.update)
        
        radio_ax = plt.axes([0.01, 0.8, 0.2, 0.15])
        radio_buttons = w.RadioButtons(radio_ax, ['hot', 'magma', 'jet', 'rainbow'])
        radio_buttons.on_clicked(self.set_color)
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)
        plt.show()
        
    def jul_fractal(self):
        self.fun_name = self.julia_set
        self.im = self.ax.imshow(self.julia_set(), cmap="hot", extent=(self.x_min, self.x_max, self.y_min, self.y_max))
        plt.subplots_adjust(bottom=0.2)
        
        text_box_it = plt.axes([0.2, 0.1, 0.07, 0.05])
        text_box = w.TextBox(text_box_it, 'iterations: ', initial=str(self.k))
        text_box.on_submit(self.set_k)
        
        button_it = plt.axes([0.27, 0.1, 0.1, 0.05])
        sub_it_button = w.Button(button_it, 'submit')
        sub_it_button.on_clicked(self.update)
        
        text_box_c_re = plt.axes([0.45, 0.1, 0.07, 0.05])
        text_box_re = w.TextBox(text_box_c_re, 'c_re: ', initial=str(self.c_re))
        text_box_re.on_submit(self.set_c_re)
        
        button_c_re = plt.axes([0.52, 0.1, 0.1, 0.05])
        button_re = w.Button(button_c_re, 'submit')
        button_re.on_clicked(self.update_re)
        
        
        text_box_c_im = plt.axes([0.7, 0.1, 0.07, 0.05])
        text_box_im = w.TextBox(text_box_c_im , 'c_im', initial=str(self.c_im))
        text_box_im.on_submit(self.set_c_im)
        
        button_c_im = plt.axes([0.77, 0.1, 0.1, 0.05])
        button_im = w.Button(button_c_im, 'submit')
        button_im.on_clicked(self.update_im)
        
        radio_ax = plt.axes([0.0, 0.7, 0.2, 0.15])
        radio_buttons = w.RadioButtons(radio_ax, ['hot', 'magma', 'jet', 'rainbow'])
        radio_buttons.on_clicked(self.set_color)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event', self.zoom)
        plt.show()

if __name__ == "__main__":
    test = Fractal(1000)
    test.mand_fractal()