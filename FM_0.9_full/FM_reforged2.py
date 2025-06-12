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
import random
import pickle


#path to fm
path_to_fm = os.getcwd()

# variables

    #screens
screenshot = f'{path_to_fm}/screenshot.png'
# where is i
p_mainscreen_checkin = f'{path_to_fm}/mainscreen_checkin.png'
p_feldsher_checkin = f'{path_to_fm}/feldsher_checkin.png'
# mainscreen clicks
p_mainscreen_status_slychainesozdan = f'{path_to_fm}/mainscreen_status_slychainesozdan.png'
p_mainscreen_alldone = f'{path_to_fm}/mainscreen_alldone.png'
# feldsher finish
p_document_ne_zapolnen = f'{path_to_fm}/document_ne_zapolnen.png'
p_feldsher_polis_checkin = f'{path_to_fm}/feldsher_polis_checkin.png'
p_feldsher_smo_checkin = f'{path_to_fm}/feldsher_smo_checkin.png'
p_feldsher_snils_checkin = f'{path_to_fm}/feldsher_snils_checkin.png'
p_feldhser_birthdate_checkin = f'{path_to_fm}/feldhser_birthdate_checkin.png'
# feldsher finish
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


# шифровка расшифровка жысонов, дата - рабочий жысон
data = {}
def data_load():
    with open('data.pickle', 'rb') as bin_file:
        global data
        data = pickle.load(bin_file)

def data_dump():
    with open('data.pickle', 'wb') as bin_file:
        global data
        pickle.dump(data, bin_file)

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
    time.sleep(2)
    autopy.mouse.smooth_move(600, 60)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(2)
    autopy.mouse.smooth_move(260, 460)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(2)
    autopy.mouse.smooth_move(1300, 420)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(2)
    autopy.mouse.smooth_move(800, 420)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(2)
    autopy.mouse.smooth_move(1000, 600)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(2)


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

        data_load()
        data['success'] += 1
        data['paid'] -= 1
        data_dump()
        time.sleep(1)
        print('Протокол успешно подписан!')
        time.sleep(1)
        print(f"Введенный ключ позволяет внести еще {data['paid']}")
        time.sleep(1)
        print(f" Успешно внессенных протоколов - {data['success']}")
        time.sleep(3)
        print('Переходим к следующему протоколу')


        exit_feldsher_window()

    if is_template_in_image(screenshot, p_document_ne_zapolnen):

        if is_template_in_image(screenshot, p_feldsher_smo_checkin):
            time.sleep(1)
            print("У пациента отсутсвует страховая медицинская организация")

        if is_template_in_image(screenshot, p_feldsher_polis_checkin):
            time.sleep(1)
            print("У пациента отсутсвует ПОЛИС")

        if is_template_in_image(screenshot, p_feldsher_snils_checkin):
            time.sleep(1)
            print("У пациента отсутсвует СНИЛС")

            # жмем крестик на документ не заполнен
        if is_template_in_image(screenshot, p_feldhser_birthdate_checkin):
            time.sleep(1)
            print("У пациента отсутсвует дата рождения")
        else:
            print("Протокол не засчитан по неизвестной причине. Возможно, движения мыши пользователя помешали программе корректно нажать клавиши. Для надежной работы откройте окно с АРМ Бригады полностью, а также переверните мышь вверх ногами, чтобы избежать случайных движений")

        data_load()
        data['skipped'] += 1
        data_dump()
        time.sleep(1)
        print("Протокол не будет засчитан")
        time.sleep(1)
        print("Если вы захотите внести недостающие данные пациента")
        time.sleep(1)
        print('Его протокол будет помещен в категорию "Только PDF" ')
        time.sleep(1)
        print("Переходим к следующему протоколу")
        time.sleep(1)
        autopy.mouse.smooth_move(1537, 271)
        autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)

        exit_feldsher_window()


def click_obnovit():
    time.sleep(1)
    autopy.mouse.smooth_move(600, 60)
    autopy.mouse.click(autopy.mouse.Button.LEFT, 0.2)
    time.sleep(1)


#словарь:
#povod_diagnoz - скопированное из повод вызова и диагноз для поиска совпадений
#type_povod - выбор на первом экране между несчастным случаем, острой и хронической
#оставшиеся - жалоба и анамнез

