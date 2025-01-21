from func import *
import algorithm
import parsing
import cache

import tkinter as tk
from ttkbootstrap import ttk
import threading
import time
import shutil



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CourseSelector")
        self.geometry("1000x800")
        self.create_start_widgets()
        

    def create_start_widgets(self):
        self.main_frame = MainFrame(master=self)
        self.calendars_frame = getCalendarsFrame(master=self)
        self.reset_default_frame = resetDefault(master=self)
        self.clear_cache_frame = clearCacheFrame(master=self)

        self.main_frame.get_calendars_btn.config(command=self.change_to_calendars_frame)
        self.main_frame.reset_default_btn.config(command=lambda: self.change_frames(actual=self.main_frame, new=self.reset_default_frame))
        self.main_frame.clear_cache_btn.config(command=lambda: self.change_frames(actual=self.main_frame, new=self.clear_cache_frame))

        self.calendars_frame.back_btn.config(command=self.change_back_from_calendars_frame)
        self.calendars_frame.see_calendars_btn.config(command=self.open_showCalendars)
        self.calendars_frame.obtain_calendar_information_btn.config(command=self.obtain_calendar_information_btn_pressed)

        self.reset_default_frame.yesbtn.config(command=lambda:self.reset_and_back(True))
        self.reset_default_frame.nobtn.config(command=lambda:self.reset_and_back(False))

        self.clear_cache_frame.yesbtn.config(command=lambda:self.clear_and_back(True))
        self.clear_cache_frame.nobtn.config(command=lambda:self.clear_and_back(False))

        self.main_frame.pack()
    
    def change_to_calendars_frame(self):
        self.change_frames(actual=self.main_frame, new=self.calendars_frame)
        self.calendars_frame.progress_bar.pack(fill=tk.X, padx=10, pady=10)
        self.calendars_frame.start()

    def change_back_from_calendars_frame(self):
        self.calendars_frame.see_calendars_btn.pack_forget()
        self.calendars_frame.obtain_calendar_information_entry.pack_forget()
        self.calendars_frame.obtain_calendar_information_btn.pack_forget()
        self.change_frames(actual=self.calendars_frame, new=self.main_frame)

    def open_showCalendars(self):
        self.show_calendars_frame = showCalendars(master=self, calendars=self.calendars_frame.calendars, points=self.calendars_frame.points)
        self.show_calendars_frame.back_btn.config(command=lambda: self.change_frames(actual=self.show_calendars_frame, new=self.calendars_frame))
        self.change_frames(actual=self.calendars_frame, new=self.show_calendars_frame)

    def obtain_calendar_information_btn_pressed(self):
        number = self.calendars_frame.obtain_calendar_information_entry_var.get() - 1
        if (number != -1) and (number < len(self.calendars_frame.calendars)):
            self.more_calendar_information = moreCalendarInformation(master=self, calendars=[self.calendars_frame.calendars[number]], points=[self.calendars_frame.points[number]], number=number)
            self.more_calendar_information.back_btn.config(command=lambda: self.change_frames(actual=self.more_calendar_information, new=self.calendars_frame))
            self.change_frames(actual=self.calendars_frame, new=self.more_calendar_information)

    def clear_and_back(self, clear):
        if clear:
            cache.clear()
        self.change_frames(actual=self.clear_cache_frame,new=self.main_frame)
    def reset_and_back(self, reset):
        if reset:
            shutil.copyfile("default/config","config.json")
        self.change_frames(actual=self.reset_default_frame,new=self.main_frame)

    def change_frames(self, *, actual, new):
        actual.pack_forget()
        new.pack()


class MainFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)

        self.title_label = ttk.Label(master=self, text="CourseSelector")
        self.title_label.pack(pady=5)
        self.get_calendars_btn = ttk.Button(master=self, text="Obtener horarios")
        self.get_calendars_btn.pack(pady=5)
        self.select_courses_btn = ttk.Button(master=self, text="Seleccionar cursos")
        self.select_courses_btn.pack(pady=5)
        self.configure_btn = ttk.Button(master=self, text="Configurar")
        self.configure_btn.pack(pady=5)
        self.reset_default_btn = ttk.Button(master=self, text="Reiniciar configuración")
        self.reset_default_btn.pack(pady=5)
        self.load_cache_btn = ttk.Button(master=self, text="Cargar horarios desde tu caché")
        self.load_cache_btn.pack(pady=5)
        self.clear_cache_btn = ttk.Button(master=self, text="Limpiar caché")
        self.clear_cache_btn.pack(pady=5)
        
