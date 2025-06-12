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




#path to fm
path_to_fm = os.getcwd()

# variables

    #screens
screenshot = f'{path_to_fm}/screenshot.png'
p_mainscreen_checkin = f'{path_to_fm}/mainscreen_checkin.png'
p_mainscreen_status_slychainesozdan = f'{path_to_fm}/mainscreen_status_slychainesozdan.png'
p_feldsher_checkin = f'{path_to_fm}/feldsher_checkin.png'
p_feldhser_birthdate_checkin = f'{path_to_fm}/feldhser_birthdate_checkin.png'

p_feldsher_polis_checkin = f'{path_to_fm}/feldsher_polis_checkin.png'
p_feldsher_smo_checkin = f'{path_to_fm}/feldsher_smo_checkin.png'
p_feldsher_snils_checkin = f'{path_to_fm}/feldsher_snils_checkin.png'
p_feldhser_birthdate_checkin = f'{path_to_fm}/feldhser_birthdate_checkin.png'

p_feldsher_success_pdf = f'{path_to_fm}/feldsher_success_pdf.png'
p_feldsher_success_semd = f'{path_to_fm}/feldsher_success_semd.png'



# functions useable variables
protocol_success = 0
protocol_success_all = 0
protocol_paid = 1050
diagnoz_povod_vizova = ""
protocol_skipped = 0
protocol_skipped_all = 0
input_text = diagnoz_povod_vizova

# Поиск диагноза

input_text = diagnoz_povod_vizova
matched_vizov = None


# поиск шаблона в картинке
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
#main_window_border_click
def main_window_border_click():
    time.sleep(1)
    autopy.mouse.move(60, 15)
    autopy.mouse.click (autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)
    print('Кликнули по границе окна чтобы перевести его на передний план')


    #switch_status_to_slychainesozdan if it need
def switch_status_to_slychainesozdan():
    if is_template_in_image(screenshot, p_mainscreen_status_slychainesozdan)==False:
        time.sleep(1)
        print('Сменяем статус на "случай не создан"')
        autopy.mouse.move(580, 370)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        time.sleep(1)
        autopy.mouse.smooth_move(560, 435)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        time.sleep(1)

    else:
        print('Статус "случай не создан"')

#go to feldsher window
def go_to_feldsher_window():
    print('Переходим к рабочему окну фельдшера')
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


#making screen
def make_screen():
    print('Делаем скриншот главного экрана. Проверьте что на экране нет ничего лишнего!')
    with mss.mss() as sct:
        screenshot = sct.shot(output=f'{path_to_fm}/screenshot.png')
        time.sleep(2)


    #exit feldhser window
def exit_feldsher_window():
    print('Выходим из рабочего окна фельдшера')
    autopy.mouse.smooth_move(150, 1000)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)


#выяснение диагноза
def check_diagnoz():
    global diagnoz_povod_vizova
    print('Выясняем диагноз и повод вызова')
    #выделение вызова
    print('Выделяем повод вызова')
    autopy.mouse.smooth_move(350, 740)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    autopy.mouse.smooth_move(1800, 740)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    #vizov ctrl+c,
    print('Копируем повод вызова')
    autopy.mouse.smooth_move(350, 740)
    autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
    time.sleep(1)
    autopy.mouse.smooth_move(400, 800)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)
    print('Сохранение повода вызова')
    povod_vizova = clipboard.paste()
    #move to diagnoz
    print('Выясняем диагноз')
    autopy.mouse.smooth_move(1900, 300)
    time.sleep(1)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    autopy.mouse.smooth_move(1900, 530)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    print('Выделяем диагноз')
    #выделение диагноза
    autopy.mouse.smooth_move(350, 830)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    autopy.mouse.smooth_move(1800, 830)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    print('Копируем диагноз')
    #vizov ctrl+c,
    autopy.mouse.smooth_move(380, 830)
    autopy.mouse.click(autopy.mouse.Button.RIGHT, 0.2)
    time.sleep(1)
    autopy.mouse.smooth_move(440, 880)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)
    print('Сохраняем диагноз')
    diagnoz = f' {clipboard.paste()}'
    print('Возвращаемся')
    # back to main feldsher menu
    autopy.mouse.smooth_move(1900, 530)
    time.sleep(1)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
    autopy.mouse.smooth_move(1900, 300)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    # повод вызова и диагноз одной строчкой

    diagnoz_povod_vizova = povod_vizova+diagnoz
    print(f' Повод вызова и диагноз обозначены как: {diagnoz_povod_vizova}')
    return diagnoz_povod_vizova
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

