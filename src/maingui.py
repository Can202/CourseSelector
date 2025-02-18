
import threading
import os

import func
import parsing
import algorithm

from kivymd.app import MDApp
# Remove red circle
from kivy.config import Config
from kivy.metrics import dp

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.anchorlayout import AnchorLayout


class MainScreen(MDScreen):
    pass
class FirstScreen(MDScreen):
    pass
class ListOfCoursesScreen(MDScreen):
    pass

class LoadScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doing = False
        

    def start_loading(self):
        if not self.doing:
            if not self.ids.startprogressbtn.icon == "eye-outline":
                self.ids.startprogressbtn.text = "Cargando"
                self.ids.startprogressbtn.icon = "close"
                threading.Thread(target=self.start_loading_task).start()
            else:
                self.manager.current = "show"
        else:
            print("The task is already activated")
    
    def start_loading_task(self):
        try:
            self.doing = True
            func.create_folder("cache")
            if not os.path.isfile("data.csv"):
                self.update_status("Error: No has seleccionado cursos!")

            app = MDApp.get_running_app()
            app.main_screen.main_data = parsing.get_main_data()
            app.main_screen.calendars = []
            app.main_screen.points = []
            app.main_screen.nrc_on = False
            
            # Doing the algorithm
            if len(app.main_screen.calendars) == 0:
                app.main_screen.calendars, app.main_screen.points, cache_loaded = algorithm.get_calendars_from_data(app.main_screen.main_data, progress_callback=self.update_progress)
                if cache_loaded:
                    self.update_status("Encontramos los horarios en tu caché.")
                else:
                    self.update_status("Encontrados todos!")
            
            if len(app.main_screen.calendars) == 0:
                self.update_status("No hay horarios sin conflicto.")
                self.doing = False
                
                self.ids.startprogressbtn.text = "Iniciar"
                self.ids.startprogressbtn.icon = "play"
                return
            app.main_screen.nrc_on = app.main_screen.calendars[0]["nrc_active"]
            self.doing = False

            self.ids.startprogressbtn.text = "Mostrar"
            self.ids.startprogressbtn.icon = "eye-outline"

            

            
            

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            self.doing = False
            self.ids.startprogressbtn.text = "Iniciar"
            self.ids.startprogressbtn.icon = "play"
    
    def update_status(self, message):
        self.ids.statuslabel.text = message
    
    def update_progress(self, current, total):
        self.ids.progress_bar.value = int((current / total) * 100)
        self.ids.statuslabel.text = str(int((current / total) * 100)) + " %"
    
    def go_back(self):
        if not self.doing:
            self.manager.current = "first"
            self.update_progress(1,100)
            self.ids.statuslabel.text = "0 %"
            self.ids.startprogressbtn.text = "Iniciar"
            self.ids.startprogressbtn.icon = "play"

class ShowScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def add_table(self):
        card = MDCard(
                style= "outlined",
                size_hint_y= None,
                height = dp(250),
                padding = dp(5),
                elevation = 1)
        anchor = AnchorLayout()
        table = MDDataTable(
            size_hint=(1, 1),  # Adjust the size
            column_data=[
                ("Lunes", dp(15)),
                ("Martes", dp(15)),
                ("Miércoles", dp(15)),
                ("Jueves", dp(15)),
                ("Viernes", dp(15)),
                ("Sábado", dp(15)),
            ],
            row_data=[
                ("A", "B", "C", "D", "E", "S"),
                ("D", "E", "F", "D", "E", "S"),
                ("G", "H", "I", "D", "E", "S"),
                ("A", "B", "C", "D", "E", "S"),
                ("D", "E", "F", "D", "E", "S"),
                ("G", "H", "I", "D", "E", "S"),
                ("A", "B", "C", "D", "E", "S"),
                ("D", "E", "F", "D", "E", "S"),
                ("G", "H", "I", "D", "E", "S"),
            ],
        )
        anchor.add_widget(table)
        card.add_widget(anchor)
        return card
    def test(self):
        print("hello")
        self.ids.cards_box.add_widget(self.add_table())
            

class CourseSelectorApp(MDApp):
    def build(self):
        self.title = "Creador de Horarios"
        self.theme_cls.primary_palette = "Blue"
        self.main_screen = MainScreen()
        return self.main_screen
    


if __name__ == "__main__":
    CourseSelectorApp().run()
