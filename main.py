import flet as ft
from flet import UserControl, Page
from flet import Text
from glob import glob
import os

class start_page(UserControl):
    def __init__(self):
        pass

class main_page(UserControl):
    def __init__(self):
        pass

def init_system():
    path = os.getcwd()
    os.chdir(path)
    temp = glob(os.path.join(*["src","fonts","*.ttf"]))
    fonts = {}
    for i in temp:
        if "NanumGothicBold" in i:
            fonts["bold"] = i
        elif "NanumGothicExtraBold" in i:
            fonts["extrabold"] = i
        elif "NanumGothicLight" in i:
            fonts["light"] = i
        elif "NanumGothic" in i:
            fonts["normal"] = i
    return fonts

def init_flet(page : Page):
    fonts = init_system()
    page.fonts = {
        "nanum_normal" : fonts["normal"],
        "nanum_bold" : fonts["bold"],
        "nanum_extrabold" : fonts["extrabold"],
        "nanum_light" : fonts["light"],
    }
    t = Text(value="안녕하세요!", color="green",font_family="bold")
    
    page.title = "my first flet"
    # t = Text(value="Hello, world!", color="green",font_family = )
    # page.add(t)
    page.controls.append(t)
    page.update()


ft.app(target=init_flet)


print(init_system())