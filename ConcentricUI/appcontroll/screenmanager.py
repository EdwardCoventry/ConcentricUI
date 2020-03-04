from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window


class AdvancedScreenManager(ScreenManager):


    def __init__(self, **kwargs):
        super(AdvancedScreenManager, self).__init__(**kwargs)
        self.back_key = 27 if platform is 'android' else 269  # 269 = numpad subtract
        Window.bind(on_keyboard=self._on_keyboard)

    def _on_keyboard(self, widget, key, scancode, codepoint, modifiers, *args):
        if key == self.back_key:  # 27 for esc
            self.current = 'Home Screen'
            return True
