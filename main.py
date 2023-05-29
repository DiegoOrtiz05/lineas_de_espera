import tkinter as tk
import random
import time

class CarAssemblyLine:

    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Línea de Ensamble de Carros")
        self.canvas_width = 700
        self.canvas_height = 618

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

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # DIbujamos los paneles
        self.canvas.create_rectangle(self.x_1panel, self.y_1panel, self.x_1panel + self.w1p, self.y_1panel + self.h1p, outline='black')

        # Dibujar el segundo panel
        self.canvas.create_rectangle(self.x_2panel, self.y_2panel, self.x_2panel + self.w2p, self.y_2panel + self.h2p, outline='black')

        # Dibujar el tercer panel
        self.canvas.create_rectangle(self.x_3panel, self.y_3panel, self.x_3panel + self.w3p, self.y_3panel + self.h3p, outline='black')

        # DIbujamos la linea de tiempo:
        self.canvas.create_line(152+47, 29+102, 152+47, 29+433+102)

        self.statusStart = [1,2]

        self.paint_status(self.statusStart)

        self.car_width = 50
        self.car_height = 30

        self.car_states = []

        self.statistics = {}

    def paint_status(self, status):
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

            if i in status:
                # Crear un Label
                texto_label = state
                label = tk.Label(root, text=texto_label, wraplength=100, relief="solid", borderwidth=1, highlightbackground="red")
                self.canvas.create_window(posX-100, posY-20, anchor='nw', window=label)
            else:
                # Crear un Label
                texto_label = state
                label = tk.Label(root, text=texto_label, wraplength=100)
                self.canvas.create_window(posX-100, posY-20, anchor='nw', window=label)
            
            i += 1

    def create_car(self):
        car_x = 0
        car_y = self.canvas_height / 2 - self.car_height / 2
        car = self.canvas.create_rectangle(car_x, car_y, car_x + self.car_width, car_y + self.car_height, fill="blue")
        self.car_states.append(car)

    def move_car(self):
        for i, car in enumerate(self.car_states):
            car_statistics = {}

            for state in self.states:
                self.canvas.itemconfig(car, fill="blue", outline="black")
                self.canvas.create_text(self.car_width / 2, self.canvas_height / 2 + 20, text=state, anchor="center")
                self.canvas.update()
                time.sleep(random.uniform(0.5, 1.5))
                self.canvas.itemconfig(car, fill="green", outline="black")
                self.canvas.create_text(self.car_width / 2, self.canvas_height / 2 + 20, text=state, anchor="center")
                self.canvas.update()
                time.sleep(random.uniform(0.5, 1.5))

                entry_time = time.time()
                in_service_time = random.uniform(1, 5)
                time.sleep(in_service_time)
                exit_time = time.time()

                car_statistics[state] = {
                    "entry_time": entry_time,
                    "in_service_time": in_service_time,
                    "exit_time": exit_time
                }

            self.statistics[i] = car_statistics

    def display_statistics(self):
        statistics_window = tk.Toplevel(self.root)
        statistics_window.title("Estadísticas")

        for car_id, car_statistics in self.statistics.items():
            car_label = tk.Label(statistics_window, text=f"Carro {car_id + 1}")
            car_label.pack()

            for state, times in car_statistics.items():
                entry_time = times["entry_time"]
                in_service_time = times["in_service_time"]
                exit_time = times["exit_time"]

                entry_label = tk.Label(statistics_window, text=f"{state}: Tiempo de entrada - {entry_time}")
                entry_label.pack()

                in_service_label = tk.Label(statistics_window, text=f"{state}: Tiempo en servicio - {in_service_time}")
                in_service_label.pack()

                exit_label = tk.Label(statistics_window, text=f"{state}: Tiempo de finalización - {exit_time}")
                exit_label.pack()

            separator = tk.Label(statistics_window, text="----------------------------------------")
            separator.pack()

    def start_simulation(self):
        num_cars = 2
        for _ in range(num_cars):
            self.create_car()
            self.move_car()

        self.display_statistics()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarAssemblyLine(root)

    start_button = tk.Button(root, text="Iniciar simulación", command=app.start_simulation)
    start_button.pack()

    root.mainloop()
