import keyboard as kb
import pyautogui as pgui
from pyscreeze import Box
import telegram_bot
import os
from PIL import Image

def scale_image(image_path, scale_factor_width, scale_factor_height):
    image = Image.open(image_path)
    # Масштабирование изображения
    print(image.size)
    new_size = (int(image.width *scale_factor_height**2), int(image.height * scale_factor_height**2))
    print(new_size)
    resized_image = image.resize(new_size)
    return resized_image

name_computer = input("Введите имя компьютера: ")
telegram_bot.name_computer = name_computer

start_text = """
Начало работы кликера (для остановки нажмите Esc)...
Если кликер работает не так как ожидается, проверьте и поменяйте скрины картинок в папке Letters.
В ней должны присутствовать Like.png, plus.png, Save.png, Next.png, Cross.png, Limit500.png (высвечивается при превышении лимита на 500 обьявлений в день)
Также для корректной работы следует закрепить в браузере главную вкладку с поиском.
"""
telegram_bot.send_massage_print(start_text)
original_size_width = 1920
original_size_height = 1080

persent = pgui.size()
if persent.height == 768:
    counts = 0
    while kb.is_pressed("Esc") == False:
        counts += 1
        try:
            if counts >= 10:
                telegram_bot.send_massage_print('Дальнейшие действия на странице не найдены')
                break
            button = None
            try: 
                button = pgui.locateOnScreen("Letters\\like1366.png", confidence=0.7)
            except pgui.ImageNotFoundException:
                print('Кнопка "like" не найдена')

            if button:
                counts = 0
                pgui.click(button)
                plus_start = None
                try:
                    plus_start = pgui.locateOnScreen("Letters\\plus1366.png", confidence=0.7, grayscale=True)
                except pgui.ImageNotFoundException:
                    print('Кнопка "plus" не найдена')

                #Не понял зачем этот код
                # pgui.sleep(1)
                # pgui.move(-190, -210, duration=1)
                # pgui.sleep(1)
                # pgui.click()

                save_button = None
                try: 
                    pgui.sleep(0.2)
                    save_button = pgui.locateOnScreen("Letters\\Save1366.png", confidence=0.8)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Save" не найдена')
                if save_button is None:
                    continue
                # поменял save_button.top - 150 => save_button.top - 120
                clickbox = Box(save_button.left, save_button.top - 120, save_button.width, save_button.height)
                pgui.moveTo(clickbox.left + 20, clickbox.top, duration=1)

                pgui.sleep(1)
                pgui.click()

                try: 
                    save_button = pgui.locateOnScreen("Letters\\Save1366.png", confidence=0.8)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Save" не найдена')

                pgui.moveTo(save_button.left + save_button.width / 2, save_button.top + save_button.height / 2, duration=1)
                pgui.sleep(1)
                pgui.click(save_button)

                limit = None
                try: 
                    limit = pgui.locateOnScreen("Letters\\Limit500_scaled.png", confidence=0.9)
                except pgui.ImageNotFoundException:
                    pass
                if limit != None:
                    telegram_bot.send_massage_print('Превышен лимит 500')
                    break

                # Из-за разного размера резюме необходимо смещение в цикле до тех пор пока не откроем резюме

                pgui.moveTo(button.left - 670, button.top - 130, duration=1)
                pgui.sleep(0.1)
                pgui.click()
                for i in range(30):
                    
                    pgui.moveTo(button.left -670, button.top - (130+(i+1)*10))
                    plus_new = pgui.locateOnScreen("Letters\\plus1366.png", confidence=0.7, grayscale=True)
                    if plus_start != plus_new:
                        break
                    pgui.sleep(0.05)
                    pgui.click()




                """
                Старая механика
                offset = None
                try: 
                    offset = pgui.locateOnScreen("../Letters\\Offset.png", confidence=0.9)
                except pgui.ImageNotFoundException:
                    print('Угол обьявления "Offset" не найден')
                if offset:
                    pgui.moveTo(offset.left + offset.width + 200, offset.top + offset.height / 2, duration=1)
                    pgui.sleep(1)
                    pgui.click()
                """


                pgui.sleep(3)
                print('Скролл')
                for i in range(10):
                    pgui.sleep(0.2)
                    pgui.scroll(-150)

                cross = None
                try: 
                    cross = pgui.locateOnScreen("Letters\\Cross1366.png", confidence=0.7, grayscale=True)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Cross" не найдена')

                if cross:
                    pgui.moveTo(cross.left+15, cross.top+15, duration=1)
                    pgui.sleep(1)
                    pgui.click()


                pgui.moveTo(120, 120)

                print('Скролл')
                pgui.scroll(-350)
                pgui.moveTo(132, 250)
                pgui.sleep(1)

            next_button = None
            try: 
                next_button = pgui.locateOnScreen("Letters\\Next1366.png", confidence=0.8)
            except pgui.ImageNotFoundException:
                print('Кнопка "Next" не найдена')

            if next_button:
                pgui.click(next_button)
                pgui.sleep(5)
            else:
                print('Скролл')
                pgui.scroll(-250)
                pgui.sleep(2)
        except Exception as e:
            telegram_bot.send_massage_print(f'Неизвестная ошибка\n{e}')
            break

    os.system("pause")
