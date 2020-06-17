from kivy.app import App
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window


class AdvancedScreenManager(ScreenManager):

    def get_last_screen(self):
        last_screen = App.get_running_app().config.get('internal', 'last screen')
        print('%%%%%%%%%%%%%%%%', last_screen)
        return last_screen

    def set_current_from_last_screen(self, *args):
        print("hey hey hey heyh ye")
        self.current = self.last_screen

    def on_current(self, instance, value):
        super(AdvancedScreenManager, self).on_current(instance, value)
        if value:
            self.save_screen_for_reload(value)

    def save_screen_for_reload(self, screen_name):
        App.get_running_app().config.set('internal', 'last screen', screen_name)
        App.get_running_app().save_config()
        print('should be saved.............................', screen_name)

    def __init__(self, **kwargs):
        self.last_screen = self.get_last_screen()
        super(AdvancedScreenManager, self).__init__(**kwargs)
        self.back_keys = [4, 27] if platform == 'android' else [269, 127]  # 269 = numpad subtract
        Window.bind(on_keyboard=self._on_keyboard)

    def _on_keyboard(self, widget, key, scancode, codepoint, modifiers, *args):
        if key in self.back_keys:  # 27 for esc
            self.current = 'Home Screen'
            return True
