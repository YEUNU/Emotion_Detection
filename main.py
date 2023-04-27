import flet as ft
from glob import glob
import pandas as pd
import os,sys
import numpy as np
import datetime
import pyaudio
import wave
import whisper
import time

try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

class User_contorl():
    def __init__(self):
        super().__init__()

    def account_new(user_name,user_password):
        temp = os.path.join(*["assets","info","user_info.csv"])
        orig = pd.read_csv(temp)
        new = pd.DataFrame()
        new["user_name"] = [user_name]
        new["user_password"] = [user_password]
        result = pd.concat([orig,new],axis=0)
        result.to_csv(temp,index=False)

    def account_check(user_name):
        temp = os.path.join(*["assets","info","user_info.csv"])
        orig = pd.read_csv(temp)
        names = np.unique(orig["user_name"])
        if user_name in names:
            return True
        else:
            return False
    
    def password_check(user_name,input_password):
        temp = os.path.join(*["assets","info","user_info.csv"])
        orig = pd.read_csv(temp)
        pwd = str(*orig["user_password"][orig["user_name"]==user_name].values)
        if input_password == pwd:
            return True
        else:
            return False
    
    def new_password_check(user_password,confirm_pssword):
        if user_password == confirm_pssword:
            return True
        else:
            return False

class Data_control():
    def __init__(self):
        super().__init__()
    
    def save(user_name,time,message,reply,emotion):
        new = pd.DataFrame()
        new["user_name"] = [user_name]
        new["user_time"] = [time]
        new["user_message"] = [message]
        new["user_reply"] = [reply]
        new["user_emotion"] = [emotion]

        temp = os.path.join(*["assets","info","user_message.csv"])
        orig = pd.read_csv(temp)
        result = pd.concat([orig,new],axis=0)
        result.to_csv(temp,index=False)


class AudioRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.chunk = 1024 
        self.format = pyaudio.paInt16  
        self.channels = 1  
        self.rate = 16000  
        self.frames = [] 
        self.recording = False  
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
        self.record_status = False

    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.recording = False
        self.save_to_file()

    def save_to_file(self):
        wave_file = wave.open(self.filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(self.format))
        wave_file.setframerate(self.rate)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()
        self.frames = []

    def run(self, record_status):
        self.record_status = record_status
        if not record_status and self.recording:
            self.stop_recording()
        if self.record_status:
            self.start_recording()
            data = self.stream.read(self.chunk)
            self.frames.append(data)



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
                    border_radius=5,
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
    os.makedirs(os.path.join(*["assets","info"]), exist_ok=True)
    os.makedirs(os.path.join(*["assets","wav"]), exist_ok=True)

    temp = os.path.join(*["assets","info","user_info.csv"])
    try:
        temp = pd.read_csv(temp)
    except:
        df = pd.DataFrame()
        df["user_name"] = None
        df["user_password"] = None
        df.to_csv(temp,index=False)
        
    temp = os.path.join(*["assets","info","user_message.csv"])
    try:
        temp = pd.read_csv(temp)
    except:
        df = pd.DataFrame()
        df["user_name"] = None
        df["user_time"] = None
        df["user_message"] = None
        df["user_reply"] = None
        df["user_emotion"] = None
        df.to_csv(temp,index=False)