else:
    current_screen_width, current_screen_height = pgui.size()
    scale_factor_width = current_screen_width / original_size_width
    scale_factor_height = current_screen_height / original_size_height
    print(persent)
    counts = 0
    scaled_image = scale_image("Letters\\like.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\like_scaled.png")
    scaled_image = scale_image("Letters\\plus.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\plus_scaled.png")
    scaled_image = scale_image("Letters\\Save2.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\Save_scaled.png")
    scaled_image = scale_image("Letters\\Next.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\Next_scaled.png")
    scaled_image = scale_image("Letters\\Cross2.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\Cross2_scaled.png")
    scaled_image = scale_image("Letters\\Limit500.png", scale_factor_width, scale_factor_height)
    scaled_image.save("Letters\\Limit500_scaled.png")

    while kb.is_pressed("Esc") == False:
        counts += 1
        try:
            if counts >= 10:
                telegram_bot.send_massage_print('Дальнейшие действия на странице не найдены')
                break
            button = None
            try: 
                button = pgui.locateOnScreen("Letters\\like_scaled.png", confidence=0.7)
            except pgui.ImageNotFoundException:
                print('Кнопка "like" не найдена')

            if button:
                counts = 0
                pgui.click(button)
                plus_start = None
                try:
                    plus_start = pgui.locateOnScreen("Letters\\plus_scaled.png", confidence=0.7, grayscale=True)
                except pgui.ImageNotFoundException:
                    print('Кнопка "plus" не найдена')

                #Не понял зачем этот код
                # pgui.sleep(1)
                # pgui.move(-190, -210, duration=1)
                # pgui.sleep(1)
                # pgui.click()

                save_button = None
                try: 
                    pgui.sleep(0.2)
                    save_button = pgui.locateOnScreen("Letters\\Save_scaled.png", confidence=0.8)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Save" не найдена')
                if save_button is None:
                    continue
                # поменял save_button.top - 150 => save_button.top - 120
                clickbox = Box(save_button.left, save_button.top - 120, save_button.width, save_button.height)
                pgui.moveTo(clickbox.left + 20, clickbox.top, duration=1)

                pgui.sleep(1)
                pgui.click()

                try: 
                    save_button = pgui.locateOnScreen("Letters\\Save_scaled.png", confidence=0.8)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Save" не найдена')

                pgui.moveTo(save_button.left + save_button.width / 2, save_button.top + save_button.height / 2, duration=1)
                pgui.sleep(1)
                pgui.click(save_button)

                limit = None
                try: 
                    limit = pgui.locateOnScreen("Letters\\Limit500_scaled.png", confidence=0.9)
                except pgui.ImageNotFoundException:
                    pass
                if limit != None:
                    telegram_bot.send_massage_print('Превышен лимит 500')
                    break

                # Из-за разного размера резюме необходимо смещение в цикле до тех пор пока не откроем резюме

                pgui.moveTo(button.left - 670*scale_factor_height**2, button.top - 130, duration=1)
                pgui.sleep(0.1)
                pgui.click()
                for i in range(30):
                    
                    pgui.moveTo(button.left -670*scale_factor_height**2, button.top - (130+(i+1)*10))
                    plus_new = pgui.locateOnScreen("Letters\\plus_scaled.png", confidence=0.7, grayscale=True)
                    if plus_start != plus_new:
                        break
                    pgui.sleep(0.01)
                    pgui.click()




                """
                Старая механика
                offset = None
                try: 
                    offset = pgui.locateOnScreen("../Letters\\Offset.png", confidence=0.9)
                except pgui.ImageNotFoundException:
                    print('Угол обьявления "Offset" не найден')
                if offset:
                    pgui.moveTo(offset.left + offset.width + 200, offset.top + offset.height / 2, duration=1)
                    pgui.sleep(1)
                    pgui.click()
                """


                pgui.sleep(3)
                print('Скролл')
                for i in range(10):
                    pgui.sleep(0.2)
                    pgui.scroll(-150)

                cross = None
                try: 
                    cross = pgui.locateOnScreen("Letters\\Cross2_scaled.png", confidence=0.7, grayscale=True)
                except pgui.ImageNotFoundException:
                    print('Кнопка "Cross" не найдена')

                if cross:
                    pgui.moveTo(cross.left+15, cross.top+15, duration=1)
                    pgui.sleep(1)
                    pgui.click()


                pgui.moveTo(120, 120)

                print('Скролл1')
                pgui.scroll(-350)
                pgui.moveTo(132, 250)
                pgui.sleep(1)

            next_button = None
            try: 
                next_button = pgui.locateOnScreen("Letters\\Next_scaled.png", confidence=0.8)
            except pgui.ImageNotFoundException:
                print('Кнопка "Next" не найдена')

            if next_button:
                pgui.click(next_button)
                pgui.sleep(5)
            else:
                print('Скролл2')
                pgui.scroll(-250)
                pgui.sleep(2)
        except Exception as e:
            telegram_bot.send_massage_print(f'Неизвестная ошибка\n{e}')
            break

    os.system("pause")