import flet as ft
from flet import KeyboardEvent, Page
from flet import Text
from glob import glob
import os,sys

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

def init_system():
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

def main(page : Page):
    assets = init_system()
    def style_init():
        page.title = "My Little Friend"
        page.window_height=800
        page.window_width=480
        page.window_min_height = 800
        page.window_min_width=480
        page.fonts = {
            "nanum_normal" : assets["fonts"]["normal"],
            "nanum_bold" : assets["fonts"]["bold"],
            "nanum_extrabold" : assets["fonts"]["extrabold"],
            "nanum_light" : assets["fonts"]["light"],
        }
    style_init()

    # page.window_center()
    user_name = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15,width=250)
    password = ft.TextField(label="비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250)

    main_page = ft.View(
                "/",
                [
                    ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "black",size = 80),
                    ft.Text(value="편하게 이야기 하는", color="gray100",font_family="nanum_light",size=20,text_align="center"),
                    ft.Text(value="나만의 작은 친구", color="brown200",font_family="nanum_extrabold",size=35,text_align="center"),
                    user_name,
                    ft.ElevatedButton("확인", on_click=lambda _: page.go("/password")),
                ],spacing=25,vertical_alignment="center",horizontal_alignment="center"
            )
    password_page =ft.View(
                    "/password",
                    [
                        ft.Icon(name = ft.icons.PASSWORD,color = "black",size = 150),
                        password,

                    ],spacing=25,vertical_alignment="center",horizontal_alignment="center"
                )
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            main_page
            
        )
        if page.route == "/password":
            page.views.append(
                password_page
            )
        page.update()

    def on_keyboard(e: KeyboardEvent):
        if e.key =="Enter" and page.route == "/" and user_name.value != "":
            page.go("/password")

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_keyboard_event = on_keyboard
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main,assets_dir="assets")