def main(page : ft.Page):
    page.title = "My Little Friend"
    page.window_height=800
    page.window_width=480
    page.window_min_height = 800
    page.window_min_width=480
    hf = ft.HapticFeedback()
    page.overlay.append(hf)

    init_system()
    
    user = {
        "user_name" : str(),
        "user_password" : str()
    }
    message = {
        "user_name" : str(),
        "user_time" : str(),
        "user_message" : str(),
        "user_reply" : str(),
        "user_emotion" : str(),
    }

    model = whisper.load_model("base")
    model.transcribe(os.path.join("assets","wav","init.wav"))
    def send(e):
        if not message_tf.value :
            msg = ChatMessage(message_tf.value,"gpt")
            chat.controls.append(msg)
        else:
            msg = ChatMessage(message_tf.value,"user")
            chat.controls.append(msg)
            message_tf.value = str()

        page.update()

    def account_check(e):
        user["user_name"] = user_name_tf.value
        message["user_name"] = user_name_tf.value

        if User_contorl.account_check(user_name_tf.value):
            page.go("/password")
        else:
            page.go("/new_password")

        page.update()

    def new_password_check(e):
        if User_contorl.new_password_check(new_password_tf.value,new_password_check_tf.value):
            user["user_password"] = new_password_tf.value
            User_contorl.account_new(user["user_name"],user["user_password"])
            page.go("/message")
        else:
            new_password_check_tf.error_text = "비밀번호가 다릅니다"

        page.update()

    def password_check(e):
        user_name = user["user_name"]
        input_password = password_tf.value
        if User_contorl.password_check(user_name,input_password):
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
            account_check(user_name_tf.value)

        page.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            main_page
            )
        if page.route == "/new_password":
            page.views.append(
                new_password_page
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

    def close_bs(e):
        global recorder
        recorder.run(False)
        result = model.transcribe(recorder.filename)["text"]
        message_tf.value += result
        bs.open = False
        bs.update()
        page.update()
        
    def record_bs(e):
        bs.open = True
        bs.update()
        record()

    def record():
        global recorder
        now = str(datetime.datetime.now())
        temp = os.path.join(*["assets","wav",".".join([now,"wav"])])
        recorder = AudioRecorder(temp)

        while True:
            recorder.run(True)
            if recorder.recording == False:
                break
        time.sleep(0.1)

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    user_name_tf = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15,width=250,value="admin",on_submit=blank_check)
    password_tf = ft.TextField(label="비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234",on_submit=password_check)
    new_password_tf = ft.TextField(label="사용할 비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234")
    new_password_check_tf = ft.TextField(label="비밀번호 확인",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234",on_submit=new_password_check)
    message_tf = ft.TextField(autofocus=True,shift_enter=True,expand=True,on_submit=send)

    record_btn = ft.IconButton(icon=ft.icons.KEYBOARD_VOICE,icon_size=35,on_click=record_bs)
    record_stop_button = ft.IconButton(icon = ft.icons.RADIO_BUTTON_CHECKED,icon_color="red", icon_size=100, on_click=close_bs)
    send_btn = ft.IconButton(icon=ft.icons.SEND,icon_size=35,on_click=send) 

    chat = ft.ListView(expand=True,spacing=10,auto_scroll=True,horizontal=400)

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    record_stop_button
                ],
                tight=True,alignment=ft.alignment.center
            ),
            padding=10,alignment=ft.alignment.center
        ),
        open=True,
        on_dismiss=close_bs,
    )

    page.overlay.append(bs)
    bs.open = False

    main_page = ft.View(
                "/",
                [
                    ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "black",size = 80),
                    ft.Text(value="편하게 이야기 하는", color="gray100",weight=ft.FontWeight.W_100,size=20,text_align="center"),
                    ft.Text(value="나만의 작은 친구", color="brown200",weight=ft.FontWeight.W_500,size=35,text_align="center"),
                    user_name_tf,
                    ft.ElevatedButton("확인", on_click=blank_check),
                ],spacing=25,vertical_alignment="center",horizontal_alignment="center"
                )
    new_password_page =ft.View(
                    "/new_password",
                    [
                        ft.Icon(name = ft.icons.PASSWORD,color = "black",size = 150),
                        ft.Text(value="사용할 비밀번호를 작성해주세요", color="gray100",weight=ft.FontWeight.W_100,size=20,text_align="center"),
                        new_password_tf,
                        new_password_check_tf,
                        ft.ElevatedButton("확인", on_click=new_password_check),
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

