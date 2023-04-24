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
    hf = ft.HapticFeedback()
    page.overlay.append(hf)
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

    user_name_tf = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15,width=250)
    password_tf = ft.TextField(label="비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER")
    message_tf = ft.TextField(multiline=True,shift_enter = True,width=350,height=35)

    record_btn = ft.IconButton(icon=ft.icons.KEYBOARD_VOICE,icon_size=35)
    send_btn = ft.IconButton(icon=ft.icons.SEND,icon_size=35)

    def password_check(e):
        correct = "1234"
        
        if password_tf.value == correct:
            page.go("/message")

        else:
            hf.vibrate()
            password_tf.error_text = "비밀번호가 틀렸습니다"

        page.update()
        
    def route_change(route):
        page.views.clear()
        page.views.append(
            main_page
            )
        if page.route == "/password":
            page.views.append(
                password_page
            )
        if page.route == "/message":
            page.views.append(
                message_page
            )
        page.update()

    def on_keyboard(e: KeyboardEvent):
        if e.key =="Enter" and page.route == "/" and user_name_tf.value != "":
            page.go("/password")

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
    main_page = ft.View(
                "/",
                [
                    ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "black",size = 80),
                    ft.Text(value="편하게 이야기 하는", color="gray100",font_family="nanum_light",size=20,text_align="center"),
                    ft.Text(value="나만의 작은 친구", color="brown200",font_family="nanum_extrabold",size=35,text_align="center"),
                    user_name_tf,
                    ft.ElevatedButton("확인", on_click=lambda _: page.go("/password")),
                ],spacing=25,vertical_alignment="center",horizontal_alignment="center"
            )
    password_page =ft.View(
                    "/password",
                    [
                        ft.Icon(name = ft.icons.PASSWORD,color = "black",size = 150),
                        password_tf,
                        ft.ElevatedButton("확인", on_click=password_check),
                    ],spacing=25,vertical_alignment="center",horizontal_alignment="center"
                )
    message_page = ft.View(
                    "/message",
                    [
                        ft.Row([message_tf,record_btn,send_btn],spacing=5)

                    ],spacing=25,vertical_alignment="end",horizontal_alignment="center"
                )
    


    page.on_keyboard_event = on_keyboard
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main,assets_dir="assets")