# записывает не найденный диагноз и выходит из протокола
def diagnoz_not_found():
    global protocol_skipped
    protocol_skipped += 1
    print("Диагноз не найден.")

    # Записываем  диагноз в файл
    with open("unknown_diagnozes.txt", "a", encoding="utf-8") as file:
        file.write(f"{diagnoz_povod_vizova}\n")
    print(f"Диагноз '{diagnoz_povod_vizova}' добавлен в файл unknown_diagnozes.txt.")


    exit_feldsher_window()

    #Выбираем повод вызова на основе выбора словаря
def choose_povod_vizova():
    if type_povod=='ostroe':
        print('Выбран повод "Острое внезапное заболевание"')
        autopy.mouse.smooth_move(540, 800)
        time.sleep(2)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        time.sleep(1)
    if type_povod=='obostrenie':
        print('Выбран повод "Обострение хронического заболевания"')
        autopy.mouse.smooth_move(850, 800)
        time.sleep(2)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        time.sleep(1)
    if type_povod=='neschastniy':
        print('Выбран повод "Несчастный случай"')
        autopy.mouse.smooth_move(320, 800)
        time.sleep(2)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        time.sleep(1)


def proclick_feldsher():

    #переход в жалобы и анамнез
    print('Переход в жалобы и анамнез')
    autopy.mouse.smooth_move(150, 300)
    time.sleep(1)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)

    #переход в жалобы и печать выбранной из словаря
    print('Переход в жалобы и анамнез и печать выбранной жалобы')
    print(f' Выбранная жалоба {a_opisanie_zaloba}')

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
    print('Переход в анамнез и печать выбранного анамнеза')
    print(f' Выбранный анамнез {a_anamnez}')

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
    print('Переход в результат')
    autopy.mouse.smooth_move(150, 615)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)
    #выбираем улучшение
    print('Выбираем улучшение')
    autopy.mouse.smooth_move(325, 420)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)

    #блок проклика подписания
#блок проклика подписания
    #блок проклика подписания

    #переход в подписание
    print('Переходим к подписи')

    autopy.mouse.smooth_move(145, 715)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(10)
    #pdf110 создать
    print('Ожидается создание PDF')
    autopy.mouse.smooth_move(450, 285)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(10)
    #подписать документ
    print('Ожидается подпись PDF')
    autopy.mouse.smooth_move(600, 285)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(10)

    #сэмд создать
    print('Ожидается создание СЭМД')
    autopy.mouse.smooth_move(450, 400)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(20)
    print('Ожидается подпись СЭМД')
    autopy.mouse.smooth_move(600, 400)
    time.sleep(2)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(10)


