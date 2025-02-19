
import threading
import os
import math
from functools import partial

import func
import parsing
import algorithm
import cache
import pointsys

from kivymd.app import MDApp
# Remove red circle
from kivy.config import Config
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.clipboard import Clipboard
from kivy.core.text import Label as CoreLabel

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import AnchorLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

from kivy.core.window import Window
Window.size = (1000, Window.height)


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
                self.update_progress(1,100)
                self.ids.statuslabel.text = "0 %"
                self.ids.startprogressbtn.text = "Iniciar"
                self.ids.startprogressbtn.icon = "play"
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
                    self.update_status(f"Encontramos {len(app.main_screen.calendars)} horarios en tu caché.")
                else:
                    self.update_status(f"Encontramos {len(app.main_screen.calendars)} horarios posibles")
            
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

class Separator(Widget):
    def __init__(self, thick=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(3) if thick else dp(1)  # Thicker if True

        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)  # Gray color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class ShowScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_calendars = 10
        self.base = 0
        
        self.app = MDApp.get_running_app()
    
    def on_kv_post(self, base_widget):
        for i in range(self.total_calendars):
            self.ids.cards_box.add_widget(self.create_table_card(i))


    def on_enter(self):
        self.ids.total_calendars_label.text = "Horarios totales: "+ str(len(self.app.main_screen.calendars))
        self.change_tables(0)
        
    def change_to_more_information(self, instance, text):
        i = self.base * self.total_calendars + int(text)
        
        if i < len(self.app.main_screen.calendars):

            the_text = parsing.show_nth_calendar_with_NRC_information_str(self.app.main_screen.calendars, self.app.main_screen.points, i)

            text_input = MDTextField(text = the_text, readonly = True, multiline = True, font_name = "RobotoMono-Regular", font_size=dp(12))


            self.dialog = MDDialog(
                title="Información Extra:",
                type="custom",
                size_hint=(0.9, None),
                content_cls=text_input,
                buttons=[
                    MDFlatButton(text="COPY", on_release=lambda x: self.copy_text(the_text)),
                    MDFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())
                ],
            )
            self.dialog.open()
    def copy_text(self, text):
        Clipboard.copy(text)  # Copies to clipboard
        self.dialog.dismiss()  # Close after copying
    
    def reset_scroll(self, dt):
        self.ids.my_scrollview.effect_y.value = 0  
        self.ids.my_scrollview.effect_y.spring_constant = 0
        self.ids.my_scrollview.effect_y.damping = 1
        self.ids.my_scrollview.scroll_y = 1


    def change_tables(self, base):
        if (base >= 0) and (base < (math.ceil(len(self.app.main_screen.calendars) / self.total_calendars))):
            Clock.schedule_once(self.reset_scroll, 0.05)
            Clock.schedule_once(self.reset_scroll, 0.2)
            self.base = base
            for i in range(self.total_calendars):
                id_cal = self.base * self.total_calendars + i
                if id_cal < len(self.app.main_screen.calendars):
                    self.ids.get(f"table_{i}_label").text = f"Horario {id_cal + 1}, Puntaje: {self.app.main_screen.points[id_cal]}"
                    array = parsing.calendar_show_array(self.app.main_screen.calendars[id_cal])
                    for j in range(10):
                        for k in range(7):
                            self.ids.get(f"table_{i}_grid_{j}_{k}").text = array[j][k]
                else:
                    self.ids.get(f"table_{i}_label").text = ""
                    for j in range(10):
                        for k in range(7):
                            self.ids.get(f"table_{i}_grid_{j}_{k}").text = ""

    
    def go_next(self):
        base = self.base + 1
        self.change_tables(base)
    def go_back(self):
        base = self.base - 1
        self.change_tables(base)
            
    def create_table_card(self, numberid=""):
        card = MDCard(
            style="outlined",
            pos_hint={"center_x": 0.5},
            size_hint_x=None,
            width=dp(900),
            size_hint_y=None,
            height=dp(420),
            padding=dp(5),
            elevation=1
        )

        box = MDBoxLayout(orientation="vertical", spacing=dp(10))

        # Title
        box2 = MDBoxLayout(orientation="horizontal", spacing=dp(10))
        self.ids[f"table_{numberid}_label"] = MDLabel(text="", halign="center", size_hint_y=None, height=dp(35))
        box2.add_widget(self.ids.get(f"table_{numberid}_label"))
        self.ids[f"table_{numberid}_btn"] = MDIconButton(icon="arrow-down-bold-hexagon-outline",
                                                        pos_hint={"center_y": 0.5},
                                                        on_release=lambda instance: self.change_to_more_information(instance, numberid))
        box2.add_widget(self.ids.get(f"table_{numberid}_btn"))
        box.add_widget(box2)

        num_columns = 7
        num_rows = 10
        table_container = MDBoxLayout(orientation="vertical", size_hint_y=None)
        table_container.bind(minimum_height=table_container.setter("height"))

        for i in range(num_rows):
            grid = MDGridLayout(cols=num_columns, spacing=dp(15), size_hint_y=None)
            grid.bind(minimum_height=grid.setter("height"))

            for j in range(num_columns):
                label_id = f"table_{numberid}_grid_{i}_{j}"
                label = MDLabel(text="", size_hint_y=None, height=dp(30), font_size=dp(12), halign="center")

                # Store reference in self.ids
                self.ids[label_id] = label
                grid.add_widget(label)

            table_container.add_widget(grid)

            # Add separator after each row
            thick = False
            if i == 4:
                thick = True
            separator = Separator(thick=thick)
            table_container.add_widget(separator)

        box.add_widget(table_container)
        card.add_widget(box)
        return card

