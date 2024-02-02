from kivy.app import App
from string import ascii_letters, digits, punctuation
from random import choice
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase

LabelBase.register("Consolans", fn_regular="C:\Windows\Fonts\consola.ttf", fn_bold="C:\Windows\Fonts\consolab.ttf", 
                    fn_bolditalic="C:\Windows\Fonts\consolaz.ttf", fn_italic="C:\Windows\Fonts\consolai.ttf")

GREEN, RED = [0, 1, 0, 1], [1, 0, 0, 1]

class PasswordGenerator(Widget):
    characters = [ascii_letters, digits, ""]
    def generate_password(self):
        return ''.join([choice(''.join(self.characters)) for _ in range(self.root.ids.password_length.value)])

    def on_focus(self):
        if self.root.ids.password.text == '': return
        self.root.ids.password.copy(self.root.ids.password.text)
        self.root.ids.hint_label.text = "Скопировано"
        self.root.ids.hint_label.color = GREEN
        self.root.ids.password.focus = False
        self.root.ids.password.delete_selection()
        def back(_):
            self.root.ids.hint_label.text = "Двигайте ползунок, чтоб получить пароль\nЧтоб скопировать пароль нажмите на него"
            self.root.ids.hint_label.color = [1, 1, 1, 1]
        Clock.schedule_once(back, 1)

    def change_text(self):
        if len(self.root.ids.password.text) == self.root.ids.password_length.value:
            return
        self.root.ids.password.text = self.generate_password()

    def change_characters(self, button_name: str):
        cur_button = eval(f'self.root.ids.{button_name}')
        groups = {'abcd_button': [0, ascii_letters], 'digits_button': [1, digits], 'symbols_button': [2, punctuation]}
        abcd, digit, symbol = self.root.ids.abcd_button, self.root.ids.digits_button, self.root.ids.symbols_button             
        if cur_button.background_color == GREEN:
            self.characters[groups[button_name][0]] = ""
            cur_button.background_color = RED
        else:
            self.characters[groups[button_name][0]] = groups[button_name][1]
            cur_button.background_color = GREEN
        
        if [abcd.background_color, digit.background_color, symbol.background_color] == [RED, RED, RED]:
            self.characters[groups[button_name][0]] = groups[button_name][1]
            cur_button.background_color = GREEN


class PasswordGeneratorApp(App, PasswordGenerator):
    def build(self):
        return PasswordGenerator()


if __name__ == '__main__':
    PasswordGeneratorApp().run()
