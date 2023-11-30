import flet as ft
import pandas as pd
import os
import time

# path = 'C:/Users/bio/Documents/festival/'

def main(page: ft.Page):
    page.fonts = {
        "Nanum" : "fonts/NanumSquareRoundB.ttf",
    }
    page.theme = ft.Theme(font_family="Nanum")
    page.bgcolor = "#F1F3F5"
    page.padding = 50
    page.theme_mode = "light"
    page.window_full_screen = True
    page.window_always_on_top = True

    user_info_csv = os.path.join("user_info.csv")

    # user_info_csv = "random_numbers.csv"
    lv_criminal1 = ft.ListView(
        expand=1, spacing=10, padding=20)
    lv_criminal2 = ft.ListView(
        expand=1, spacing=10, padding=20)
    lv_gambler = ft.ListView(expand=1, spacing=10,
                             padding=20)
    lv_glory = ft.ListView(expand=1, spacing=10, padding=20)

    ca_size = 60

    say_list = ["범죄도시 1", "범죄도시 2", "타짜", "더 글로리"]
    
    def button_click(e):
        
        if page.window_full_screen == True:
            page.window_full_screen = False
            page.update()
        elif page.window_full_screen == False:
            page.window_full_screen = True
            page.update()

    def items():
        items = []
        for i in say_list:
            items.append(
                ft.Container(
                    content = ft.Text(i, size = ca_size/3), expand=1, padding=20,
                )
            )
        return items
    
    # def page_resize(e):
    #     print("New page size:", page.window_width, page.window_height)

    # page.on_resize = page_resize


    page.add(
        ft.Row(
            controls=[ft.Text("점수표",
                              size=ca_size/2)],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,

        ),
        ft.Row(
            controls=[
                ft.Stack(
                    [
                        ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal1.gif', width = ca_size*2, height= ca_size*2, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size*2)),
                                        width=ca_size*2,
                                        height=ca_size*2),
                    ]
                ),

                ft.Stack(
                    [
                        ft.CircleAvatar(content=ft.Image(src = 'assets/img/criminal2.gif', width = ca_size*2, height= ca_size*2, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size*2)),
                                        width=ca_size*2,
                                        height=ca_size*2),
                    ]
                ),

                ft.Stack(
                    [
                        ft.CircleAvatar(content=ft.Image(src = 'assets/img/gambler.gif', width = ca_size*2, height= ca_size*2, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size*2)),
                                        width=ca_size*2,
                                        height=ca_size*2),
                    ]
                ),

                ft.Stack(
                    [
                        ft.CircleAvatar(content=ft.Image(src = 'assets/img/glory.gif', width = ca_size*2, height= ca_size*2, fit = ft.ImageFit.COVER, border_radius=ft.border_radius.all(ca_size*2)),
                                        width=ca_size*2,
                                        height=ca_size*2),
                    ]
                ),
            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.CENTER,),
        ft.Row(controls = items(), spacing=10, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER,),
        ft.Row(
            [
                lv_criminal1,
                ft.VerticalDivider(width=1),
                lv_criminal2,
                ft.VerticalDivider(width=1),
                lv_gambler,
                ft.VerticalDivider(width=1),
                lv_glory,
            ],
            spacing=0,
            expand=True,
        ),
    )
    page.add(ft.ElevatedButton(text="전체화면", on_click=button_click))
    page.add(ft.ElevatedButton(text="새로고침", on_click=page.update()))

    previous_time = 0.0
    while True:
        time.sleep(1)
        if not os.path.exists(user_info_csv):
            continue

        else:
            current_time = os.path.getmtime(user_info_csv)
            if previous_time != current_time:
                lv_criminal1.controls.clear()
                lv_criminal2.controls.clear()
                lv_gambler.controls.clear()
                lv_glory.controls.clear()

                user_info_df = pd.read_csv(user_info_csv)
                cnt_criminal1 = 0
                cnt_criminal2 = 0
                cnt_gambler = 0
                cnt_glory = 0

                for i in ["criminal1", "criminal2", "gambler", "glory"]:
                    sorted_df = user_info_df.sort_values(by=i, ascending=False)
                    for _, row in sorted_df.iterrows():
                        score = row[i]
                        id = row["name"]
                        act = i

                        if float(score) != 0.0:
                            if act == "criminal1":
                                if cnt_criminal1 < 5:
                                    lv_criminal1.controls.append(ft.Row(controls=[
                                        ft.Image(
                                            src = 'assets/img/crown.png',
                                            width=int(ca_size/3),
                                            height=int(ca_size/3),
                                            ),
                                        # ft.Text(f"{cnt_criminal1+1}등 {id} : {score}",
                                        #         size=int(ca_size/4)),]))
                                        ft.Text(weight=ft.FontWeight.W_900, spans=[
                                                ft.TextSpan(f"{cnt_criminal1+1}등 ", ft.TextStyle(size=ca_size/5, color="#E3C04D",)),
                                                ft.TextSpan(f"{id} : ", ft.TextStyle(size=ca_size/5,)),
                                                ft.TextSpan(f"{score}", ft.TextStyle(size=ca_size/3, color="#374999",)),])]))
                                else:
                                    lv_criminal1.controls.append(ft.Text(f"{cnt_criminal1+1}등 {id} : {score}",
                                                                     size=int(ca_size/6)))
                                cnt_criminal1 += 1

                            elif act == "criminal2":
                                if cnt_criminal2 < 5:
                                    lv_criminal2.controls.append(ft.Row(controls=[
                                        ft.Image(
                                            src = 'assets/img/crown.png',
                                            width=int(ca_size/3),
                                            height=int(ca_size/3),
                                            fit=ft.ImageFit.CONTAIN),
                                        # ft.Text(f"{cnt_criminal1+1}등 {id} : {score}",
                                        #         size=int(ca_size/4)),]))
                                        ft.Text(weight=ft.FontWeight.W_900, spans=[
                                                ft.TextSpan(f"{cnt_criminal2+1}등 ", ft.TextStyle(size=ca_size/5, color="#E3C04D",)),
                                                ft.TextSpan(f"{id} : ", ft.TextStyle(size=ca_size/5,)),
                                                ft.TextSpan(f"{score}", ft.TextStyle(size=ca_size/3, color="#374999",)),])]))

                                else:
                                    lv_criminal2.controls.append(ft.Text(f"{cnt_criminal2+1}등 {id} : {score}",
                                                                     size=int(ca_size/6)))
                                cnt_criminal2 += 1

                            elif act == "gambler":
                                if cnt_gambler < 5:
                                    lv_gambler.controls.append(ft.Row(controls=[
                                        ft.Image(
                                            src = 'assets/img/crown.png',
                                            width=int(ca_size/3),
                                            height=int(ca_size/3),
                                            fit=ft.ImageFit.CONTAIN),
                                        # ft.Text(f"{cnt_criminal1+1}등 {id} : {score}",
                                        #         size=int(ca_size/4)),]))
                                        ft.Text(weight=ft.FontWeight.W_900, spans=[
                                                ft.TextSpan(f"{cnt_gambler+1}등 ", ft.TextStyle(size=ca_size/5, color="#E3C04D",)),
                                                ft.TextSpan(f"{id} : ", ft.TextStyle(size=ca_size/5,)),
                                                ft.TextSpan(f"{score}", ft.TextStyle(size=ca_size/3, color="#374999",)),])]))
                                else:
                                    lv_gambler.controls.append(ft.Text(f"{cnt_gambler+1}등 {id} : {score}",
                                                                     size=int(ca_size/6)))
                                cnt_gambler += 1

                            elif act == "glory":
                                if cnt_glory < 5:
                                    lv_glory.controls.append(ft.Row(controls=[
                                        ft.Image(
                                            src = 'assets/img/crown.png',
                                            width=int(ca_size/3),
                                            height=int(ca_size/3),
                                            fit=ft.ImageFit.CONTAIN),
                                        # ft.Text(f"{cnt_criminal1+1}등 {id} : {score}",
                                        #         size=int(ca_size/4)),]))
                                        ft.Text(weight=ft.FontWeight.W_900, spans=[
                                                ft.TextSpan(f"{cnt_glory+1}등 ", ft.TextStyle(size=ca_size/5, color="#E3C04D",)),
                                                ft.TextSpan(f"{id} : ", ft.TextStyle(size=ca_size/5,)),
                                                ft.TextSpan(f"{score}", ft.TextStyle(size=ca_size/3, color="#374999",)),])]))
                                else:
                                    lv_glory.controls.append(ft.Text(f"{cnt_glory+1}등 {id} : {score}",
                                                                     size=int(ca_size/6)))

                                cnt_glory += 1

                            page.update()
                        else:
                            continue

                previous_time = current_time
                page.update()
            else:
                continue


ft.app(target=main)
