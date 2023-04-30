import flet as ft
import time, threading
import whisper
import pyaudio
import wave
import datetime
import os
import asyncio

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
        self.text.value = self.message_tf.value
        self.text.value += self.model.transcribe(self.filename)["text"]
        await self.update_async()

    def build(self):
        self.text = ft.Text(visible=False)
        return self.text
    
async def main(page: ft.Page):
    page.title = "My Little Friend"
    page.window_height=500
    page.window_width=480
    page.window_min_height = 500
    page.window_min_width=480

    model = whisper.load_model("base")
    message_tf = ft.TextField(autofocus=True,shift_enter=True,expand=True)

    async def close_bs(e):
        global recorder
        recorder.running = False
        recorder.task.cancel() 
        bs.open = False
        temp = Whisper(filename=recorder.filename,model=model)
        await page.add_async(temp)
        await bs.update_async()
        await page.update_async()

        
    async def record_bs(e):
        global recorder
        bs.open = True
        await bs.update_async()
        now = datetime.datetime.now()
        date_format = "%Y_%m_%d_%H_%M_%S"

        now = now.strftime(date_format)

        temp = os.path.join(*["assets","wav",".".join([now,"wav"])])
        recorder = AudioRecord(filename=temp,model=model)
        await page.add_async(recorder)


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
        open=True,
        on_dismiss=close_bs,
    )

    page.overlay.append(bs)
    bs.open = False

    
    await page.add_async(message_tf,record_btn)
    await page.update_async()

ft.app(target=main)