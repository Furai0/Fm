import pyscreeze
import os
os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")
import mss
import cv2
import numpy as np
import autopy
import time
import pyperclip
import clipboard


def is_template_in_image(img_path, template_path, threshold=0.8):
    img_rgb = cv2.imread(img_path)
    template = cv2.imread(template_path)
    if img_rgb is None:
        print(f"Ошибка: не удалось загрузить изображение {img_path}")
        return False
    if template is None:
        print(f"Ошибка: не удалось загрузить шаблон {template_path}")
        return False
    h, w = template.shape[:-1]
    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        return True
    else:
        return False


#path to fm
path_to_fm = os.getcwd()

#screens
p_mainscreen_checkin = f'{path_to_fm}/mainscreen_checkin.png'
p_mainscreen_status_slychainesozdan = f'{path_to_fm}/mainscreen_status_slychainesozdan.png'
p_feldsher_checkin = f'{path_to_fm}/feldsher_checkin.png'
p_feldsher_birthdate_checkin = f'{path_to_fm}/feldsher_birthdate_checkin.png'


#main gigacycle
while True:

#making screen
    with mss.mss() as sct:
        screenshot = sct.shot(output=f'{path_to_fm}/screenshot.png')

#repeat for returning window
    autopy.mouse.move(60, 15)
    autopy.mouse.click (autopy.mouse.Button.LEFT, 0.2)
    time.sleep(5)

    #MAINWINDOW block
    if is_template_in_image(screenshot, p_mainscreen_checkin):

        #next if repearing status
        if is_template_in_image(screenshot, p_mainscreen_status_slychainesozdan)==False:
            print(is_template_in_image(screenshot, p_mainscreen_status_slychainesozdan))
            autopy.mouse.move(580, 370)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(560, 435)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
        #go to feldsher window
        else:
            autopy.mouse.smooth_move(600, 60)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(260, 460)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(1300, 420)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(800, 420)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(1000, 600)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
    #FELDSHER_WINDOW block

    if is_template_in_image(screenshot, p_feldsher_checkin):

        #birthdate checking - if empty - skipping protol
        print(f' birthdate {is_template_in_image(screenshot, p_feldsher_birthdate_checkin)}')
        if is_template_in_image(screenshot, p_feldsher_birthdate_checkin)==True:

            #exit block - repeats othen
            autopy.mouse.smooth_move(150, 1000)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)
            print(is_template_in_image(screenshot, p_feldsher_birthdate_checkin), 'нет даты рождения')

        else:
        #выяснение диагноза
            #выделение вызова
            autopy.mouse.smooth_move(350, 740)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
            autopy.mouse.smooth_move(1800, 740)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

            #vizov ctrl+c,
            autopy.mouse.smooth_move(350, 740)
            autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(400, 800)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)

            povod_vizova = clipboard.paste()

            #move to diagnoz
            autopy.mouse.smooth_move(1900, 300)
            time.sleep(1)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
            autopy.mouse.smooth_move(1900, 530)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

            #выделение диагноза
            autopy.mouse.smooth_move(350, 830)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
            autopy.mouse.smooth_move(1800, 830)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

            #vizov ctrl+c,
            autopy.mouse.smooth_move(380, 830)
            autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
            time.sleep(1)
            autopy.mouse.smooth_move(440, 880)
            autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
            time.sleep(1)

            diagnoz = f' {clipboard.paste()}'

            # back to main feldsher menu
            autopy.mouse.smooth_move(1900, 530)
            time.sleep(1)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
            autopy.mouse.smooth_move(1900, 300)
            autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

            diagnoz_povod_vizova = povod_vizova+diagnoz
            print(diagnoz_povod_vizova)

#словарь:
#povod_diagnoz - скопированное из повод вызова и диагноз для поиска совпадений
#type_povod - выбор на первом экране между несчастным случаем, острой и хронической
#оставшиеся - жалоба и анамнез

            templates_vizovi = [
        {
        'povod_diagnoz': ' J 0 6 ОРВИ неуточненная 12К температура кашель',
        'type_povod': 'ostroe',
        'opisanie_zaloba': ['высокая температура тела, озноб, гиперемия зева'],
        'anamnez': ['Заболевание внезапно, таблетки не принимаются']
        },
        {
        'povod_diagnoz': 'g G ',
        'type_povod': 'obostrenie',
        'opisanie_zaloba': ['головокружение, шум в ушах'],
        'anamnez': ['на учете состоит у врача терапевта, к врачу не обращалась, лекарства не принимала']

        },
        {
        'povod_diagnoz': 'ОСТЕОХАНДРОЗ',
        'type_povod': 'obostrenie',
        'opisanie_zaloba': ['жалобы на боль в поясничной области, тяжесть в поясничном отделе'],
        'anamnez': ['заболело внезапно после физической нагрузки. к терапевту не обащалась']

        },
        {
        'povod_diagnoz': 'АСТМА',
        'type_povod': 'obostrenie',
        'opisanie_zaloba': ['приступы удушья, затрудненное дыхание, одышка'],
        'anamnez': ['болеет в течении нескольких лет. на учете у терапевта состоит']
        },
        {
        'povod_diagnoz': '    02Б ушиб, перелом конечностей',
        'type_povod': 'neschastniy',
        'opisanie_zaloba': ['жалобы на боли в поврежденной области, которые возрастают при попытке движений, ограниченность движений, некоторая визуальную деформацию со стороны костной системы.'],
        'anamnez': ['Падение с последующим ударом']
        },
        {
        'povod_diagnoz': '    M42.9 остеохондроз позвоночника неуточненный M42.9 остеохондроз позвоночника неуточненный',
        'type_povod': 'obostrenie',
        'opisanie_zaloba': ['жалобы на боль в поясничной области, тяжесть в поясничном отделе'],
        'anamnez': ['заболело внезапно после физической нагрузки. к терапевту не обратились']
        },
]

