import flet as ft
from flet import UserControl, Page
from flet import Text
from glob import glob
import os,sys

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

class password_page(UserControl):
    def __init__(self):
        pass

class main_page(UserControl):
    def __init__(self):
        pass

def init_system():
    # path = os.getcwd()
    # os.chdir(path)
    
    assets = {}

    fonts = {}
    imgs = {}
    for i in glob(os.path.join(*["assets","fonts","*.ttf"])):
        if "NanumGothicBold" in i:
            fonts["bold"] = i
        elif "NanumGothicExtraBold" in i:
            fonts["extrabold"] = i
        elif "NanumGothicLight" in i:
            fonts["light"] = i
        elif "NanumGothic" in i:
            fonts["normal"] = i
    
    for i in glob(os.path.join(*["assets","img","*.svg"])):
        if "background" in i:
            imgs["background"] = i

    assets["fonts"] = fonts
    assets["imgs"] = imgs

    return assets

def init_flet(page : Page):
    page.title = "My Little Friend"
    page.bgcolor = ft.colors.LIGHT_BLUE_100
    assets = init_system()
    page.fonts = {
        "nanum_normal" : assets["fonts"]["normal"],
        "nanum_bold" : assets["fonts"]["bold"],
        "nanum_extrabold" : assets["fonts"]["extrabold"],
        "nanum_light" : assets["fonts"]["light"],
    }

    page.vertical_alignment = "center"
    user_name = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15)
    page.add(ft.Column(
        [
        ft.Row([ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "white",size = 150)],alignment="center"),
        ft.Row([ft.Text(value="편하게 이야기 하는", color="white",font_family="nanum_light",size=30,text_align="center")],alignment="center"),
        ft.Row([ft.Text(value="나만의 작은 친구", color="white",font_family="nanum_extrabold",size=50,text_align="center")],alignment="center"),
        ft.Row([user_name],alignment="center"),
        
        ]
    ,spacing=25))
    # page.add(ft.Text("hi"))

ft.app(target=init_flet,assets_dir="assets")
