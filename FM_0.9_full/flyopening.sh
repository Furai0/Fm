#!/bin/bash

# Проверяем, установлен ли wmctrl
if ! command -v wmctrl &> /dev/null; then
    echo "Утилита wmctrl не установлена. Установите её командой:"
    echo "sudo apt install wmctrl"
    exit 1
fi

# Запускаем Fly Terminal (если ещё не запущен)
fly-terminal &

# Даём время на открытие окна
sleep 3

# Находим ID окна терминала Fly (по названию или классу)
WINDOW_ID=$(wmctrl -l | grep -i "Терминал Fly" | awk '{print $1}')

if [ -z "$WINDOW_ID" ]; then
    echo "Не удалось найти окно терминала Fly."
    exit 1
fi

# Устанавливаем размеры и положение окна (ширинаxвысота+X+Y)
wmctrl -i -r "$WINDOW_ID" -e 0,200,200,1000,600

echo "Окно терминала Fly установлено в положение 100x100 с размером 800x600."