#ДАЛЕЕ НЕЙРОКУСОК

                        # Функция для поиска наиболее подходящего диагноза
            def find_diagnosis(input_text):
                best_match = None
                max_matches = 0

                # Перебираем все вызовы в списке
                for vizov in templates_vizovi:
                    # Получаем значение povod_diagnoz
                    diagnoz = vizov['povod_diagnoz']

                    # Считаем количество совпадений слов
                    matches = sum(word in diagnoz.lower() for word in input_text.lower().split())

                    # Если найдено больше совпадений, чем у текущего лучшего диагноза
                    if matches > max_matches:
                        max_matches = matches
                        best_match = vizov

                return best_match


            # Ввод текста для поиска
            input_text = diagnoz_povod_vizova

            # Поиск диагноза
            matched_vizov = find_diagnosis(input_text)

            # Если диагноз ne найден

                        #КОНЕЦ НЕЙРОКУСКА
        #КОНЕЦ НЕЙРОКУСКА
        #КОНЕЦ НЕЙРОКУСКА



            if matched_vizov:
                # Присваиваем данные в переменные
                povod_diagnoz = matched_vizov['povod_diagnoz']
                type_povod = matched_vizov['type_povod']
                opisanie_zaloba = matched_vizov['opisanie_zaloba']
                anamnez = matched_vizov['anamnez']
                ###переопределяем переменные потому что все кривое и только так работает

                a_opisanie_zaloba = ''.join(opisanie_zaloba)
                a_anamnez = ''.join(anamnez)

                # Выводим результат
                print(f"Диагноз: {povod_diagnoz}")
                print(f"Тип повода: {type_povod}")
                print(f"Описание жалоб: {', '.join(opisanie_zaloba)}")
                print(f"Анамнез: {', '.join(anamnez)}")



                #Выбираем повод вызова на основе выбора словаря
                if type_povod=='ostroe':
                    autopy.mouse.smooth_move(540, 800)
                    time.sleep(2)
                    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                    time.sleep(1)
                if type_povod=='obostrenie':
                    autopy.mouse.smooth_move(850, 800)
                    time.sleep(2)
                    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                    time.sleep(1)
                if type_povod=='neschastniy':
                    autopy.mouse.smooth_move(320, 800)
                    time.sleep(2)
                    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                    time.sleep(1)

                #переход в жалобы и анамнез
                autopy.mouse.smooth_move(150, 300)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)

                #переход в жалобы и печать выбранной из словаря

                print(a_opisanie_zaloba)
                clipboard.copy(a_opisanie_zaloba)


                autopy.mouse.smooth_move(400, 280)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)

                autopy.mouse.smooth_move(400, 280)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
                time.sleep(1)

                autopy.mouse.smooth_move(430, 360)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)


                #переход в anamnez и печать выбранной из словаря

                print(a_anamnez)
                clipboard.copy(a_anamnez)



                autopy.mouse.smooth_move(400, 430)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)

                autopy.mouse.smooth_move(400, 430)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
                time.sleep(1)

                autopy.mouse.smooth_move(450, 515)
                time.sleep(1)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)

                #переход в результат
                autopy.mouse.smooth_move(150, 615)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)
                #выбираем улучшение
                autopy.mouse.smooth_move(325, 420)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)

                #блок проклика подписания
#блок проклика подписания
                #блок проклика подписания

                #переход в подписание
                autopy.mouse.smooth_move(145, 715)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(10)
                #pdf110 создать
                autopy.mouse.smooth_move(450, 285)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(10)
                #подписать документ
                autopy.mouse.smooth_move(600, 285)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(10)

                #сэмд создать
                autopy.mouse.smooth_move(450, 400)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(20)

                autopy.mouse.smooth_move(600, 400)
                time.sleep(2)
                autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
                time.sleep(10)

                #проверка успешной подписи


#выход после успеха

            else:
                print("Диагноз не найден.")

                # Записываем неизвестный диагноз в файл
                with open("unknown_diagnozes.txt", "a", encoding="utf-8") as file:
                    file.write(f"{input_text}\n")
                print(f"Диагноз '{input_text}' добавлен в файл unknown_diagnozes.txt.")

                #repeat for returning window
                autopy.mouse.move(60, 15)
                autopy.mouse.click (autopy.mouse.Button.LEFT, 0.2)
                time.sleep(1)


    else:
        print('ERROR')
    break



















