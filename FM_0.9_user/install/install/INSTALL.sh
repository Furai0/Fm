#!/bin/bash

cd /home/adisadmin/Desktop/FM_0.9/install/install_test
# Установка deb-пакетов
echo "Устанавливаю deb-пакеты..."
sudo dpkg -i 1.deb 2.deb 3.deb
sudo apt-get install -f

# Запуск get-pip.py
echo "Запускаю get-pip.py..."
python3 get-pip.py

# Установка Python-пакетов из локальной директории
echo "Устанавливаю Python-пакеты..."
python3 -m pip install --no-index --find-links=./ wheel
python3 -m pip install --no-index --find-links=./ setuptools
python3 -m pip install --no-index --find-links=./ autopy 
python3 -m pip install --no-index --find-links=./ opencv-python 
python3 -m pip install --no-index --find-links=./ numpy art 
python3 -m pip install --no-index --find-links=./ pyperclip 
python3 -m pip install --no-index --find-links=./ clipboard 
python3 -m pip install --no-index --find-links=./ pillow
python3 -m pip install --no-index --find-links=./ pyautogui

python3 -m pip install --no-index --find-links=./ pyscreeze 
python3 -m pip install --no-index --find-links=./ mss 
python3 -m pip install --no-index --find-links=./ textual

echo "Все операции завершены."

exit 0
