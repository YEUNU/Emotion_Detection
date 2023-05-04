import flet as ft
import pandas as pd
import os,sys,re
import numpy as np
import datetime
import pyaudio
import wave
import whisper
import asyncio
import gdown
import chatgpt
from chatgpt import generate_gpt3_response

try:
    exe_dir = os.getcwd()
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

user_message = {
    "user_name" : None,
    "user_time" : None,
    "user_message" : None,
    "user_reply" : None,
    "user_emotion" : None,
}
user_info = {
    "user_name" : None,
    "user_password" : None
}

user_info_dir = os.path.join(*[exe_dir,".assets","info","user_info.csv"])
user_message_dir = os.path.join(*[exe_dir,".assets","info","user_message.csv"])


class AudioRecord(ft.UserControl):
    def __init__(self,filename=None,model=None):
        super().__init__()
        self.model = model
        self.record_status = True
        self.filename = filename
        self.chunk = 1024 
        self.format = pyaudio.paInt16  
        self.channels = 1  
        self.rate = 16000  
        self.frames = [] 
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels,
                                      rate=self.rate, input=True,
                                      frames_per_buffer=self.chunk)
        self.task = asyncio.create_task(self.recording())

    async def did_mount(self):
        self.running = True

    async def will_unmount(self):
        self.running = False

    async def recording(self):
        try:
            while True:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
                await asyncio.sleep(0)  # Allow the event loop to run other tasks

        except asyncio.CancelledError:
            pass

        finally:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            wave_file = wave.open(self.filename, 'wb')
            wave_file.setnchannels(self.channels)
            wave_file.setsampwidth(self.audio.get_sample_size(self.format))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(self.frames))
            wave_file.close()
            self.frames = []
            if self.task is not None and not self.task.done():
                self.task.cancel()

    def build(self):
        self.new_msg = ft.Text(visible=False)
        return self.new_msg

class Whisper(ft.UserControl):
    def __init__(self, filename,model,message_tf):
        super().__init__()
        self.filename = filename
        self.model = model
        self.message_tf = message_tf

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.stt())

    async def will_unmount_async(self):
        self.running = False

    async def stt(self):
        self.text = self.message_tf.value
        self.text += self.model.transcribe(self.filename)["text"]
        await self.update_async()

    def build(self):
        self.bar = ft.ProgressBar(expand=True)
        return self.bar

class gpt(ft.UserControl):
    def __init__(self, sen):
        super().__init__()
        self.sen = sen
        self.text = None
        self.msg = ChatMessage(message_type="gpt_load")

    async def did_mount_async(self):
        asyncio.create_task(self.gpt())

    async def will_unmount_async(self):
        pass
    

    async def gpt(self):
        self.text = generate_gpt3_response(chatgpt.conversation, self.sen)
        user_message["user_reply"] = [self.text]

    def build(self):
        self.bar = ft.ProgressBar(expand=True)
        return self.bar
    
class User_contorl():
    def account_new(user_name,user_password):
        orig = pd.read_csv(user_info_dir)
        new = pd.DataFrame()
        new["user_name"] = [user_name]
        new["user_password"] = [user_password]
        result = pd.concat([orig,new],axis=0)
        result.to_csv(user_info_dir,index=False)

    def account_check(user_name):
        orig = pd.read_csv(user_info_dir)
        names = np.unique(orig["user_name"])
        if user_name in names:
            return True
        else:
            return False
    
    def password_check(user_name,user_password):
        orig = pd.read_csv(user_info_dir)
        pwd = str(*orig["user_password"][orig["user_name"]==user_name].values)

        if user_password == pwd:
            return True
        else:
            return False
        
    def new_password_check(new_password,new_password_check):
        if new_password == new_password_check:
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

        orig = pd.read_csv(user_message_dir)
        result = pd.concat([orig,new],axis=0)
        result.to_csv(user_message_dir,index=False)

class ChatMessage(ft.Row):
    def __init__(self, text=None,message_type=None):
        super().__init__()
        self.text = text
        self.message_type = message_type
        if self.message_type == "user":
            self.controls = [
                ft.Container(
                    ft.Text(self.text, selectable=True),
                    alignment=ft.alignment.center_right,
                    bgcolor=ft.colors.LIGHT_BLUE_50,
                    padding=15,
                    margin=5,
                    border_radius=10,
                    expand=True
                    ),
                ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                    size=40,
                    color=ft.colors.BLACK45
                    )
            ]
        elif self.message_type == "gpt":
            self.controls = [
                ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                    size=40,
                    color=ft.colors.BLACK45
                    ),
                ft.Container(
                    ft.Text(self.text, selectable=True),
                    alignment=ft.alignment.center_right,
                    bgcolor=ft.colors.LIGHT_GREEN_50,
                    padding=15,
                    margin=5,
                    border_radius=10,
                    expand=True
                    )
            ]
        elif self.message_type == "gpt_load":
            self.controls = [
                ft.Icon(
                    name=ft.icons.ACCOUNT_CIRCLE,
                    size=40,
                    color=ft.colors.BLACK45
                    ),
                ft.Container(
                    ft.Text(value="",visible=False),
                    ft.ProgressRing(),
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.LIGHT_GREEN_50,
                    padding=15,
                    margin=5,
                    border_radius=10,
                    expand=True
                    )
            ]

    