class CacheScreen(MDScreen):
    def on_kv_post(self, base_widget):
        self.cache_btns = []
        caches = cache.get_cache_information_in_str()
        for i in range(len(caches), cache.MAX_CACHE+1):
            caches.append("")
        for i in range(cache.MAX_CACHE):
            opacity = 1
            disabled = False
            if caches[i] == "":
                opacity = 0
                disabled = True
            self.cache_btns.append(MDFlatButton(text=caches[i], pos_hint={"center_x":0.5}, opacity = opacity, disabled = disabled, on_release=lambda instance, i=i: self.load_cache(instance, i+1)))
            self.ids.btn_box.add_widget(self.cache_btns[i])

    def on_enter(self):
        self.update_cache_list()
    def update_cache_list(self):
        caches = cache.get_cache_information_in_str()
        for i in range(len(caches), cache.MAX_CACHE+1):
            caches.append("")
        for i in range(cache.MAX_CACHE):
            a = i
            opacity = 1
            disabled = False
            if caches[i] == "":
                opacity = 0
                disabled = True
            self.cache_btns[i].text = caches[i]
            self.cache_btns[i].opacity = opacity
            self.cache_btns[i].disabled = disabled


    def load_cache(self, instance, cache_id):
        print(cache_id)
        cache.save_csv_cache(number=cache_id)
        self.app = MDApp.get_running_app()
        self.app.main_screen.calendars, self.app.main_screen.points = cache.load_cache(number=cache_id)
        self.manager.current="show"
        pass
    def cache_removal(self, instance):
        print("Caché limpiado")
        cache.clear()
        self.dialog.dismiss()
        self.manager.current = "first"
    def cache_btn(self):
        
        self.dialog = MDDialog(
            title="Quieres limpiar el caché?",
            type="custom",
            size_hint=(0.9, None),
            buttons=[
                MDFlatButton(text="Sí", on_release=self.cache_removal),
                MDFlatButton(text="No", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()
class ConfigScreen(MDScreen):
    def reset_removal(self, instance):
        print("Configuración reiniciada")
        pointsys.reset_config()
        self.dialog.dismiss()
        self.manager.current = "first"
    def reset_btn(self):
        
        self.dialog = MDDialog(
            title="Quieres reiniciar la configuración?",
            type="custom",
            size_hint=(0.9, None),
            buttons=[
                MDFlatButton(text="Sí", on_release=self.reset_removal),
                MDFlatButton(text="No", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

class CourseSelectorApp(MDApp):
    def build(self):
        self.title = "Creador de Horarios"
        self.theme_cls.primary_palette = "Blue"
        self.main_screen = MainScreen()
        return self.main_screen
    

if __name__ == "__main__":
    CourseSelectorApp().run()