class getCalendarsFrame(tk.Frame):
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

        
        self.see_calendars_btn = ttk.Button(master=self,text="Ver horarios cargados")
        self.obtain_calendar_information_entry_var = tk.IntVar()
        self.obtain_calendar_information_entry_var.set(1)
        self.obtain_calendar_information_entry = ttk.Entry(master=self,textvariable=self.obtain_calendar_information_entry_var)
        self.obtain_calendar_information_btn = ttk.Button(master=self,text="Obtener información extra")

    def start(self):
        threading.Thread(target=self.start_task).start()

    def add_back_button(self):
        self.back_btn.pack()
    
    
    
    def start_task(self):
        try:
            create_folder("cache")
            if not os.path.isfile("data.csv"):
                self.update_status("Error: No has seleccionado cursos!")
                self.progress_bar.pack_forget()
                self.add_back_button()
                return 

            self.main_data = parsing.get_main_data()
            self.calendars = []
            self.points = []
            # Doing the algorithm
            if len(self.calendars) == 0:
                self.calendars, self.points, cache_loaded = algorithm.get_calendars_from_data(self.main_data, progress_callback=self.update_progress)
                if cache_loaded:
                    self.update_status("Encontramos los horarios en tu caché.")
                else:
                    self.update_status("Encontrados todos!")

            if len(self.calendars) == 0:
                self.update_status("No hay horarios sin conflicto.")
                self.progress_bar.pack_forget()
                self.add_back_button()
                return
            self.NRC_on = self.calendars[0]["nrc_active"]


            self.see_calendars()

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.progress_bar.pack_forget()
            self.add_back_button()

    def update_progress(self, current, total):
        self.progress_bar["value"] = (current / total) * 100
        self.situation_label.config(text=f"Progreso: {current}%")
    def update_status(self, message):
        self.situation_label.config(text=message)
    
    def see_calendars(self):
        self.progress_bar.pack_forget()
        self.add_back_button()

        self.see_calendars_btn.pack(pady=5)
        self.obtain_calendar_information_entry.pack(side=tk.LEFT, padx=5)
        self.obtain_calendar_information_btn.pack()

class showCalendars(tk.Frame):
    def __init__(self, master, calendars, points, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.back_btn = ttk.Button(self, text="Volver")
        self.back_btn.pack(pady=5)

        self.calendars = calendars
        self.points = points

        data = parsing.get_schedule_array_for_all(self.calendars, self.points)


        self.table = Table(self, data=data)
        self.table.pack(fill=tk.BOTH, expand=True)

class moreCalendarInformation(tk.Frame):
    def __init__(self, master, calendars, points, number, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.back_btn = ttk.Button(self, text="Volver")
        self.back_btn.pack(pady=5)

        text_output = f"---Calendar {number+1}---\n"
        text_output += parsing.calendar_show(calendars[0], PRINT=False, len_between_columns=17)
        text_output += f"score: {points[0]}\n"

        text_output += "NRCs:\n"
        
        max_len = 0
        for i in range(len(calendars[0]["courses_id"])):
            if max_len < len(calendars[0]['sections_nrc_bundle'][i]):
                max_len = len(calendars[0]['sections_nrc_bundle'][i])
        for i in range(len(calendars[0]["courses_id"])):
            if calendars[0]['sections_nrc_alternative_bundle'][i] != "":
                text_output += f"{calendars[0]['courses_id'][i]}: {(calendars[0]['sections_nrc_bundle'][i]).ljust(max_len+2)} ({calendars[0]['sections_nrc_alternative_bundle'][i]})\n"
            else:
                text_output += f"{calendars[0]['courses_id'][i]}: {(calendars[0]['sections_nrc_bundle'][i]).ljust(max_len+2)}\n"

        print(text_output)
        self.text = tk.Text(self, height=40, width=140, wrap="word", font=("Courier New", 10))
        self.text.insert(tk.END, text_output)
        self.text.config(state="disabled")
        self.text.pack(padx=10, pady=10)

class Table(tk.Frame):
    def __init__(self, master, data, height=40, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)

        # Extract rows from the data (headers are no longer used)
        self.rows = data if len(data) > 1 else []

        # Create the Treeview widget without headers
        self.table = ttk.Treeview(self, columns=("0", "1", "2", "3", "4", "5", "6"), show="headings", height=height)

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)

        self.table.column("0", width=25, anchor=tk.CENTER)
        self.table.column("1", width=100, anchor=tk.CENTER)
        self.table.column("2", width=100, anchor=tk.CENTER)
        self.table.column("3", width=100, anchor=tk.CENTER)
        self.table.column("4", width=100, anchor=tk.CENTER)
        self.table.column("5", width=100, anchor=tk.CENTER)
        self.table.column("6", width=100, anchor=tk.CENTER)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Insert rows into the table (columns need to be set even if headers are not displayed)
        for row in self.rows:
            self.table.insert("", tk.END, values=row)

class clearCacheFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)
        self.label = ttk.Label(self,text="Quieres limpiar el caché?")
        self.yesbtn = ttk.Button(self,text="Sí")
        self.nobtn = ttk.Button(self,text="No")
        self.label.pack(pady=5)
        self.yesbtn.pack(side=tk.LEFT, padx=5)
        self.nobtn.pack()

class resetDefault(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(padx=10, pady=10)
        self.label = ttk.Label(self,text="Quieres reiniciar la configuración a la predeterminada?")
        self.yesbtn = ttk.Button(self,text="Sí")
        self.nobtn = ttk.Button(self,text="No")
        self.label.pack(pady=5)
        self.yesbtn.pack(side=tk.LEFT, padx=5)
        self.nobtn.pack()



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()