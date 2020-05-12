
__all__ = ('ConcentricSettingsPanel', 'ConcentricSettingItem', 'ConcentricSettingString',
           'ConcentricSettingPath', 'ConcentricSettingBoolean', 'ConcentricSettingNumeric',
           'ConcentricSettingOptions', 'ConcentricSettingButtons', 'ConcentricSettingsSlider',
           'ConcentricSettingTitle', 'ConcentricSettingNumericIncrement')

import os

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.settings import SettingItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput


from ConcentricUI.circle.circlebutton import CircleButton
from ConcentricUI.circle.circletogglebutton import CircleToggleButton
from ConcentricUI.circle.circleslider import CircleSlider
from ConcentricUI.oblong.oblongbutton import OblongButton
from ConcentricUI.oblong.oblongtogglebutton import OblongToggleButton
from ConcentricUI.oblong.oblongtextinput import OblongTextInput
#from ConcentricUI.widgets.fullscreenpopup import

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.animation import Animation
from kivy.compat import string_types, text_type

kv = """
<ConcentricSettingItem>:
    size_hint: .25, None
    height: labellayout.texture_size[1] + dp(10)
    content: content
    canvas:
        Color:
            rgba: app.foreground_colour
            #rgba: 47 / 255., 167 / 255., 212 / 255., self.selected_alpha
        Rectangle:
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgb: app.background_colour
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

    BoxLayout:
        pos: root.pos

        Label:
            size_hint_x: .66
            id: labellayout
            markup: True
            text: u'[color={2}]{0}[/color]\\n[size=13sp][color={3}]{1}[/color][/size]'.format(root.title or '', root.desc or '', app.colour_references['background_colour'], app.colour_references['text_colour'])
            font_size: '15sp'
            text_size: self.width - 32, None

        BoxLayout:
            id: content
            size_hint_x: .33
            
<ConcentricSettingsSlider>:
    size_hint: 1, None
    height: labellayout.texture_size[1] + dp(30)
    content: content
    canvas:
        Color:
            rgba: app.foreground_colour
        Rectangle:
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgb: app.background_colour
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

    BoxLayout:
        pos: root.pos
        orientation: 'vertical'
        padding: 0, self.height*0.1
        #size: root.size
        size_hint: 1, 1
        Label:
            halign: 'center'
            valign: 'bottom'
            size_hint_y: .5
            id: labellayout
            markup: True
            text: u'[color={2}]{0}[/color]\\n[size=13sp][color={3}]{1}[/color][/size]'.format(root.title or '', '', app.colour_references['background_colour'], app.colour_references['text_colour'])
            font_size: '15sp'
            text_size: self.width - 32, None

        BoxLayout:
            id: content
            size_hint_y: .5
            
<ConcentricSettingTitle>:
    text_size: self.width - 32, None
    size_hint_y: None
    height: max(dp(82), self.texture_size[1] + dp(82))
    color: app.text_colour
    font_size: '18sp'
    halign: 'center'
    underline: True
    bold: True
    # outline_color: app.background_colour
    # outline_width: dp(3)
    canvas:
        # Color:
        #     rgba: .15, .15, .15, .5
        # Rectangle:
        #     pos: self.x, self.y + 2
        #     size: self.width, self.height - 2
        Color:
            rgb: app.background_colour
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

<ConcentricSettingBoolean>:
    OblongToggleButton:
        size_hint: 0.5, 0.5
        pos_hint: {'center_y': 0.5}
        text: 'ON' if self.state == 'down' else 'OFF'
        pos: root.pos
        #state: 'down' if (bool(root.values.index(root.value)) if root.value in root.values else False) else 'normal'
        on_state: root.value = 1 if args[1] == 'down' else 0
        state: 'down' if root.loaded_state else 'normal'


<ConcentricSettingString>:
    Label:
        text: root.value or ''
        pos: root.pos
        font_size: '18sp'
        color: app.text_colour

<ConcentricSettingPath>:
    Label:
        text: root.value or ''
        pos: root.pos
        font_size: '18sp'
        color: app.text_colour

<ConcentricSettingOptions>:
    Label:
        text: root.value or ''
        pos: root.pos
        font_size: '18sp'
        color: app.text_colour

<ConcentricSettingNumericIncrement>:

    BoxLayout:
    
        halign: 'center'
    
        CircleButton:
            button_source: 'minus'
            shape_size_hint_list: [0.5, 0.7, 0.8]
            allow_concentric: False
            size_hint: 0.5, 0.5
            pos_hint: {'center_y': 0.5}
            on_release: root.increment(-1)
    
        Label:
            text: root.value or ''
            pos: root.pos
            font_size: '18sp'
            color: app.text_colour  
            
        CircleButton:
            button_source: 'plus'
            shape_size_hint_list: [0.5, 0.7, 0.8]
            allow_concentric: False
            size_hint: 0.5, 0.5
            pos_hint: {'center_y': 0.5}
            on_release: root.increment(+1)
            
            
<ConcentricSettingsPanel>:
    spacing: 5
    padding: 5
    size_hint_y: None
    height: self.minimum_height

    # Label:
    #     size_hint_y: None
    #     text: root.title
    #     text_size: self.width - 32, None
    #     height: max(50, self.texture_size[1] + 20)
    #     color: (.5, .5, .5, 1)
    #     font_size: '15sp'
    # 
    #     canvas.after:
    #         Color:
    #             rgb: .2, .2, .2
    #         Rectangle:
    #             pos: self.x, self.y - 2
    #             size: self.width, 1
    """

