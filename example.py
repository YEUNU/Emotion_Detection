import flet as ft

def main(page : ft.Page):
    txt_kor = ft.TextField(value = "한국어로 명령을 입력하시오.")
    btn_send = ft.ElevatedButton(text = "실행")
    txt_eng = ft. TextField(value = "영어로 번역된 명령입니다.")
    txt_python = ft. TextField(value = "Python Code")

    first_row = ft.Row(controls = [txt_kor, btn_send])
    first_column = ft.Column(controls = [first_row, txt_eng, txt_python])

    page.add(first_column)

ft.app(target = main)