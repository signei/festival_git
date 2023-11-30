import flet as ft
import pandas as pd
from utils import *
import time
import threading
from asyncio import create_task, wait, run
import pygame

"""
언젠간 클래스 만들어서 해야지,...
"""

# path = 'C:/Users/bio/Documents/festival/'

def main(page: ft.Page):
    page.fonts = {
        "Nanum" : "fonts/NanumSquareRoundB.ttf",
    }
    page.theme = ft.Theme(font_family="Nanum")
    user_info = dict()
    ca_size = 270
    button_radius = 10

    def button_click(e):
        if page.window_full_screen == True:
            page.window_full_screen = False
            page.update()
        elif page.window_full_screen == False:
            page.window_full_screen = True
            page.update()

    def record_listen(idx):
        pygame.mixer.init()
        f = f"./data/{user_info['id'][0]}/{user_info['id'][0]}_{idx}.wav"
        pygame.mixer.music.load(f)
        pygame.mixer.music.play()

    async def update_progress_bar(e):
        page.views[-1].controls[-2].controls[e].controls.append(pb)
        for i in range(0, 100):
            pb.value = i * 0.01
            await asyncio.sleep(0.03)
            page.update()
        pb.value = 1
        page.update()
        page.views[-1].controls[-2].controls[e].controls.pop()

    async def record_assemble(e):
        # Start recording and progress bar update tasks
        recording_task = create_task(async_start_recording(user_info["id"], e))
        progress_task = create_task(update_progress_bar(e))

        # Run both tasks concurrently
        completed, pending = await wait([recording_task, progress_task], return_when="ALL_COMPLETED")

    def record_display(e):
        run(record_assemble(e))

    def route_change(route):

        def page_main():
            rail = ft.Row(
                controls=[
                    ft.Stack(
                        [
                            ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal1.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                            ft.ElevatedButton(opacity=0,
                                              width=ca_size,
                                              height=ca_size,
                                              on_click=lambda _: audio_criminal1.play())
                        ],
                    ),

                    ft.Stack(
                        [
                            ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal2.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                            ft.ElevatedButton(opacity=0,
                                              width=ca_size,
                                              height=ca_size,
                                              on_click=lambda _: audio_criminal2.play()),
                        ]
                    ),

                    ft.Stack(
                        [
                            ft.CircleAvatar(content=ft.Image(src = 'assets/img/gambler.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                            ft.ElevatedButton(opacity=0,
                                              width=ca_size,
                                              height=ca_size,
                                              on_click=lambda _: audio_gambler.play()),
                        ]
                    ),

                    ft.Stack(
                        [
                            ft.CircleAvatar(content=ft.Image(src = 'assets/img/glory.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                            ft.ElevatedButton(opacity=0,
                                              width=ca_size,
                                              height=ca_size,
                                              on_click=lambda _: audio_glory.play()),
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            return ft.View(
                "/",
                [
                    ft.Text(value="성대모사 챌린지",
                            size=int(ca_size/2)),
                    ft.ElevatedButton(text="전체화면", on_click=button_click,),
                    rail,
                    ft.ElevatedButton(content = ft.Text("참가하기", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/4),
                                      on_click=lambda _: page.go("/participate")),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )

        def page_participate():
            student_department = ft.TextField(
                label="학과",
                multiline=False,
                width=int(ca_size + ca_size/3),
                text_size = ca_size/10)

            student_id = ft.TextField(
                label="학번",
                multiline=False,
                width=int(ca_size + ca_size/3),
                text_size = ca_size/10)

            student_name = ft.TextField(
                label="이름",
                multiline=False,
                width=int(ca_size + ca_size/3),
                text_size = ca_size/10)

            student_phone = ft.TextField(
                label="휴대전화",
                multiline=False,
                width=int(ca_size + ca_size/3),
                text_size = ca_size/10)

            def student_info_save(d, i, n, p):
                user_info["department"] = [str(d)]
                user_info["id"] = [str(i)]
                user_info["name"] = [str(n)]
                user_info["phone"] = [str(p)]
                user_info["criminal1"] = [0]
                user_info["criminal2"] = [0]
                user_info["gambler"] = [0]
                user_info["glory"] = [0]

                page.go("/listen")

            return ft.View(
                "/participate",
                [
                    ft.Text("참가 정보", size=int(ca_size/4)),
                    student_department,
                    student_id,
                    student_name,
                    student_phone,
                    ft.ElevatedButton(content = ft.Text("확인", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size/2),
                                      height=int(ca_size/4),
                                      on_click=lambda _: student_info_save(student_department.value,
                                                                           student_id.value,
                                                                           student_name.value,
                                                                           student_phone.value))
                ],
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_listen():
            rail = ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Stack(
                                [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal1.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                                 ft.ElevatedButton(opacity=0,
                                                   width=ca_size,
                                                   height=ca_size,
                                                   on_click=lambda _: page.go("/criminal1")),],
                            ),
                            ft.Text(value="진실의 방으로",
                                    size=int(ca_size/8)),
                            ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_criminal1.play()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                    ),
                    ft.Column(
                        controls=[
                            ft.Stack(
                                [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal2.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                                 ft.ElevatedButton(opacity=0,
                                                   width=ca_size,
                                                   height=ca_size,
                                                   on_click=lambda _: page.go("/criminal2")),]
                            ),
                            ft.Text(value="너 납치된거야",
                                    size=int(ca_size/8)),
                            ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_criminal2.play()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Column(
                        controls=[
                            ft.Stack(
                                [ft.CircleAvatar(content=ft.Image(src = 'assets/img/gambler.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                                 ft.ElevatedButton(opacity=0,
                                                   width=ca_size,
                                                   height=ca_size,
                                                   on_click=lambda _: page.go("/gambler")),]
                            ),
                            ft.Text(value="쏠 수 있어",
                                    size=int(ca_size/8)),
                            ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_gambler.play()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Column(
                        controls=[
                            ft.Stack(
                                [ft.CircleAvatar(content=ft.Image(src = 'assets/img/glory.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                                 ft.ElevatedButton(opacity=0,
                                                   width=ca_size,
                                                   height=ca_size,
                                                   on_click=lambda _: page.go("/glory")),]
                            ),
                            ft.Text(value="멋지다 연진아",
                                    size=int(ca_size/8)),
                            ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_glory.play()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            return ft.View(
                "/listen",
                [
                    rail,
                    ft.Text("위의 사진을 클릭하여 모사할 대사를 선택하세요", size=int(ca_size/10))
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )

        def page_criminal1():
            user_info["act"] = "criminal1"
            return ft.View(
                "/criminal1",
                [
                    ft.Stack(
                        [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal1.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                         ft.ElevatedButton(opacity=0,
                                           width=ca_size,
                                           height=ca_size,
                                           on_click=lambda _: audio_criminal1.play())]),
                    ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_criminal1.play()),

                    ft.Row(controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(0)),
                            ]
                        ),

                        ft.Column(
                            controls=[
                                    ft.ElevatedButton(content = ft.Text("첫번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(0)),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("두번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(2)),
                            ]
                        ),

                        ft.Column(
                            controls=[ft.ElevatedButton(content = ft.Text("두번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(2)),
                                      ]
                        ),
                    ],
                        spacing=int(ca_size/5),
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.ElevatedButton(content = ft.Text("제출", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size/2),
                                      height=int(ca_size/4),
                                      on_click=lambda e: page.go("/inference"),)

                ],
                ft.ElevatedButton(content = ft.Text("뒤로가기", size = ca_size/20), on_click=lambda e: page.go("/listen")),
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_criminal2():
            user_info["act"] = "criminal2"
            return ft.View(
                "/criminal2",
                [
                    ft.Stack(
                        [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal2.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                         ft.ElevatedButton(opacity=0,
                                           width=ca_size,
                                           height=ca_size,
                                           on_click=lambda _: audio_criminal2.play())]),
                    ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_criminal2.play()),

                    ft.Row(controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(0)),
                            ]
                        ),

                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(0)),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("두번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(2)),
                            ]
                        ),

                        ft.Column(
                            controls=[ft.ElevatedButton(content = ft.Text("두번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(2)),
                                      ]
                        ),
                    ],
                        spacing=int(ca_size/5),
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.ElevatedButton(content = ft.Text("제출", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size/2),
                                      height=int(ca_size/4),
                                      on_click=lambda e: page.go("/inference"),)

                ],
                ft.ElevatedButton(content = ft.Text("뒤로가기", size = ca_size/20), on_click=lambda e: page.go("/listen")),
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_gambler():
            user_info["act"] = "gambler"
            return ft.View(
                "/gambler",
                [
                    ft.Stack(
                        [ft.CircleAvatar(content=ft.Image(src = 'assets/img/gambler.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                         ft.ElevatedButton(opacity=0,
                                           width=ca_size,
                                           height=ca_size,
                                           on_click=lambda _: audio_gambler.play())]),
                    ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_gambler.play()),

                    ft.Row(controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(0)),
                            ]
                        ),

                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(0)),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("두번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(2)),
                            ]
                        ),

                        ft.Column(
                            controls=[ft.ElevatedButton(content = ft.Text("두번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(2)),
                                      ]
                        ),
                    ],
                        spacing=int(ca_size/5),
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.ElevatedButton(content = ft.Text("제출", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size/2),
                                      height=int(ca_size/4),
                                      on_click=lambda e: page.go("/inference"),)

                ],
                ft.ElevatedButton(content = ft.Text("뒤로가기", size = ca_size/20), on_click=lambda e: page.go("/listen")),
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_glory():
            user_info["act"] = "glory"
            return ft.View(
                "/glory",
                [
                    ft.Stack(
                        [ft.CircleAvatar(content=ft.Image(src = 'assets/img/glory.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                            width=ca_size,
                                            height=ca_size),
                         ft.ElevatedButton(opacity=0,
                                           width=ca_size,
                                           height=ca_size,
                                           on_click=lambda _: audio_glory.play())]),
                    ft.ElevatedButton(content = ft.Text("듣기", size = ca_size/28),
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                              width=int(ca_size/4),
                                              height=int(ca_size/8),
                                              on_click=lambda _: audio_glory.play()),

                    ft.Row(controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(0)),
                            ]
                        ),

                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("첫번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(0)),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(content = ft.Text("두번째 녹음", size = ca_size/8, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_display(2)),
                            ]
                        ),

                        ft.Column(
                            controls=[ft.ElevatedButton(content = ft.Text("두번째 녹음 듣기", size = ca_size/10, color="WHITE"),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=ca_size,
                                      height=int(ca_size/2),
                                      bgcolor = "PRIMARY",
                                      on_click=lambda e: record_listen(2)),
                                      ]
                        ),
                    ],
                        spacing=int(ca_size/5),
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.ElevatedButton(content = ft.Text("제출", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size/2),
                                      height=int(ca_size/4),
                                      on_click=lambda e: page.go("/inference"),)

                ],
                ft.ElevatedButton(content = ft.Text("뒤로가기", size = ca_size/20), on_click=lambda e: page.go("/listen")),
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_inference():
            
            if len(os.listdir(f"./data/{user_info['id'][0]}")) != 2:
                page.go('/listen')
            
            score = predict(user_info["act"], user_info["id"][0])
            print("predict score : ", score)
            user_info[user_info["act"]] = [score]
            if not os.path.exists("user_info.csv"):
                result = pd.DataFrame(user_info)

            else:
                old_info = pd.read_csv("user_info.csv")
                new_info = pd.DataFrame(user_info)
                result = pd.concat([old_info, new_info])

            result.to_csv("user_info.csv", index=False)

            if user_info["act"] == "criminal1":
                ca = ft.Stack(
                    [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal1.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                     width=ca_size,
                                     height=ca_size),
                     ft.ElevatedButton(opacity=0,
                                       width=ca_size,
                                       height=ca_size,
                                       on_click=lambda _: audio_criminal1.play())])
            elif user_info["act"] == "criminal2":
                ca = ft.Stack(
                    [ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal2.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                     width=ca_size,
                                     height=ca_size),
                     ft.ElevatedButton(opacity=0,
                                       width=ca_size,
                                       height=ca_size,
                                       on_click=lambda _: audio_criminal2.play())])
            elif user_info["act"] == "gambler":
                ca = ft.Stack(
                    [ft.CircleAvatar(content=ft.Image(src = 'assets/img/gambler.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                     width=ca_size,
                                     height=ca_size),
                     ft.ElevatedButton(opacity=0,
                                       width=ca_size,
                                       height=ca_size,
                                       on_click=lambda _: audio_gambler.play())])
            elif user_info["act"] == "glory":
                ca = ft.Stack(
                    [ft.CircleAvatar(content=ft.Image(src = 'assets/img/glory.gif', width = ca_size, height= ca_size, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size)),
                                     width=ca_size,
                                     height=ca_size),
                     ft.ElevatedButton(opacity=0,
                                       width=ca_size,
                                       height=ca_size,
                                       on_click=lambda _: audio_glory.play())])
            return ft.View(
                "/inference",
                controls=[
                    ca,
                    ft.Text("당신의 점수는?", size = ca_size/4),
                    ft.ElevatedButton(content = ft.Text("확인하기", size = ca_size/6),
                                      on_click=lambda _:page.go("/show"), width=int(ca_size),
                                      height=int(ca_size/2))

                ],
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        def page_show():
            return ft.View(
                "./show",
                controls=[
                    ft.Text(
                        f"{user_info['name'][0]}님의 점수는 \n {user_info[user_info['act']][0]}점 입니다!",
                        size=int(ca_size/2)),
                    ft.ElevatedButton(content = ft.Text("처음으로", size = ca_size/6),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=button_radius)),
                                      width=int(ca_size),
                                      height=int(ca_size/2),
                                      on_click=lambda _:page.go("/")),

                ],
                spacing=int(ca_size/10),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )

        page.views.clear()

        if page.route == "/":
            page.views.append(
                page_main()
            )

        elif page.route == "/participate":
            page.views.append(
                page_participate()
            )

        elif page.route == "/listen":
            page.views.append(
                page_listen()
            )

        elif page.route == "/criminal1":
            page.views.append(
                page_criminal1()
            )

        elif page.route == "/criminal2":
            page.views.append(
                page_criminal2()
            )

        elif page.route == "/gambler":
            page.views.append(
                page_gambler()
            )

        elif page.route == "/glory":
            page.views.append(
                page_glory()
            )

        elif page.route == "/inference":
            page.views.append(
                page_inference()
            )

        elif page.route == "/show":
            page.views.append(
                page_show()
            )

        page.overlay.append(audio_criminal1)
        page.overlay.append(audio_criminal2)
        page.overlay.append(audio_gambler)
        page.overlay.append(audio_glory)

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    audio_criminal1 = ft.Audio(src="./sample/criminal1_sample.wav")
    audio_criminal2 = ft.Audio(src="./sample/criminal2_sample.wav")
    audio_gambler = ft.Audio(src="./sample/gambler_sample.wav")
    audio_glory = ft.Audio(src="./sample/glory_sample.wav")

    page.padding = 50
    page.theme_mode = "light"
    page.window_full_screen = True
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    pb = ft.ProgressBar(width=ca_size)


ft.app(target=main)