Builder.load_string(kv)


# class ConcentricSettingItem(SettingItem):
#     pass

class ConcentricSettingItemBase(FloatLayout):
    '''Base class for individual settings (within a panel). This class cannot
    be used directly; it is used for implementing the other setting classes.
    It builds a row with a title/description (left) and a setting control
    (right).

    Look at :class:`SettingBoolean`, :class:`SettingNumeric` and
    :class:`SettingOptions` for usage examples.

    :Events:
        `on_release`
            Fired when the item is touched and then released.

    '''

    title = StringProperty('<No title set>')
    '''Title of the setting, defaults to '<No title set>'.

    :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
    '<No title set>'.
    '''

    desc = StringProperty(None, allownone=True)
    '''Description of the setting, rendered on the line below the title.

    :attr:`desc` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    disabled = BooleanProperty(False)
    '''Indicate if this setting is disabled. If True, all touches on the
    setting item will be discarded.

    :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    section = StringProperty(None)
    '''Section of the token inside the :class:`~kivy.config.ConfigParser`
    instance.

    :attr:`section` is a :class:`~kivy.properties.StringProperty` and defaults
    to None.
    '''

    key = StringProperty(None)
    '''Key of the token inside the :attr:`section` in the
    :class:`~kivy.config.ConfigParser` instance.

    :attr:`key` is a :class:`~kivy.properties.StringProperty` and defaults to
    None.
    '''

    value = ObjectProperty(None)
    '''Value of the token according to the :class:`~kivy.config.ConfigParser`
    instance. Any change to this value will trigger a
    :meth:`Settings.on_config_change` event.

    :attr:`value` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    panel = ObjectProperty(None)
    '''(internal) Reference to the SettingsPanel for this setting. You don't
    need to use it.

    :attr:`panel` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    content = ObjectProperty(None)
    '''(internal) Reference to the widget that contains the real setting.
    As soon as the content object is set, any further call to add_widget will
    call the content.add_widget. This is automatically set.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    selected_alpha = NumericProperty(0)
    '''(internal) Float value from 0 to 1, used to animate the background when
    the user touches the item.

    :attr:`selected_alpha` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 0.
    '''

    __events__ = ('on_release', )

    def __init__(self, **kwargs):
        super(ConcentricSettingItemBase, self).__init__(**kwargs)
        self.value = self.panel.get_value(self.section, self.key)

    def add_widget(self, *largs):
        if self.content is None:
            return super(ConcentricSettingItemBase, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return
        touch.grab(self)
        self.selected_alpha = 1
        return super(ConcentricSettingItemBase, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.dispatch('on_release')
            Animation(selected_alpha=0, d=.25, t='out_quad').start(self)
            return True
        return super(ConcentricSettingItemBase, self).on_touch_up(touch)

    def on_release(self):
        pass

    def on_value(self, instance, value):
        if not self.section or not self.key:
            return
        # get current value in config
        panel = self.panel
        if not isinstance(value, string_types):
            value = str(value)
        panel.set_value(self.section, self.key, value)


class ConcentricSettingItem(ConcentricSettingItemBase):
    pass

class ConcentricSettingButtons(ConcentricSettingItem):

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        # For Python3 compatibility we need to drop the buttons keyword when calling super.
        kw = kwargs.copy()
        kw.pop('buttons', None)
        super(ConcentricSettingButtons, self).__init__(**kw)
        for aButton in kwargs["buttons"]:
            oButton=CircleButton(text=aButton['title'], font_size='15sp')
            oButton.ID=aButton['id']
            self.add_widget(oButton)
            oButton.bind (on_release=self.On_ButtonPressed)
    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return
    def On_ButtonPressed(self,instance):
        self.panel.settings.dispatch('on_config_change',self.panel.config, self.section, self.key, instance.ID)


class ConcentricSettingsSlider(ConcentricSettingItemBase):


    def __init__(self, **kwargs):


        self.register_event_type('on_release')
        # For Python3 compatibility we need to drop the buttons keyword when calling super.
        kw = kwargs.copy()
        slider_kwargs = kw.pop('slider', None)


        super(ConcentricSettingsSlider, self).__init__(**kw)

        print('@@@@@@@@@@@@@@@eheheheheh', self.section, self.key, self.panel.get_value(self.section, self.key))

        print('!!!!!!!!!!!!!1231232131', slider_kwargs)

        self.slider = CircleSlider(master_colour=App.get_running_app().text_colour,
                                   text_colour=App.get_running_app().background_colour,
                                   value=self.value,
                                   **slider_kwargs)
        self.add_widget(self.slider)
        self.bind(value=self.set_slider_value)

        self.slider.bind(selected=self.value_update)

        # for aButton in kwargs["buttons"]:
        #     oButton=Button(text=aButton['title'], font_size= '15sp')
        #     oButton.ID=aButton['id']
        #     self.add_widget(oButton)
        #     oButton.bind (on_release=self.On_ButtonPressed)


    def set_slider_value(self, wid, value):
        self.slider.value = value

    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return

    def value_update(self, wid, selected):

        if selected:
            return

        self.panel.settings.dispatch('on_config_change', self.panel.config, self.section, self.key, int(wid.value))

        App.get_running_app().config.set(self.section, self.key, int(wid.value))

        filename = App.get_running_app().config.filename
        App.get_running_app().config.update_config(filename)




class ConcentricSettingSpacer(Widget):
    # Internal class, not documented.
    pass

# #  Rounded rectangle
# class ConcentricSettingItem(FloatLayout):
#     '''Base class for individual settings (within a panel). This class cannot
#     be used directly; it is used for implementing the other setting classes.
#     It builds a row with a title/description (left) and a setting control
#     (right).
#
#     Look at :class:`SettingBoolean`, :class:`SettingNumeric` and
#     :class:`SettingOptions` for usage examples.
#
#     :Events:
#         `on_release`
#             Fired when the item is touched and then released.
#
#     '''
#
#     title = StringProperty('<No title set>')
#     '''Title of the setting, defaults to '<No title set>'.
#
#     :attr:`title` is a :class:`~kivy.properties.StringProperty` and defaults to
#     '<No title set>'.
#     '''
#
#     desc = StringProperty(None, allownone=True)
#     '''Description of the setting, rendered on the line below the title.
#
#     :attr:`desc` is a :class:`~kivy.properties.StringProperty` and defaults to
#     None.
#     '''
#
#     disabled = BooleanProperty(False)
#     '''Indicate if this setting is disabled. If True, all touches on the
#     setting item will be discarded.
#
#     :attr:`disabled` is a :class:`~kivy.properties.BooleanProperty` and
#     defaults to False.
#     '''
#
#     section = StringProperty(None)
#     '''Section of the token inside the :class:`~kivy.config.ConfigParser`
#     instance.
#
#     :attr:`section` is a :class:`~kivy.properties.StringProperty` and defaults
#     to None.
#     '''
#
#     key = StringProperty(None)
#     '''Key of the token inside the :attr:`section` in the
#     :class:`~kivy.config.ConfigParser` instance.
#
#     :attr:`key` is a :class:`~kivy.properties.StringProperty` and defaults to
#     None.
#     '''
#
#     value = ObjectProperty(None)
#     '''Value of the token according to the :class:`~kivy.config.ConfigParser`
#     instance. Any change to this value will trigger a
#     :meth:`Settings.on_config_change` event.
#
#     :attr:`value` is an :class:`~kivy.properties.ObjectProperty` and defaults
#     to None.
#     '''
#
#     panel = ObjectProperty(None)
#     '''(internal) Reference to the SettingsPanel for this setting. You don't
#     need to use it.
#
#     :attr:`panel` is an :class:`~kivy.properties.ObjectProperty` and defaults
#     to None.
#     '''
#
#     content = ObjectProperty(None)
#     '''(internal) Reference to the widget that contains the real setting.
#     As soon as the content object is set, any further call to add_widget will
#     call the content.add_widget. This is automatically set.
#
#     :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and defaults
#     to None.
#     '''
#
#     selected_alpha = NumericProperty(0)
#     '''(internal) Float value from 0 to 1, used to animate the background when
#     the user touches the item.
#
#     :attr:`selected_alpha` is a :class:`~kivy.properties.NumericProperty` and
#     defaults to 0.
#     '''
#
#     __events__ = ('on_release',)
#
#     def __init__(self, **kwargs):
#         super(ConcentricSettingItem, self).__init__(**kwargs)
#         self.value = self.panel.get_value(self.section, self.key)
#
#         self.size_hint = 1, None
#
#     def add_widget(self, *largs):
#         if self.content is None:
#             return super(ConcentricSettingItem, self).add_widget(*largs)
#         return self.content.add_widget(*largs)
#
#     def on_touch_down(self, touch):
#         if not self.collide_point(*touch.pos):
#             return
#         if self.disabled:
#             return
#         touch.grab(self)
#         self.selected_alpha = 1
#         return super(ConcentricSettingItem, self).on_touch_down(touch)
#
#     def on_touch_up(self, touch):
#         if touch.grab_current is self:
#             touch.ungrab(self)
#             self.dispatch('on_release')
#             Animation(selected_alpha=0, d=.25, t='out_quad').start(self)
#             return True
#         return super(ConcentricSettingItem, self).on_touch_up(touch)
#
#     def on_release(self):
#         pass
#
#     def on_value(self, instance, value):
#         if not self.section or not self.key:
#             return
#         # get current value in config
#         panel = self.panel
#         if not isinstance(value, string_types):
#             value = str(value)
#         panel.set_value(self.section, self.key, value)


