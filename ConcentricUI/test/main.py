from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from concentricui.circle.circleslider import CircleSlider
from concentricui.circle.doublecircleslider import DoubleCircleSlider
from concentricui.oblong.oblongtogglebutton import OblongToggleButton


class TestWidget(OblongToggleButton):

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        if keycode[1] == 'left':
            self.x -= 10
        elif keycode[1] == 'right':
            self.x += 10
        elif keycode[1] == 'up':
            self.y += 10
        elif keycode[1] == 'down':
            self.y -= 10
        return True


from kivy.core.window import Window

from concentricui.widgets.screenchangespinner import ScreenChangeSpinner

from kivy.uix.screenmanager import ScreenManager

# class TestApp(App):
#
#         #bl.add_widget(circle_label)
#         #bl.add_widget(hoblong_label)
#         #bl.add_widget(voblong_label)
#         #bl.add_widget(rect_label)
#         #w1 = OblongSpinner(text='test_1', shape_size_hint_list=[0.7, 0.8, 0.9], master_colour=(1,0,1))
#         #w1 = OblongToggleButton(shape_size_hint_list=[0.7, 0.8, 0.9], master_colour=(0.2,1,0.3,0.1))
#
#         circle_slider = DoubleCircleSlider(range=(1, 9),values=(5, 5),display_value_toggle=True, size_hint_y=0.3, orientation='horizontal', shape_size_hint_list=[0.7, 0.8, 0.9], master_colour=(1,0,1))
#         #circle_slider = CircleSlider(range=(250, 500),value=399,display_value_toggle=True, size_hint_y=0.3, orientation='horizontal', shape_size_hint_list=[0.7, 0.8, 0.9], master_colour=(1,0,1))
#         #w2 = OblongTextInput(shape_size_hint_list=[0.7, 0.8, 0.9], master_colour=(1,0,1,0.1))
#         #w2 = OblongSpinner(total_height=Window.height, size_hint_y=0.2,option_cls_kwargs={'opening_pin':circle_slider, 'closing_pin':True, 'shape_size_hint_list':[0.8, 0.7], 'master_colour':(1,1,0,1)}, values=['1aaaaaaaaaaaaaabbb','2aaaaaaaaaaaaaabbb','3aaaaaaaaaaaaaabbb','4aaaaaaaaaaaaaabbb','5aaaaaaaaaaaaaabbb'], text_colour=(0,1,1,1),opening_pin='True',closing_pin=circle_slider, shape_size_hint_list=[0.7, 1], master_colour=(1,0,1,1))

from concentricui.colourscheme.colourscreen import ColourScreen

from concentricui.circle.circletogglebutton import CircleToggleButton


# Declare both screens
class MenuScreen(ColourScreen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

        self.foreground_colour = '#41f46e'
        self.background_colour = '#f4c141'
        self.trim_colour = '#f44242'
        self.text_colour = '#123456'

        boxlay = BoxLayout(orientation='vertical', top=self.top_bar_y)
        double_circle_slider = DoubleCircleSlider(range=(1, 9), values=(5, 5), display_value_toggle=True,
                                                  size_hint_y=0.1, orientation='horizontal',
                                                  shape_size_hint_list=[0.6, 1])

        # circle_slider = CircleSlider(range=(1, 9), master_colour='foreground_colour', colour_scheme='screen', value=5,
        #                              display_value_toggle=True, size_hint_y=0.1, orientation='horizontal',
        #                              shape_size_hint_list=[0.6, 1])
        circle_slider = CircleSlider()

        textinput = CircleToggleButton(text_colour='#123456', master_colour='#339966',
                                       colour_scheme='screen')  # , shape_size_hint_list=[0.6, 1])
        #
        boxlay.add_widget(double_circle_slider)
        boxlay.add_widget(circle_slider)  # master_colour=(0.4,0.2,0.7,1),
        boxlay.add_widget(textinput)  # master_colour=(0.4,0.2,0.7,1),
        boxlay.add_widget(
            ScreenChangeSpinner(master_colour='#339966', text_colour='#634521', colour_scheme='screen', id='coolio',
                                option_cls_kwargs={'shape_size_hint_list': [0.6, 0.9]}, opening_pin='True',
                                closing_pin='True', shape_size_hint_list=[0.8, 0.9]))
        self.add_widget(boxlay)


class SettingsScreen(ColourScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='Menu'))
sm.add_widget(SettingsScreen(name='Settings'))

from concentricui.colourscheme.colourwidget import ColourProperties


class TestApp(App, ColourProperties):

    def build(self):
        self.background_colour = '#434359'
        self.foreground_colour = '#7993ad'
        self.trim_colour = '#e6e0be'
        self.text_colour = '#d8d9c7'
        self.features_colour = '#ff00d4'

        return sm


if __name__ == '__main__':
    TestApp().run()
