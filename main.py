import flet as ft
from flet import KeyboardEvent, Page
from flet import Text
from glob import glob
import pandas as pd
import os,sys

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

class ChatMessage(ft.Row):
    def __init__(self, text,message_type):
        super().__init__()
        if message_type == "user":
            self.controls = [
                ft.Container(
                    ft.Text(text, selectable=True),
                    alignment=ft.alignment.center_right,
                    bgcolor=ft.colors.LIGHT_BLUE_50,
                    width=380,
                    height=40,
                    padding=5,
                    margin=5,
                    border_radius=5
                    ),
                ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                    size=40,
                    color=ft.colors.BLACK45
                    )
            ]
        else:
            self.controls = [
                ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                    size=40,
                    color=ft.colors.BLACK45
                    ),
                ft.Container(
                    ft.Text(text, selectable=True),
                    alignment=ft.alignment.center_right,
                    bgcolor=ft.colors.LIGHT_GREEN_50,
                    width=380,
                    height=40,
                    padding=5,
                    margin=5,
                    border_radius=5
                    )
            ]
    
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
    try:
        user_info_df = pd.read_csv("./assets/info/user_info.csv")
    except:
        df = pd.DataFrame(columns=["user_name","password","recent_emotion"])
        df.to_csv("./assets/info/user_info.csv")
    finally:
        user_info_df = pd.read_csv("./assets/info/user_info.csv")

    try:
        user_message_df = pd.read_csv("./assets/info/user_message.csv")
    except:
        df = pd.DataFrame(columns=["user_name","time","message","reply","emotion"])
        df.to_csv("./assets/info/user_message.csv")
    finally:
        user_message_df = pd.read_csv("./assets/info/user_message.csv")

    assets["fonts"] = fonts
    assets["imgs"] = imgs
    assets["user_info"] = user_info_df
    assets["user_message"] = user_message_df

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

    def send(e):
        if not message_tf.value :
            pass
        else:
            user_message = ChatMessage(message_tf.value,"user")
            chat.controls.append(user_message)
            message_tf.value = str()

        page.update()

    def password_check(e):
        correct = "1234"
        
        if password_tf.value == correct:
            page.go("/message")

        else:
            hf.vibrate()
            password_tf.error_text = "비밀번호가 틀렸습니다"

        page.update()

    def blank_check(e):
        if not user_name_tf.value :
            hf.vibrate()
            user_name_tf.error_text = "이름을 입력해주세요"

        else:
            page.go("/password")

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

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    user_name_tf = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15,width=250,value="admin",on_submit=blank_check)
    password_tf = ft.TextField(label="비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234",on_submit=password_check)
    message_tf = ft.TextField(autofocus=True,shift_enter=True,expand=True,on_submit=send)

    record_btn = ft.IconButton(icon=ft.icons.KEYBOARD_VOICE,icon_size=35)
    send_btn = ft.IconButton(icon=ft.icons.SEND,icon_size=35,on_click=send) 

    chat = ft.ListView(expand=True,spacing=10,auto_scroll=True,)

    main_page = ft.View(
                "/",
                [
                    ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "black",size = 80),
                    ft.Text(value="편하게 이야기 하는", color="gray100",font_family="nanum_light",size=20,text_align="center"),
                    ft.Text(value="나만의 작은 친구", color="brown200",font_family="nanum_extrabold",size=35,text_align="center"),
                    user_name_tf,
                    ft.ElevatedButton("확인", on_click=blank_check),
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
                        chat,
                        ft.Row([message_tf,record_btn,send_btn],spacing=5)

                    ],spacing=25,vertical_alignment="end",horizontal_alignment="center"
                )
    

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main,assets_dir="assets")