templates_vizovi = [
        {
        "povod_diagnoz": " J06 ОРВИ неуточненная 12К температура кашель 12Я температура без осложнений J06.9 ОРВИ неуточненная 11Я головная боль",
        "type_povod": "ostroe",

        "opisanie_zaloba":    ["Высокая температура тела, озноб, гиперемия зева" ,    "Пациент жалуется на повышение температуры тела до 38,5°C, общую слабость, головную боль, заложенность носа, обильные слизистые выделения из носа, першение в горле и сухой кашель. Также отмечает ломоту в мышцах и суставах." ,    "Пациентка предъявляет жалобы на повышение температуры тела до 38,8°C, насморк с прозрачными выделениями, боль в горле при глотании, сухой кашель и общую слабость. Также отмечает снижение аппетита и головную боль." ,    "Пациент жалуется на заложенность носа, чихание, боль в горле, сухой кашель и повышение температуры тела до 38,5°C. Также отмечает общую слабость, потливость и ломоту в теле." ,    "Пациентка жалуется на повышение температуры тела до 39,0°C, сильную головную боль, заложенность носа, боль в горле и сухой кашель. Также отмечает общую слабость, снижение аппетита и ломоту в мышцах." ],

        "anamnez":    ["Заболевание внезапно, таблетки не принимаются" ,    "Температура появилась в первый день заболевания, сопровождалась ознобом. Самостоятельно принимал жаропонижающие препараты (парацетамол), но улучшения не отмечает." ,    "Температура поднялась на второй день заболевания. Самостоятельно принимала противовирусные препараты, но улучшения не наблюдается. Контактировал с людьми, которые болели ОРВИ" ,    "Заболел остро день назад. Температура появилась в первый день заболевания. Самостоятельно принимались жаропонижающие препараты, но состояние не улучшилось." ,    "Симптомы появились два дня назад после контакта с больным ОРВИ. Температура поднялась в первый день заболевания. Самостоятельно принимались жаропонижающие препараты, но улучшения не наблюдается." ],
        },
        {
        "povod_diagnoz": "I10 эссенциальная (первичная) гипертензия  04К боль в груди (кардио больной) 04Д повышенное АД I10 эссенциальная (первичная) гипертензия 11Я головная боль G96.9 поражение ЦНС неуточненное  головная боль G93.4 энцефалопатия неуточненная G90.9 расстр.вегетат-ной (автоном) НС неуточ G93.4 энцефалопатия неуточненная I67.9 цереброваскулярная болезнь неуточненн. 04Г повышенное АД у больного с ГБ I10 эссенциальная (первичная) гипертензия 04К боль в груди (кардио больной) G90.9 расстр.вегетат-ной (автоном) НС неуточ 04А аритмия I25.9 хроническая ИБС неуточненная",
        "type_povod": "obostrenie",

        "opisanie_zaloba":    ["Головокружение, шум в ушах, пульсирующими головными болями, тошнотой и мельканием мушек перед глазами, учащенное сердцебиение." ,    " головные боли давящего характера в лобной и височной областях, мелькание мушек перед глазами" ,    "Пациент жалуется на чувство тяжести в груди, периодические боли в области сердца давящего характера" ,    "Пациент жалуется на головокружение, слабость, снижение работоспособности, а также на периодическое онемение пальцев рук и ног. Отмечает ухудшение зрения" ,    "Пациент жалуется на сильные головные боли, тошноту, слабость и снижение концентрации внимания."] ,

       "anamnez":   [ "На учете состоит у врача терапевта, к врачу не обращалась. Регулярно принимает антигипертензивные препараты, но периодически отмечает повышение АД до 160/100 мм рт. ст., особенно при нарушении режима приема лекарств. Отмечает эпизоды учащенного сердцебиения, особенно в стрессовых ситуациях." ,    "Гипертензия выявлена 3 года назад во время профилактического осмотра. Регулярного лечения не получала, за медицинской помощью обращалась редко." ,    "Неоднократно госпитализировался с гипертоническими кризами. Регулярно принимает антигипертензивные препараты, но последний месяц отмечает ухудшение контроля АД. Ведет малоподвижный образ жизни." ,    "Лечение получает нерегулярно, часто пропускает прием препаратов. "],

        },
        {
        "povod_diagnoz": "09Я болит бок, поясница M42.9 остеохондроз позвоночника неуточненный 11Я головная боль M42.9 остеохондроз позвоночника неуточненный  09Я болит бок, поясница M06.9 ревматоидный артрит неуточненный ",
        "type_povod": "obostrenie",

        "opisanie_zaloba":    ["Жалобы на боль в поясничной области, тяжесть в поясничном отделе" ,    "Жалобы на боли в поясничном отделе позвоночника, которые усиливаются при наклонах, подъеме тяжестей и длительном стоянии. Также отмечает иррадиацию боли в правую ногу, чувство онемения в области бедра" ,    "Пациент жалуется на боли в грудном отделе позвоночника, которые усиливаются при глубоком вдохе или поворотах туловища. Также отмечает чувство скованности в спине по утрам и быструю утомляемость." ,    "Пациент жалуется на сильные боли в поясничном отделе позвоночника, которые иррадиируют в левую ногу. Отмечает затруднения при ходьбе, особенно при подъеме по лестнице, и чувство онемения в области стопы." ] ,

        "anamnez":   [ "Заболело внезапно после физической нагрузки. К терапевту не обащалась, таблетки не принимались" ,    "Заболело внезапно после физической нагрузки.  Регулярно принимает нестероидные противовоспалительные препараты, но последний месяц отмечает усиление болей" ,    "Диагностирован остеохондроз грудного отдела позвоночника . Периодически проходит лечение у невролога, но последний месяц отмечает ухудшение состояния" ,     "Периодически проходит лечение у невролога, но последний месяц отмечает ухудшение состояния" ,    "Периодически проходит лечение у невролога. Регулярно проходит курсы массажа и физиотерапии, но последний месяц отмечает усиление болей"] ,

        },
        {
        "povod_diagnoz": "05А задыхается (бронхиальная астма) J45.9 астма неуточненная",
        "type_povod": "obostrenie",

       "opisanie_zaloba":   [ "Пациент жалуется на периодические приступы удушья, сопровождающиеся свистящими хрипами в грудной клетке" ,    "Приступ затрудненного дыхания" ,    "Пациент жалуется на эпизоды свистящего дыхания, чувство нехватки воздуха и приступы удушья" ] ,

        "anamnez":    ["Болеет в течении нескольких лет. на учете у терапевта состоит" ,    "Регулярно принимает базисную терапию, но последний месяц отмечает ухудшение контроля над симптомами." ,    "Регулярно использует ингаляционные препараты, но последний месяц отмечает учащение приступов. Аллергия на пыль и шерсть животных," ,     "Регулярно использует ингаляционные препараты" ,    "Регулярно использует ингаляционные, аллергический ринит с детства"] ,
        },
        {
        "povod_diagnoz": "    02Б ушиб, перелом конечностей S79.8 др уточ травмы области тазобедр сустав 02Я старая травма, ухудшение S70.9 поверх.травма таза, бедра неуточненная  S06.0 сотрясение головного мозга",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["жалобы на боли в поврежденной области, которые возрастают при попытке движений, ограниченность движений, некоторая визуальную деформацию со стороны костной системы."] ,
        "anamnez":    ["Падение с последующим ударом"],
        },
        {
        "povod_diagnoz": "    40Ц констатировать смерть I46.1 внезапная сердечная смерть 40Ц констатировать смерть R99 другие/неуточненные причины смерти",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["Констатировать смерть"] ,
        "anamnez":    ["Смерть"],
        },
        {
        "povod_diagnoz": "999 безрезультатный",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["Безрезультативный"] ,
        "anamnez":    ["Безрезультативный"],
        },
         {
        "povod_diagnoz": "09Ж болит живот K29.9 гастродуоденит неуточненный 09Ж болит живот K85.9 острый панкреатит неуточненный K59.9 функцион-ное нарушение кишечника неут.",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["Интенсивные жгучие боли в эпигастрии"] ,
        "anamnez":    ["Ранее подобные эпизоды были, но проходили самостоятельно"],
        },
         {
        "povod_diagnoz": "09М почечная колика  N20.9 мочевые камни неуточненные",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["Дизурия (рези при мочеиспускании). Острая, нестерпимая боль в пояснице справа/слева, отдающая в пах, бедро, половые органы"] ,
        "anamnez":    ["Приступ возник внезапно после физической нагрузки/тряски/обильного питья. Ранее были эпизоды болей в пояснице, но менее интенсивные."],
        },
         {
        "povod_diagnoz": "13С сыпь L50 крапивница 13К отек Квинке",
        "type_povod": "neschastniy",
        "opisanie_zaloba":    ["Внезапное появление зудящих волдырей (как от ожога крапивой) на коже живота, рук, спины."] ,
        "anamnez":    ["Принимались антигистаминные "],
        },
]