#     Проверка успешности подписания
def success_check():
    print('Проверка подписей')
    make_screen()
    if is_template_in_image(screenshot, p_feldsher_success_pdf) and is_template_in_image(screenshot, p_feldsher_success_semd):
        global protocol_paid
        global protocol_success
        protocol_success += 1
        protocol_paid -= 1
        time.sleep(1)
        print('Протокол успешно подписан!')
        time.sleep(1)
        print(f' Введенный ключ позволяет внести еще {protocol_paid}')
        time.sleep(1)
        print(f' Успешно внессенных протоколов за сеанс {protocol_success}')
        time.sleep(5)
        print(f' Осталось протоколов {protocol_paid}')
        time.sleep(5)
        print('Переходим к следующему протоколу')


        exit_feldsher_window()

    else:
        if is_template_in_image(screenshot, p_feldsher_smo_checkin):
            time.sleep(1)
            print("У пациента отсутсвует страховая медицинская организация")
            time.sleep(1)
            print("Также могут отсутсвовать другие данные")
            time.sleep(1)
            print("Протокол не будет засчитан")
            time.sleep(1)
            print("Если вы захотите внести недостающие данные пациента")
            time.sleep(1)
            print('Его протокол будет помещен в категорию "Только PDF" ')
            time.sleep(1)
            print("Переходим к следующему протоколу")
            time.sleep(1)


        if is_template_in_image(screenshot, p_feldsher_polis_checkin):
            time.sleep(1)
            print("У пациента отсутсвует ПОЛИС")
            time.sleep(1)
            print("Также могут отсутсвовать другие данные")
            time.sleep(1)
            print("Протокол не будет засчитан")
            time.sleep(1)
            print("Если вы захотите внести недостающие данные пациента")
            time.sleep(1)
            print('Его протокол будет помещен в категорию "Только PDF" ')
            time.sleep(1)
            print("Переходим к следующему протоколу")
            time.sleep(1)


        if is_template_in_image(screenshot, p_feldsher_snils_checkin):
            time.sleep(1)
            print("У пациента отсутсвует СНИЛС")
            time.sleep(1)
            print("Также могут отсутсвовать другие данные")
            time.sleep(1)
            print("Протокол не будет засчитан")
            time.sleep(1)
            print("Если вы захотите внести недостающие данные пациента")
            time.sleep(1)
            print('Его протокол будет помещен в категорию "Только PDF" ')
            time.sleep(1)
            print("Переходим к следующему протоколу")
            time.sleep(1)
            # жмем крестик на документ не заполнен
        if is_template_in_image(screenshot, p_feldsher_birthdate_checkin):
            time.sleep(1)
            print("У пациента отсутсвует дата рождения")
            time.sleep(1)
            print("Также могут отсутсвовать другие данные")
            time.sleep(1)
            print("Протокол не будет засчитан")
            time.sleep(1)
            print("Если вы захотите внести недостающие данные пациента")
            time.sleep(1)
            print('Его протокол будет помещен в категорию "Только PDF" ')
            time.sleep(1)
            print("Переходим к следующему протоколу")
            time.sleep(1)
            # жмем крестик на документ не заполнен
        global protocol_skipped
        protocol_skipped += 1
        print(f' Протоколов пропущено за сеанс {protocol_skipped}')
        print(f' Протоколов пропущено за все время {protocol_skipped_all}')
        time.sleep(1)
        autopy.mouse.smooth_move(1537, 271)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)

        exit_feldsher_window()






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




#main gigacycle
while True:

    time.sleep(2)
    make_screen()
    main_window_border_click()
    time.sleep(2)
    #MAINWINDOW block
    if is_template_in_image(screenshot, p_mainscreen_checkin):
        main_window_border_click()
# ДОБАВИТЬ НАЖИТИЕ ОБНОВИТЬ
        switch_status_to_slychainesozdan()
# ДОБАВИТЬ НАЖИТИЕ ОБНОВИТЬ
        go_to_feldsher_window()


    #FELDSHER_WINDOW block
    #определяем переменную чтобы код дальше не падал

    if is_template_in_image(screenshot, p_feldsher_checkin):

        main_window_border_click()
        autopy.mouse.smooth_move(1600, 400)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
        check_diagnoz()
        matched_vizov = find_diagnosis(diagnoz_povod_vizova)

        if matched_vizov:

            # Присваиваем данные в переменные
            povod_diagnoz = matched_vizov['povod_diagnoz']
            type_povod = matched_vizov['type_povod']
            opisanie_zaloba = matched_vizov['opisanie_zaloba']
            anamnez = matched_vizov['anamnez']

            #переопределяем переменные потому что все кривое и только так работает
            a_opisanie_zaloba = ''.join(opisanie_zaloba)
            a_anamnez = ''.join(anamnez)

            # Выводим результат
            print(f"Диагноз: {povod_diagnoz}")
            print(f"Тип повода: {type_povod}")
            print(f"Описание жалоб: {', '.join(opisanie_zaloba)}")
            print(f"Анамнез: {', '.join(anamnez)}")

            with open("unknown_diagnozes.txt", "a", encoding="utf-8") as file:
                file.write(f"{diagnoz_povod_vizova}\n")
            print(f"Диагноз '{diagnoz_povod_vizova}' добавлен в файл unknown_diagnozes.txt.")

            choose_povod_vizova()

            proclick_feldsher()

            success_check()

        else:
            diagnoz_not_found()


    else:
        print('ERR12OR')




















