import flet as ft
import time, threading
import whisper
import pyaudio
import wave
import datetime
import os
import asyncio


class Whisper(ft.UserControl):
    def __init__(self, filename,model):
        super().__init__()
        self.filename = filename
        self.model = model
        self.text = None

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.stt())

    async def will_unmount_async(self):
        self.running = False

    async def stt(self):
        self.text.value = self.model.transcribe(self.filename)["text"]
        await self.update_async()

    def build(self):
        self.text = ft.Text()
        return self.text
    
def main(page: ft.Page):
    model = whisper.load_model("base")
    async def start(e):
        await page.add_async(Whisper("assets/wav/2023_04_30_16_35_26.wav",model))
    btn = ft.IconButton(icon=ft.icons.ABC,on_click=start)
    page.add(btn)

ft.app(target=main)