class ConcentricSettingBoolean(ConcentricSettingItem):
    '''Implementation of a boolean setting on top of a :class:`SettingItem`. It
    is visualized with a :class:`~kivy.uix.switch.Switch` widget. By default,
    0 and 1 are used for values: you can change them by setting :attr:`values`.
    '''

    values = ListProperty(['0', '1'])
    '''Values used to represent the state of the setting. If you want to use
    "yes" and "no" in your ConfigParser instance::

        SettingBoolean(..., values=['no', 'yes'])

    .. warning::

        You need a minimum of two values, the index 0 will be used as False,
        and index 1 as True

    :attr:`values` is a :class:`~kivy.properties.ListProperty` and defaults to
    ['0', '1']
    '''

    loaded_state = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if int(self.value):
            self.loaded_state = True





class ConcentricSettingString(ConcentricSettingItem):
    '''Implementation of a string setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.textinput.Textinput` so the user can enter a custom
    value.
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it's shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    textinput = ObjectProperty(None)
    '''(internal) Used to store the current textinput from the popup and
    to listen for changes.

    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text=self.value, font_size='24sp', multiline=False,
            size_hint_y=None, height='82sp')
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(ConcentricSettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = OblongButton(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = OblongButton(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()


class ConcentricSettingPath(ConcentricSettingItem):
    '''Implementation of a Path setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.filechooser.FileChooserListView` so the user can enter
    a custom value.

    .. versionadded:: 1.1.0
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it is shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    textinput = ObjectProperty(None)
    '''(internal) Used to store the current textinput from the popup and
    to listen for changes.

    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    show_hidden = BooleanProperty(False)
    '''Whether to show 'hidden' filenames. What that means is
    operating-system-dependent.

    :attr:`show_hidden` is an :class:`~kivy.properties.BooleanProperty` and
    defaults to False.

    .. versionadded:: 1.10.0
    '''

    dirselect = BooleanProperty(True)
    '''Whether to allow selection of directories.

    :attr:`dirselect` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True.

    .. versionadded:: 1.10.0
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.selection

        if not value:
            return

        self.value = os.path.realpath(value[0])

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, 0.9),
            width=popup_width)

        # create the filechooser
        initial_path = self.value or os.getcwd()
        self.textinput = textinput = FileChooserListView(
            path=initial_path, size_hint=(1, 1),
            dirselect=self.dirselect, show_hidden=self.show_hidden)
        textinput.bind(on_path=self._validate)

        # construct the content
        content.add_widget(textinput)
        content.add_widget(ConcentricSettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = OblongButton(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = OblongButton(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()


class ConcentricSettingNumeric(ConcentricSettingString):
    '''Implementation of a numeric setting on top of a :class:`SettingString`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.textinput.Textinput` so the user can enter a custom
    value.
    '''

    def _validate(self, instance):
        # we know the type just by checking if there is a '.' in the original
        # value
        is_float = '.' in str(self.value)
        self._dismiss()
        try:
            if is_float:
                self.value = text_type(float(self.textinput.text))
            else:
                self.value = text_type(int(self.textinput.text))
        except ValueError:
            return


class ConcentricSettingOptions(ConcentricSettingItem):
    '''Implementation of an option list on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    list of options from which the user can select.
    '''

    options = ListProperty([])
    '''List of all availables options. This must be a list of "string" items.
    Otherwise, it will crash. :)

    :attr:`options` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it is shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()

    def _create_popup(self, instance):
        # create the popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            content=content, title=self.title, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)

        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = OblongToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        content.add_widget(ConcentricSettingSpacer())
        btn = OblongButton(text='Cancel', size_hint_y=None, height=dp(50))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

        # and open the popup !
        popup.open()


class ConcentricSettingTitle(Label):
    '''A simple title label, used to organize the settings in sections.
    '''

    title = Label.text

    panel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ConcentricSettingTitle, self).__init__(**kwargs)
        # self.canvas.clear()
        # self.text = str(Label.text)


class ConcentricSettingsPanel(GridLayout):
    '''This class is used to contruct panel settings, for use with a
    :class:`Settings` instance or subclass.
    '''

    title = StringProperty('Default title')
    '''Title of the panel. The title will be reused by the :class:`Settings` in
    the sidebar.
    '''

    config = ObjectProperty(None, allownone=True)
    '''A :class:`kivy.config.ConfigParser` instance. See module documentation
    for more information.
    '''

    settings = ObjectProperty(None)
    '''A :class:`Settings` instance that will be used to fire the
    `on_config_change` event.
    '''

    def __init__(self, **kwargs):
        if 'cols' not in kwargs:
            self.cols = 1
        super(ConcentricSettingsPanel, self).__init__(**kwargs)

    def on_config(self, instance, value):

        if value is None:
            return
        if not isinstance(value, ConfigParser):
            raise Exception('Invalid config object, you must use a'
                            'kivy.config.ConfigParser, not another one !')

    def get_value(self, section, key):
        '''Return the value of the section/key from the :attr:`config`
        ConfigParser instance. This function is used by :class:`SettingItem` to
        get the value for a given section/key.

        If you don't want to use a ConfigParser instance, you might want to
        override this function.
        '''
        config = self.config
        if not config:
            return
        return config.get(section, key)

    def set_value(self, section, key, value):
        current = self.get_value(section, key)
        if current == value:
            return
        config = self.config
        if config:
            config.set(section, key, value)
            config.write()
        settings = self.settings
        if settings:
            settings.dispatch('on_config_change',
                              config, section, key, value)


class ConcentricSettingNumericIncrement(ConcentricSettingItem):

    def increment(self, amount):
        self.value = str(int(self.value) + amount)
