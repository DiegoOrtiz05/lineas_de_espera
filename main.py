import tkinter as tk
import random
import time
from PIL import Image, ImageTk
import threading

class CarAssemblyLine:

    def __init__(self, root):
        
        self.root = root
        self.root.title("Simulación de Línea de Ensamble de Carros")
        self.canvas_width = 700
        self.canvas_height = 618
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()


        # Estados de la linea de espera
        self.states = [
            "Recepción de componentes",
            "Ensamble del chasis",
            "Instalación del motor",
            "Instalación de sistemas eléctricos",
            "Instalación de sistemas de suspensión",
            "Instalación de sistemas de frenado",
            "Ensamble de carrocería",
            "Instalación de sistemas de climatización",
            "Instalación de sistemas de audio",
            "Pintura y acabado",
            "Inspección de calidad",
            "Embalaje y envío"
        ]

        # Tamaños y ubicaciones de los 3 pneles
        self.x_1panel = 47
        self.y_1panel = 102
        self.x_2panel = 399
        self.y_2panel = 102
        self.x_3panel = 399
        self.y_3panel = 370
        self.w1p= 310
        self.h1p= 491
        self.w2p= 253
        self.h2p= 223
        self.w3p= 253
        self.h3p= 223

        # DIbujamos los paneles
        self.canvas.create_rectangle(self.x_1panel, self.y_1panel, self.x_1panel + self.w1p, self.y_1panel + self.h1p, outline='black')

        # Dibujar el segundo panel
        self.canvas.create_rectangle(self.x_2panel, self.y_2panel, self.x_2panel + self.w2p, self.y_2panel + self.h2p, outline='black')

        # Dibujar el tercer panel
        self.canvas.create_rectangle(self.x_3panel, self.y_3panel, self.x_3panel + self.w3p, self.y_3panel + self.h3p, outline='black')

        # DIbujamos la linea de tiempo:
        self.canvas.create_line(152+47, 29+102, 152+47, 29+433+102)

        # Dibujamos los estados
        posX = 0
        posY = 0
        i = 0
        for state in self.states:
            if i % 2 == 0:
                self.canvas.create_line(120+47, 102+68+(i*33), 152+47, 102+68+(i*33))
                posX = 120+47
                posY = 102+68+(i*33)
            else: 
                self.canvas.create_line(152+47, 102+68+(i*33), 152+94, 102+68+(i*33))
                posX = 152+47+147
                posY = 102+68+(i*33)
            
            # Crear un Label
            texto_label = state
            label = tk.Label(root, text=texto_label, wraplength=100)
            self.canvas.create_window(posX-100, posY-20, anchor='nw', window=label)
            
            i += 1
        # Se terminan de dibujar los estados

        self.car_width = 50
        self.car_height = 30

        self.car_states = []

        self.statistics = {}

    def paint_status(self, status, isOn):
        posX = 0
        posY = 0
        if status % 2 == 0:
            posX = 120+47
            posY = 102+68+(status*33)
        else:
            posX = 152+47+147
            posY = 102+68+(status*33)
        # Crear un Label
        texto_label = self.states[status]
        if isOn:
            label = tk.Label(root, text=texto_label, wraplength=100, relief="solid", borderwidth=1, highlightbackground="red")
        else: 
            label = tk.Label(root, text=texto_label, wraplength=100)
        self.canvas.create_window(posX-100, posY-20, anchor='nw', window=label) 

    def init_status(self, status):
        self.paint_status(status, True)
        # El hilo se duerme por un tiempo
        print("Esperando")
        time.sleep(random.randint(1, 5)) 
        print("Terminó de esperar")
        self.paint_status(status, False)
        self.statusBoolean[status] = True 
        self.statusBoolean[status+1] = True 
        self.init_status(status+1)

    def init_simulation(self):
        self.statusBoolean = [True, True, True, True, True, True, True, True, True, True, True, True]
        for i in range (100):
            while self.statusBoolean[0] == False:
                print("Esperando a que se desocupe el primer estado")
                
            self.statusBoolean[i] = False
            # Crear un objeto de tipo Thread
            mi_hilo = threading.Thread(target=self.init_status(0))
            # Iniciar la ejecución del hilo
            mi_hilo.start()
            i+=1
    

if __name__ == "__main__":
    root = tk.Tk()
    app = CarAssemblyLine(root)

    start_button = tk.Button(root, text="Iniciar simulación", command=app.init_simulation)
    start_button.pack()

    root.mainloop()