def init_system():
    os.makedirs(os.path.join(*[exe_dir,".assets","info"]), exist_ok=True)
    os.makedirs(os.path.join(*[exe_dir,".assets","wav"]), exist_ok=True)

    try:
        pd.read_csv(user_info_dir)
    except:
        df = pd.DataFrame()
        df["user_name"] = None
        df["user_password"] = None
        df.to_csv(user_info_dir,index=False)
        
    try:
        pd.read_csv(user_message_dir)
    except:
        df = pd.DataFrame()
        df["user_name"] = None
        df["user_time"] = None
        df["user_message"] = None
        df["user_reply"] = None
        df["user_emotion"] = None
        df.to_csv(user_message_dir,index=False)

async def main(page : ft.Page):
    page.title = "My Little Friend"
    page.window_height=800
    page.window_width=480
    page.window_min_height = 800
    page.window_min_width=480
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    init_system()

    whisper_model = whisper.load_model("base")
    dest_path = os.path.join(exe_dir,"emotion_detect","multi-datasetklue-bert-token_len_64-batch_size_16-drop_out_0.5-lr_2e-05-weight_decay_0.01 + 9.pth")
    if not os.path.isfile(dest_path):
        gdown.download("https://drive.google.com/uc?id=1laKn5IbhOIi5vEOqE0Jh1xCNDX0vyCgL",dest_path)

    import emotion_detect
    from emotion_detect import EmotionClassifier

    async def new_pwd_check(e):
        if User_contorl.new_password_check(new_pwd_tf.value,new_pwd_chk_tf.value):
            user_info["user_password"] = new_pwd_tf.value
            User_contorl.account_new(user_info["user_name"],user_info["user_password"])
            app.selected_index = 3
        else:
            new_pwd_chk_tf.error_text = "비밀번호가 다릅니다"

        await page.update_async()

    async def account_check(e):
        user_info["user_name"] = user_name_tf.value
        user_message["user_name"] = user_name_tf.value

        if User_contorl.account_check(user_name_tf.value):
            app.selected_index = 1
        else:
            app.selected_index = 2

        await page.update_async()
    
    async def blank_check(e):
        if user_name_tf.value :
            await account_check(user_name_tf.value)

        else:
            user_name_tf.error_text = "이름을 입력해주세요"

        await page.update_async()

    async def pwd_check(e):
        user_name = user_info["user_name"]
        inp = pwd_tf.value
        if User_contorl.password_check(user_name,inp):
            app.selected_index = 3
        else:
            pwd_tf.error_text = "비밀번호가 틀렸습니다"

        await page.update_async()

    async def emotion(user_sen):
        return emotion_detect.emotion_classifier.predict(user_sen)
    
    async def send(e):
        if msg_tf.value:
            now = datetime.datetime.now()
            date_format = "%Y_%m_%d_%H_%M_%S"
            now = now.strftime(date_format)

            user_sen = msg_tf.value
            msg = ChatMessage(user_sen,"user")
            chat.controls.append(msg)
            msg_tf.value = str()

            chatgpt.conversation[0]['content'] = re.sub(r'\s+', ' ', chatgpt.conversation[0]['content'].strip())
            emotion_pred = await emotion(user_sen)

            if emotion_pred[0] in ['분노', '불안', '슬픔', '혐오']:
                changed_sen = '공감해 줘. 조언해 줘. ' + user_sen
            else:
                changed_sen = '공감해 줘. ' +  user_sen

            temp = gpt(changed_sen)
            await page.add_async(temp)

            await page.remove_async(temp)
            await page.update_async()

            rp = ChatMessage(*user_message["user_reply"],"gpt")
            chat.controls.append(rp)
            
            await page.update_async()
            user_message["user_time"] = [now]
            user_message["user_message"] = [user_sen]
            user_message["user_emotion"] = [emotion_pred]

            orig = pd.read_csv(user_message_dir)
            new = pd.DataFrame.from_dict(user_message,orient="columns")
            
            new = pd.concat([orig,new],axis=0)
            print(new)
            new.to_csv(user_message_dir,index=False)

    async def close_bs(e):
        global recorder
        recorder.running = False
        recorder.task.cancel() 
        bs.open = False
        temp = Whisper(filename=recorder.filename,model=whisper_model,message_tf=msg_tf)
        await page.add_async(temp)
        await bs.update_async()
        await asyncio.sleep(0.1)
        msg_tf.value = temp.text
        await page.remove_async(temp)
        page.controls.pop()
        await page.update_async()
        
    async def record_bs(e):
        global recorder
        bs.open = True
        await bs.update_async()
        now = datetime.datetime.now()
        date_format = "%Y_%m_%d_%H_%M_%S"

        now = now.strftime(date_format)
        user_message["user_time"] = [now]
        temp = os.path.join(*[exe_dir,".assets","wav",".".join([now,"wav"])])
        recorder = AudioRecord(filename=temp,model=whisper_model)
        await page.add_async(recorder)

    user_name_tf = ft.TextField(label="이름",hint_text = "이름을 작성해주세요",text_size=15,width=250,value="admin",on_submit=blank_check)
    pwd_tf = ft.TextField(label="비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234",on_submit=pwd_check)
    new_pwd_tf = ft.TextField(label="사용할 비밀번호",hint_text = "비밀번호를 작성해주세요",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234")
    new_pwd_chk_tf = ft.TextField(label="비밀번호 확인",text_size=15,password=True, can_reveal_password=True,width=250,keyboard_type="NUMBER",value="1234",on_submit=new_pwd_check)
    msg_tf = ft.TextField(autofocus=True,shift_enter=True,expand=True,on_submit=send)

    chat = ft.ListView(expand=True,spacing=10,auto_scroll=True,horizontal=400)

    record_btn = ft.IconButton(icon=ft.icons.KEYBOARD_VOICE,icon_size=35,on_click=record_bs)
    record_stop_button = ft.IconButton(icon = ft.icons.RADIO_BUTTON_CHECKED,icon_color="red", icon_size=100, on_click=close_bs)
    send_btn = ft.IconButton(icon=ft.icons.SEND,icon_size=35,on_click=send) 
    
    main_page = ft.Container(
        content=ft.Column([
            ft.Icon(name = ft.icons.QUESTION_ANSWER,color = "black",size = 100),
            ft.Text(value="편하게 이야기 하는", color="gray100",weight=ft.FontWeight.W_100,size=20,text_align="center"),
            ft.Text(value="나만의 작은 친구", color="brown200",weight=ft.FontWeight.W_500,size=35,text_align="center"),
            user_name_tf,
            ft.ElevatedButton("확인", on_click=blank_check),
        ],alignment="center",horizontal_alignment="center",spacing=35,expand=True),expand=True
    )

    pwd_page = ft.Container(
        content=ft.Column([
            ft.Icon(name = ft.icons.PASSWORD,color = "black",size = 150),
            pwd_tf,
            ft.ElevatedButton("확인", on_click=pwd_check),
        ],alignment="center",horizontal_alignment="center",spacing=35,expand=True),expand=True
    )

    new_pwd_page = ft.Container(
        content=ft.Column([
            ft.Icon(name = ft.icons.PASSWORD,color = "black",size = 150),
            ft.Text(value="사용할 비밀번호를 작성해주세요", color="gray100",weight=ft.FontWeight.W_100,size=20,text_align="center"),
            new_pwd_tf,
            new_pwd_chk_tf,
            ft.ElevatedButton("확인", on_click=new_pwd_check),
        ],alignment="center",horizontal_alignment="center",spacing=35,expand=True),expand=True
    )

    msg_page = ft.Container(
        content=ft.Column([
                        chat,
                        ft.Row([msg_tf,record_btn,send_btn],spacing=5)
        ],alignment="center",horizontal_alignment="center",spacing=35,expand=True),expand=True
    )

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    record_stop_button
                ],
                tight=True,alignment=ft.alignment.center,expand=True
            ),
            padding=10,alignment=ft.alignment.center,expand=True
        ),
        open=False,
        on_dismiss=close_bs,
    )

    page.overlay.append(bs)

    app = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
            content=main_page,
            tab_content=None
                ),
                ft.Tab(
            tab_content=None,
            content=pwd_page
                ),
                ft.Tab(
            tab_content=None,
            content=new_pwd_page
                ),
                ft.Tab(
            tab_content=None,
            content=msg_page
                ),
            ],expand=True)
    


    await page.add_async(app)
    await page.update_async()

ft.app(target=main)