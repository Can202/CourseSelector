from func import *
import algorithm
import parsing

import tkinter as tk
from ttkbootstrap import ttk
import threading
import time


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CourseSelector")
        self.geometry("400x200")
        self.create_start_widgets()
        

    def create_start_widgets(self):
        self.main_frame = MainFrame(master=self)
        self.calendars_frame = CalendarsFrame(master=self)

        self.main_frame.get_calendars_btn.config(command=self.change_to_calendars_frame)
        self.calendars_frame.back_btn.config(command=lambda: self.change_frames(actual=self.calendars_frame, new=self.main_frame))

        self.main_frame.pack()
    
    def change_to_calendars_frame(self):
        self.change_frames(actual=self.main_frame, new=self.calendars_frame)
        self.calendars_frame.start()

    def change_frames(self, *, actual, new):
        actual.pack_forget()
        new.pack()


class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)

        self.calendars_frame = CalendarsFrame(master=self)

        self.title_label = ttk.Label(master=self, text="CourseSelector")
        self.title_label.pack()
        self.get_calendars_btn = ttk.Button(master=self, text="Obtener horarios")
        self.get_calendars_btn.pack()
        
class CalendarsFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)
        self.title_label = ttk.Label(master=self, text="Obtener horarios")
        self.title_label.pack()
        self.situation_label = ttk.Label(master=self, text="Cargando")
        self.situation_label.pack()
        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)
        self.back_btn = ttk.Button(self, text="Volver")

        

    def start(self):
        threading.Thread(target=self.start_task).start()

    def add_back_button(self):
        self.back_btn.pack()
    
    def start_task(self):
        try:
            create_folder("cache")
            if not os.path.isfile("data.csv"):
                self.update_status("Error: Archivo data.csv no encontrado!")
                self.add_back_button()
                return 

            self.main_data = parsing.get_main_data()
            self.calendars = []
            self.points = []
            # Doing the algorithm
            if len(self.calendars) == 0:
                self.calendars, self.points, cache_loaded = algorithm.get_calendars_from_data(self.main_data, progress_callback=self.update_progress)
                if cache_loaded:
                    self.update_status("Encontramos los horarios en tu caché. Los cargamos desde ahí")
                else:
                    self.update_status("Encontrados!")

            if len(self.calendars) == 0:
                self.update_status("No hay horarios sin conflicto.")
                self.add_back_button()
                return
            self.NRC_on = self.calendars[0]["nrc_active"]

            self.see_calendars()

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.add_back_button()

    def update_progress(self, current, total):
        self.progress_bar["value"] = (current / total) * 100
        self.situation_label.config(text=f"Progreso: {current}%")
    def update_status(self, message):
        self.situation_label.config(text=message)
    
    def see_calendars(self):
        pass


    


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()