while True:

    time.sleep(2)
    make_screen()
    time.sleep(2)
    #MAINWINDOW block
    main_window_border_click()
    time.sleep(2)
    click_obnovit()
    time.sleep(2)
    switch_status_to_slychainesozdan()
    time.sleep(2)
    if is_template_in_image(screenshot, p_mainscreen_alldone)==False and is_template_in_image(screenshot, p_mainscreen_checkin):
        time.sleep(2)
        main_window_border_click()
        time.sleep(2)
        click_obnovit()
        time.sleep(2)
        switch_status_to_slychainesozdan()
        time.sleep(2)
        click_obnovit()
        time.sleep(2)
        go_to_feldsher_window()

        # если все протоколы сделаны
    if is_template_in_image(screenshot, p_mainscreen_alldone) and is_template_in_image(screenshot, p_mainscreen_checkin):

        time.sleep(5)
        print('Все протоколы отправлены')
        print('Программа проверит появление новых через 5 минут')
        time.sleep(300)
    #FELDSHER_WINDOW block


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
            opisanie_zaloba = random.choice(matched_vizov['opisanie_zaloba'])
            anamnez = random.choice(matched_vizov['anamnez'])

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


    if is_template_in_image(screenshot, p_mainscreen_checkin)==False and is_template_in_image(screenshot, p_feldsher_checkin)==False:
        print('ОКНО С ПРОГРАММОЙ НЕ НАЙДЕНО')




















