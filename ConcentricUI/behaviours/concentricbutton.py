""" Some notes go here """

from kivy.clock import Clock

all__ = ('ConcentricButton',)

from kivy.uix.button import ButtonBehavior

from ConcentricUI.behaviours.concentriclabel import ConcentricLabel


class ConcentricButton(ButtonBehavior, ConcentricLabel):

    def on_state(self, *args):

        Clock.schedule_once(self.set_trim, -1)
        #Clock.schedule_once(partial(self.on_show_trim, True), -1)

        # super(ConcentricButton, self).on_state(*args)

    def set_trim(self, *args):
        if self.state == 'down':
            self.show_trim = True
        else:
            self.show_trim = False

    def __init__(self, **kwargs):

        super(ConcentricButton, self).__init__(**kwargs)

        self.show_trim = False

        self.background_color = None
        self.background_normal = None
        self.background_down = None
        self.background_disabled_normal = None
        self.background_disabled_down = None

        # self.bind(state=self.set_trim)
