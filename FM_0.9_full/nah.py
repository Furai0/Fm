import pickle
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from datetime import datetime
import os
import autopy
import time
from textual.widgets import Label
from textual.screen import Screen, ModalScreen
import subprocess

file_path = os.getcwd()

def launch_script_in_terminal():
    script_path = f"{file_path}/FM_reforged2.pyc" 
    terminal_cmd = [
        "xterm",  
        "-geometry", "80x10+800+675",  
        "-T", "FM statistics",
        "-e", f"python3 {script_path}"
    ]

    process = subprocess.Popen(terminal_cmd)

    time.sleep(1)

    subprocess.run([
        "wmctrl",
        "-r", "POPA Script",  
        "-b", "add,above"
    ])


text_infa_okna_okey = """ВНИМАНИЕ
Откройте программу бригады на полный экран!
"""
text_infa_sleva = """
КУПИТЬ ПРОТОКОЛЫ:
+7 902 387 31 19
igrka4@gmail.com


АВТОМАТИЧЕСКОЕ ЗАПОЛНЕНИЕ ПРОТОКОЛОВ.

































Created by Pop it and Furai
"""


def key_check2(input_key):
    with open('data.pickle', 'rb') as keys_pack:  
        keys = pickle.load(keys_pack)  

        if input_key in keys['key100']:
            print('Ключ успешно введен, добавили 100 протоколов!')
            keys['key100'].remove(input_key)
            keys['paid'] += 100
            with open('data.pickle', 'wb') as bin_file: 
                pickle.dump(keys, bin_file)  
            return keys
        if input_key in keys['key500']:
            print('Ключ успешно введен, добавили 500 протоколов!')
            keys['key500'].remove(input_key)
            keys['paid'] += 500
            with open('data.pickle', 'wb') as bin_file:
                pickle.dump(keys, bin_file)
            return keys
        if input_key in keys['key1000']:
            print('Ключ успешно введен, добавили 1000 протоколов!')
            keys['key1000'].remove(input_key)
            keys['paid'] += 1000
            with open('data.pickle', 'wb') as bin_file:
                pickle.dump(keys, bin_file)
            return keys
        else:
            print('Ключ не верный или уже использовался')


def load_protocols(file_path):
    try:
        with open(file_path, 'rb') as bin_file:  
            data = pickle.load(bin_file)  
            if 'paid' not in data:
                data['paid'] = 0
                data['key100'] = []
                data['key500'] = []
                data['key1000'] = []
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)  
            return data
    except (FileNotFoundError, pickle.PickleError):
        default_data = {
            'paid': 0,
            'key100': [],
            'key500': [],
            'key1000': []
        }
        with open(file_path, 'wb') as f: 
            pickle.dump(default_data, f) 
        return default_data


class ConfirmationScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(text_infa_okna_okey),
            Horizontal(
                Button("Понятно", variant="success", id="ok"),
                Button("Отмена", variant="error", id="cancel"),
            ),
            id="dialog"
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(True)
            launch_script_in_terminal()
        else:
            self.dismiss(False)


class FM(App):
    authenticated = reactive(False)
    message = reactive("")
    contacts_left = reactive(f"{text_infa_sleva}")
    contacts_right = reactive("")
    device_status = reactive("Выключено")
    stats = reactive({})

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="controls"):
                yield Input(placeholder="ВВЕДИТЕ КЛЮЧ ДОСТУПА",
                            password=False,
                            id="key-input",
                            disabled=self.stats.get('paid', 0) > 0)
                yield Button("ВКЛЮЧИТЬ", id="on",
                             disabled=not (self.stats.get('paid', 0) > 0),
                             variant="success")
                yield Static("", id="message")
                yield Static(self.contacts_left, id="contacts-left")

            with Vertical(id="status"):
                yield Static(self._format_stats(), id="stats-display")
                yield Static(self.contacts_right, id="contacts-right")

    async def on_mount(self):
        self.stats = load_protocols("data.pickle")  
        self.valid_keys = self.stats

        if self.stats.get('paid', 0) > 0:
            self.authenticated = True
            self.query_one("#message").update(f"[green]Доступ разрешён ({self.stats['paid']} протоколов)")

        self._setup_styles()
        self._update_stats_display()

    def _setup_styles(self):
        self.query_one("#on").styles.width = 25
        self.query_one("#on").styles.height = 4
        self.query_one("#key-input").styles.width = 25
        self.query_one("#key-input").styles.height = 3

        self.query_one("#on").styles.background = "darkgreen"
        self.query_one("#on").styles.color = "white"

        self.query_one("#contacts-left").styles.border_top = ("heavy", "gray")
        self.query_one("#contacts-right").styles.border_top = ("heavy", "gray")
        self.query_one("#stats-display").styles.border = ("round", "blue")
        self.query_one("#stats-display").styles.content_align = ("center", "middle")
        self.query_one("#stats-display").styles.font_size = "32px"

    def _format_stats(self) -> str:
        return f"СТАТИСТИКА ПРОТОКОЛОВ: {self.stats.get('paid', 0)}"

    def _update_stats_display(self):
        self.query_one("#stats-display").update(self._format_stats())

    def watch_authenticated(self, auth: bool):
        if self.stats.get('paid', 0) > 0:
            self.query_one("#key-input").disabled = True
            self.query_one("#key-input").styles.border = ("round", "green")
        else:
            self.query_one("#key-input").disabled = auth
            border_color = "green" if auth else "red"
            self.query_one("#key-input").styles.border = ("round", border_color)

        self.query_one("#on").disabled = not auth

    def on_input_submitted(self, event: Input.Submitted):
        if not isinstance(self.valid_keys, dict):
            self.query_one("#message").update("[red]Ошибка загрузки ключей")
            return

        input_key = event.value.strip()
        found = False

        for key_type, count in [("key100", 100), ("key500", 500), ("key1000", 1000)]:
            if input_key in self.valid_keys.get(key_type, []):
                self._process_valid_key(input_key, key_type, count)
                found = True
                break

        if not found:
            self.query_one("#message").update("[red]Неверный ключ")
        event.input.value = ""

    def _process_valid_key(self, key, key_type, count):
        self.valid_keys[key_type].remove(key)
        self.valid_keys["paid"] += count

        with open("data.pickle", 'wb') as f:
            pickle.dump(self.valid_keys, f)

        self.authenticated = True
        self.stats = self.valid_keys
        self.query_one("#message").update(f"[green]Доступ разрешён ({count} протоколов)")
        self._update_stats_display()

    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "on":
            confirmed = await self.push_screen(ConfirmationScreen())
            if confirmed:
                self.query_one("#on").styles.background = "green"
                self.contacts_right = "Системный статус: Устройство активно"


if __name__ == "__main__":
    app = FM()
    app.run()
