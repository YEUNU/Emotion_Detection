import flet as ft
import time, threading
import whisper
import pyaudio
import wave
import datetime
import os

class AudioRecord(ft.UserControl):
    def __init__(self,filename=None,message_tf=None,model=None):
        super().__init__()
        self.orig_msg = message_tf
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

    def did_mount(self):
        self.running = True
        self.th = threading.Thread(target=self.update_record, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.running = False

    def update_record(self):

        while self.record_status and self.running:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

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

        self.new_msg.value += self.orig_msg
        self.new_msg.value += self.model.transcribe(self.filename)["text"]
        print("result : ",self.new_msg)
        
        self.update()

    def build(self):
        self.new_msg = ft.TextField(visible=False,on_change=self.on_change)
        return self.new_msg
        # return self.countdown

def main(page : ft.Page):
    page.title = "My Little Friend"
    page.window_height=500
    page.window_width=480
    page.window_min_height = 500
    page.window_min_width=480


    model = whisper.load_model("base")
    model.transcribe(os.path.join("assets","wav","init.wav"))
    message_tf = ft.TextField(autofocus=True,shift_enter=True,expand=True)

    def close_bs(e):
        global record_tf
        record_tf.record_status = False
        print(record_tf.new_msg.value)
        bs.open = False
        bs.update()
        page.update()

    def record_bs(e):
        global record_tf
        bs.open = True
        bs.update()
        now = datetime.datetime.now()
        date_format = "%Y_%m_%d_%H_%M_%S"

        now = now.strftime(date_format)

        temp = os.path.join(*["assets","wav",".".join([now,"wav"])])
        record_tf = AudioRecord(filename=temp,message_tf=message_tf.value,model=model)
        page.add(record_tf)



    record_btn = ft.IconButton(icon=ft.icons.KEYBOARD_VOICE,icon_size=35,on_click=record_bs)
    record_stop_button = ft.IconButton(icon = ft.icons.RADIO_BUTTON_CHECKED,icon_color="red", icon_size=100, on_click=close_bs)

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
        open=False,
        on_dismiss=close_bs,
    )

    page.overlay.append(bs)

    page.add(message_tf,record_btn)


ft.app(target=main,assets_dir="assets")