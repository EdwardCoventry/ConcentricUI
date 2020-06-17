
'''
Settings
========

.. versionadded:: 1.0.7

This module provides a complete and extensible framework for adding a
Settings interface to your application. By default, the interface uses
a :class:`SettingsWithSpinner`, which consists of a
:class:`~kivy.uix.spinner.Spinner` (top) to switch between individual
settings panels (bottom). See :ref:`differentlayouts` for some
alternatives.

.. image:: images/settingswithspinner_kivy.jpg
    :align: center

A :class:`SettingsPanel` represents a group of configurable options. The
:attr:`SettingsPanel.title` property is used by :class:`Settings` when a panel
is added: it determines the name of the sidebar button. SettingsPanel controls
a :class:`~kivy.config.ConfigParser` instance.

The panel can be automatically constructed from a JSON definition file: you
describe the settings you want and corresponding sections/keys in the
ConfigParser instance... and you're done!

Settings are also integrated into the :class:`~kivy.app.App` class. Use
:meth:`Settings.add_kivy_panel` to configure the Kivy core settings in a panel.


.. _settings_json:

Create a panel from JSON
------------------------

To create a panel from a JSON-file, you need two things:

    * a :class:`~kivy.config.ConfigParser` instance with default values
    * a JSON file

.. warning::

    The :class:`kivy.config.ConfigParser` is required. You cannot use the
    default ConfigParser from Python libraries.

You must create and handle the :class:`~kivy.config.ConfigParser`
object. SettingsPanel will read the values from the associated
ConfigParser instance. Make sure you have set default values (using
:attr:`~kivy.config.ConfigParser.setdefaults`) for all the sections/keys
in your JSON file!

The JSON file contains structured information to describe the available
settings. Here is an example::

    [
        {
            "type": "title",
            "title": "Windows"
        },
        {
            "type": "bool",
            "title": "Fullscreen",
            "desc": "Set the window in windowed or fullscreen",
            "section": "graphics",
            "key": "fullscreen"
        }
    ]

Each element in the root list represents a setting that the user can configure.
Only the "type" key is mandatory: an instance of the associated class will be
created and used for the setting - other keys are assigned to corresponding
properties of that class.

    ============== =================================================
    Type           Associated class
    -------------- -------------------------------------------------
    title          :class:`SettingTitle`
    bool           :class:`SettingBoolean`
    numeric        :class:`SettingNumeric`
    options        :class:`SettingOptions`
    string         :class:`SettingString`
    path           :class:`SettingPath`
    ============== =================================================

    .. versionadded:: 1.1.0
        Added :attr:`SettingPath` type

In the JSON example above, the first element is of type "title". It will create
a new instance of :class:`SettingTitle` and apply the rest of the key-value
pairs to the properties of that class, i.e. "title": "Windows" sets the
:attr:`~SettingsPanel.title` property of the panel to "Windows".

To load the JSON example to a :class:`Settings` instance, use the
:meth:`Settings.add_json_panel` method. It will automatically instantiate a
:class:`SettingsPanel` and add it to :class:`Settings`::

    from kivy.config import ConfigParser

    config = ConfigParser()
    config.read('myconfig.ini')

    s = Settings()
    s.add_json_panel('My custom panel', config, 'settings_custom.json')
    s.add_json_panel('Another panel', config, 'settings_test2.json')

    # then use the s as a widget...


.. _differentlayouts:

Different panel layouts
-----------------------

A kivy :class:`~kivy.app.App` can automatically create and display a
:class:`Settings` instance. See the :attr:`~kivy.app.App.settings_cls`
documentation for details on how to choose which settings class to
display.

Several pre-built settings widgets are available. All except
:class:`SettingsWithNoMenu` include close buttons triggering the
on_close event.

- :class:`Settings`: Displays settings with a sidebar at the left to
  switch between json panels.

- :class:`SettingsWithSidebar`: A trivial subclass of
  :class:`Settings`.

- :class:`SettingsWithSpinner`: Displays settings with a spinner at
  the top, which can be used to switch between json panels. Uses
  :class:`InterfaceWithSpinner` as the
  :attr:`~Settings.interface_cls`. This is the default behavior from
  Kivy 1.8.0.

- :class:`SettingsWithTabbedPanel`: Displays json panels as individual
  tabs in a :class:`~kivy.uix.tabbedpanel.TabbedPanel`. Uses
  :class:`InterfaceWithTabbedPanel` as the :attr:`~Settings.interface_cls`.

- :class:`SettingsWithNoMenu`: Displays a single json panel, with no
  way to switch to other panels and no close button. This makes it
  impossible for the user to exit unless
  :meth:`~kivy.app.App.close_settings` is overridden with a different
  close trigger! Uses :class:`InterfaceWithNoMenu` as the
  :attr:`~Settings.interface_cls`.

You can construct your own settings panels with any layout you choose
by setting :attr:`Settings.interface_cls`. This should be a widget
that displays a json settings panel with some way to switch between
panels. An instance will be automatically created by :class:`Settings`.

Interface widgets may be anything you like, but *must* have a method
add_panel that receives newly created json settings panels for the
interface to display. See the documentation for
:class:`InterfaceWithSidebar` for more information. They may
optionally dispatch an on_close event, for instance if a close button
is clicked. This event is used by :class:`Settings` to trigger its own
on_close event.

For a complete, working example, please see
:file:`kivy/examples/settings/main.py`.

'''

__all__ = ('Settings', 'InterfaceWithSidebar', 'ContentPanel', 'MenuSidebar')

import json
import os
from functools import partial

from kivy.app import App
from ConcentricUI.circle.circlebutton import CircleButton
from ConcentricUI.circle.circletogglebutton import CircleToggleButton
from ConcentricUI.oblong.oblongtogglebutton import OblongToggleButton
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.factory import Factory
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import rgba

from ConcentricUI.settings.settingsitems import *


class InterfaceWithSidebar(BoxLayout):
    '''The default Settings interface class. It displays a sidebar menu
    with names of available settings panels, which may be used to switch
    which one is currently displayed.

    See :meth:`~InterfaceWithSidebar.add_panel` for information on the
    method you must implement if creating your own interface.

    This class also dispatches an event 'on_close', which is triggered
    when the sidebar menu's close button is released. If creating your
    own interface widget, it should also dispatch such an event which
    will automatically be caught by :class:`Settings` and used to
    trigger its own 'on_close' event.

    '''

    menu = ObjectProperty()
    '''(internal) A reference to the sidebar menu widget.

    :attr:`menu` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    content = ObjectProperty()
    '''(internal) A reference to the panel display widget (a
    :class:`ContentPanel`).

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    __events__ = ('on_close',)

    def __init__(self, *args, **kwargs):
        super(InterfaceWithSidebar, self).__init__(*args, **kwargs)
        self.menu.close_button.bind(
            on_release=lambda j: self.dispatch('on_close'))

    def add_panel(self, panel, name, uid):
        '''This method is used by Settings to add new panels for possible
        display. Any replacement for ContentPanel *must* implement
        this method.

        :Parameters:
            `panel`: :class:`SettingsPanel`
                It should be stored and the interface should provide a way to
                switch between panels.
            `name`:
                The name of the panel as a string. It may be used to represent
                the panel but isn't necessarily unique.
            `uid`:
                A unique int identifying the panel. It should be used to
                identify and switch between panels.

        '''
        self.menu.add_item(name, uid)
        self.content.add_panel(panel, name, uid)

    def on_close(self, *args):
        pass



class ContentPanel(ScrollView):
    '''A class for displaying settings panels. It displays a single
    settings panel at a time, taking up the full size and shape of the
    ContentPanel. It is used by :class:`InterfaceWithSidebar` and
    :class:`InterfaceWithSpinner` to display settings.

    '''

    panels = DictProperty({})
    '''(internal) Stores a dictionary mapping settings panels to their uids.

    :attr:`panels` is a :class:`~kivy.properties.DictProperty` and
    defaults to {}.

    '''

    container = ObjectProperty()
    '''(internal) A reference to the GridLayout that contains the
    settings panel.

    :attr:`container` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    current_panel = ObjectProperty(None)
    '''(internal) A reference to the current settings panel.

    :attr:`current_panel` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    current_uid = NumericProperty(0)
    '''(internal) A reference to the uid of the current settings panel.

    :attr:`current_uid` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.

    '''

    def add_panel(self, panel, name, uid):
        '''This method is used by Settings to add new panels for possible
        display. Any replacement for ContentPanel *must* implement
        this method.

        :Parameters:
            `panel`: :class:`SettingsPanel`
                It should be stored and displayed when requested.
            `name`:
                The name of the panel as a string. It may be used to represent
                the panel.
            `uid`:
                A unique int identifying the panel. It should be stored and
                used to identify panels when switching.

        '''
        self.panels[uid] = panel
        if not self.current_uid:
            self.current_uid = uid

    def clear_panels(self):
        self.panels = []
        # self.current_uid = None

    def on_current_uid(self, *args):
        '''The uid of the currently displayed panel. Changing this will
        automatically change the displayed panel.

        :Parameters:
            `uid`:
                A panel uid. It should be used to retrieve and display
                a settings panel that has previously been added with
                :meth:`add_panel`.

        '''
        uid = self.current_uid
        if uid in self.panels:
            if self.current_panel is not None:
                self.remove_widget(self.current_panel)
            new_panel = self.panels[uid]
            self.add_widget(new_panel)
            self.current_panel = new_panel
            return True
        return False  # New uid doesn't exist

    def add_widget(self, widget):
        if self.container is None:
            super(ContentPanel, self).add_widget(widget)
        else:
            self.container.add_widget(widget)

    def remove_widget(self, widget):
        self.container.remove_widget(widget)


class Settings(BoxLayout):
    '''Settings UI. Check module documentation for more information on how
    to use this class.

    :Events:
        `on_config_change`: ConfigParser instance, section, key, value
            Fired when the section's key-value pair of a ConfigParser changes.

            .. warning:

                value will be str/unicode type, regardless of the setting
                type (numeric, boolean, etc)
        `on_close`
            Fired by the default panel when the Close button is pressed.

        '''

    interface = ObjectProperty(None)
    '''(internal) Reference to the widget that will contain, organise and
    display the panel configuration panel widgets.

    :attr:`interface` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    interface_cls = ObjectProperty(InterfaceWithSidebar)
    '''The widget class that will be used to display the graphical
    interface for the settings panel. By default, it displays one Settings
    panel at a time with a sidebar to switch between them.

    :attr:`interface_cls` is an
    :class:`~kivy.properties.ObjectProperty` and defaults to
    :class:`InterfaceWithSidebar`.

    .. versionchanged:: 1.8.0
        If you set a string, the :class:`~kivy.factory.Factory` will be used to
        resolve the class.

    '''

    __events__ = ('on_close', 'on_config_change')

    def __init__(self, *args, **kargs):
        self._types = {}
        super(Settings, self).__init__(*args, **kargs)

        # self.create_interface('bicycling')
        # self.create_interface('walking')

        self.common_panel_count = 0
        self.multi_panel_count = 0

        # config_type = App.get_running_app().config_type
        # if config_type in ('bicycling'):
        #     mode = 'bicycling'
        # elif config_type in ('walking, transit'):
        #     mode = 'walking'

        self.interface_dict = {'common': self.create_interface('common'),
                               'walking': self.create_interface('walking'),
                               'bicycling': self.create_interface('bicycling')}

        self.switch_interface()

        self.register_type('string', ConcentricSettingString)
        self.register_type('bool', ConcentricSettingBoolean)
        self.register_type('numeric', ConcentricSettingNumeric)
        self.register_type('options', ConcentricSettingOptions)
        self.register_type('title', ConcentricSettingTitle)
        self.register_type('path', ConcentricSettingPath)
        self.register_type('buttons', ConcentricSettingButtons)
        self.register_type('slider', ConcentricSettingsSlider)
        self.register_type('numericincrement', ConcentricSettingNumericIncrement)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            super(Settings, self).on_touch_down(touch)
            return True

    def register_type(self, tp, cls):
        '''Register a new type that can be used in the JSON definition.
        '''
        self._types[tp] = cls

    def on_close(self, *args):
        pass

    called_count = 0

    def switch_interface(self, switch_from=None, *args):

        self.called_count += 1

        # if switch_from:
        #     new = switch_from
        # else:
        #     new = App.get_running_app().config_type
        #
        # old = 'bicycling' if new is 'walking' else 'walking'
        #

        # print('removing', old, 'adddding', new)
        if self.interface:
            old_mode = self.interface.config_type

            if old_mode == 'walking':
                new_mode = 'bicycling'
            elif old_mode == 'bicycling':
                new_mode = 'common'
            elif old_mode == 'common':
                new_mode = 'walking'
            else:
                raise Exception("mode {} not recognised".format(old_mode))

            self.remove_interface()
            self.add_interface(new_mode)
        else:
            self.add_interface('common')
            # print('using route mode')
            # config_type = App.get_running_app().route_mode
            # self.add_interface(config_type)

        # uid = self.interface.get_current()
        # self.interface.set_current(uid)

    def create_interface(self, mode=None):

        cls = self.interface_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        interface = cls()
        interface.config_type = mode
        # self.interface = interface
        # if mode:
        #     self.interface_dict[mode] = self.interface
        return interface

    def remove_interface(self):

        # if not mode:
        #     interface = self.interface
        # else:
        #     interface = self.interface_dict[mode]
        # group = self.interface.config_type + '_menu_section'
        # print('iiiiiiiiiiiiiiiiiiiiiiiiii', group, [button.state for button in ToggleButton.get_widgets('menu_section')])

        self.interface.menu.settings_mode_button.clear_callbacks()

        self.remove_widget(self.interface)
        # self.interface = None

    def add_interface(self, mode=None):

        '''(Internal) creates an instance of :attr:`Settings.interface_cls`,
        and sets it to :attr:`~Settings.interface`. When json panels are
        created, they will be added to this interface which will display them
        to the user.
        '''
        # if not mode:
        #     print('NO MODE AT ALL!')
        #     self.interface = self.create_interface()
        # else:

        if mode == 'bicycling':
            mode = 'bicycling'
        if mode in ('walking', 'transit'):
            mode = 'walking'

        self.interface = self.interface_dict[mode]
        # self.interface = self.create_interface(mode)

        self.add_widget(self.interface)
        self.interface.bind(on_close=lambda j: self.dispatch('on_close'))

        # print('the one to remove will be:', mode)
        self.interface.menu.settings_mode_button.set_button(self.interface.config_type)
        self.interface.menu.settings_mode_button.bind(on_release=self.switch_interface)
        # self.interface.menu.settings_mode_button.bind(on_release=partial(App.get_running_app().build_settings, self))

    def on_config_change(self, config, section, key, value):
        pass

    def common_add_json_panel(self, title, config, filename=None, data=None):

        self.common_panel_count += 1

        panel = self.create_json_panel(title, config, filename, data)
        uid = panel.uid

        interface = self.interface_dict['common']
        if interface is not None:

            interface.add_panel(panel, title, uid)
            panel.interface = interface


    def multi_add_json_panel(self, title, config_dict, filename=None, data=None):

        self.multi_panel_count += 1

        for config_type, interface in self.interface_dict.items():
            if config_type == 'common':
                continue
            config = config_dict[config_type]
            panel = self.create_json_panel(title, config, filename, data)
            uid = panel.uid
            if interface is not None:
                interface.add_panel(panel, title, uid)

    def add_json_panel(self, title, config, filename=None, data=None):
        '''Create and add a new :class:`SettingsPanel` using the configuration
        `config` with the JSON definition `filename`.

        Check the :ref:`settings_json` section in the documentation for more
        information about JSON format and the usage of this function.
        '''

        panel = self.create_json_panel(title, config, filename, data)

        uid = panel.uid
        if self.interface is not None:
            self.interface.add_panel(panel, title, uid)

    def add_custom_panel(self, title, widget):
        uid = widget.uid
        if self.interface is not None:
            self.interface.add_panel(widget, title, uid)


    def clear_json_panels(self):
        self.interface.clear_panels()

    def create_json_panel(self, title, config, filename=None, data=None):
        '''Create new :class:`SettingsPanel`.

        .. versionadded:: 1.5.0

        Check the documentation of :meth:`add_json_panel` for more information.
        '''

        if filename is None and data is None:
            raise Exception('You must specify either the filename or data')
        if filename is not None:
            with open(filename, 'r') as fd:
                data = json.loads(fd.read())
        else:
            data = json.loads(data)
        if type(data) != list:
            raise ValueError('The first element must be a list')
        panel = ConcentricSettingsPanel(title=title, settings=self, config=config)

        for setting in data:
            # determine the type and the class to use
            if 'type' not in setting:
                raise ValueError('One setting are missing the "type" element')
            ttype = setting['type']
            cls = self._types.get(ttype)
            if cls is None:
                raise ValueError(
                    'No class registered to handle the <%s> type' %
                    setting['type'])

            # create a instance of the class, without the type attribute
            del setting['type']
            str_settings = {}
            for key, item in setting.items():
                str_settings[str(key)] = item

            instance = cls(panel=panel, **str_settings)

            # instance created, add to the panel
            panel.add_widget(instance)

        return panel

    def add_kivy_panel(self):
        '''Add a panel for configuring Kivy. This panel acts directly on the
        kivy configuration. Feel free to include or exclude it in your
        configuration.

        See :meth:`~kivy.app.App.use_kivy_settings` for information on
        enabling/disabling the automatic kivy panel.

        '''
        from kivy import kivy_data_dir
        from kivy.config import Config
        from os.path import join
        self.add_json_panel('Kivy', Config,
                            join(kivy_data_dir, 'settings_kivy.json'))


# from naviUI import CircleButton, CircleToggleButton, ModeButton

class SettingsSectionButton(OblongToggleButton):
    uid = NumericProperty()
    section = StringProperty()
    down = StringProperty()
    config_type = StringProperty()
    interface = ObjectProperty()

    def on_section(self, wid, section, *args):
        #self.text = section[:3]
        self.text = section.split(' ')[0]

    def __init__(self, **kwargs):
        super(SettingsSectionButton, self).__init__(**kwargs)

    def on_state(self, wid, state, *args):
        if state == 'down':
            self.__class__.down = self.section

            self.disabled = True
        if state == 'normal':
            self.disabled = False

    def load_state(self):

        # self.interface.set_current(self.uid)

        # return

        self.state = 'down' if self.down == self.section else 'normal'

        if self.state == 'down':
            self.interface.set_current(self.uid)


class SettingsModeButton(Widget):
    """ This will just be a spacer unless you overwrite it! """

    size_hint = None, None
    size = 0, 0

    def __init__(self, **kwargs):
        #self.
        super(SettingsModeButton, self).__init__(**kwargs)

    def set_button(self, *args):
        pass

    def on_release(self, *args):
        pass

class MenuCirclebar(BoxLayout):
    close_button = ObjectProperty()
    interface = ObjectProperty()

    config_type = StringProperty()

    any_down = False

    def __init__(self, *args, **kwargs):

        super(MenuCirclebar, self).__init__(*args, **kwargs)

        self.back_button = CircleButton(button_source='backwards',
                                        shape_size_hint_list=[0.5, 0.7, 0.7],
                                        allow_concentric=False,
                                        on_release=App.get_running_app().close_settings,
                                        size_hint_x=0.25)

        #self.back_button.image_source = "textures/buttons/backwards_button.png"

        self.add_widget(self.back_button)

        #  this is just a spacer
        #self.add_widget(Widget(size_hint_x=0.25))


        self.settings_mode_button = SettingsModeButton()

        self.settings_sections_buttons = []

        self.add_widget(self.settings_mode_button)

        #  this is just a spacer
        #self.add_widget(Widget(size_hint_x=0.25))

        self.padding = [0, 10, 0, 0]

        #self.settings_mode_button.bind(master_colour=self.set_buttons_colour)

    def add_item(self, name, uid):

        state = 'down' if not self.any_down else 'normal'
        self.any_down = True

        # group = self.config_type + '_menu_section'
        # print('groupy', group)

        button = SettingsSectionButton(section=name,
                                       # button_colour=rgba('#ECA793'),
                                       id=name + '_button',
                                       group='menu_section',
                                       config_type=self.config_type,
                                       state=state,
                                       uid=uid,
                                       interface=self.interface,
                                       master_colour=App.get_running_app().background_colour)

        self.settings_sections_buttons.append(button)

        self.add_widget(widget=button)

    def add_spacer(self):
        self.add_widget(widget=Widget())

    def clear_items(self):
        for wid in self.children:
            if not isinstance(wid, SettingsModeButton):
                self.remove_widget(wid)

    # def set_buttons_colour(self, wid, colour):
    #     print('iiiiiiiiiiiiiiiiiiiiii')
    #     for button in self.settings_sections_buttons:
    #         print('>>>>>>>>>>>', colour)
    #         button.master_colour = colour

class SettingsWithCirclebar(Settings):
    def __init__(self, *args, **kwargs):
        self.interface_cls = InterfaceWithCirclebar
        super(SettingsWithCirclebar, self).__init__(*args, **kwargs)

        with self.canvas.before:
            Color(*App.get_running_app().foreground_colour)
            self.background = Rectangle(size=App.get_running_app().root.size,
                                        pos=App.get_running_app().root.pos)

        App.get_running_app().root.bind(size=self.set_size,
                                        pos=self.set_pos)

    def set_size(self, wid, size):
        self.background.size = size

    def set_pos(self, wid, pos):
        self.background.pos = pos



    # def set_settings_mode_button(self, *args):
    #     self.interface.menu.ids.settings_mode_button.s


class InterfaceWithCirclebar(BoxLayout):
    top_bar = ObjectProperty()
    config_type = StringProperty()

    '''See :meth:`InterfaceWithSidebar` for
    information on implementing your own interface class.
    '''

    __events__ = ('on_close',)

    menu = ObjectProperty()
    '''(internal) A reference to the sidebar menu widget.

    :attr:`menu` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    content = ObjectProperty()
    '''(internal) A reference to the panel display widget (a
    :class:`MyContentPanel`).

    :attr:`menu` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    '''

    def __init__(self, *args, **kwargs):
        super(InterfaceWithCirclebar, self).__init__(*args, **kwargs)

        self.orientation = 'vertical'

        self.top_bar = None
        self.menu = MenuCirclebar(interface=self, config_type=self.config_type, size_hint_y=0.1)
        self.content = ContentPanel()

        self.add_widget(self.menu)
        self.add_widget(self.content)

        Clock.schedule_once(self.bind_buttons)

    # def on_top_bar(self, *args):
    #     self.top_bar.ids.settings_button.bind(
    #         on_release=lambda j: self.dispatch('on_close'))
    #     Clock.schedule_once(self.bind_buttons)
    #     self.top_bar.ids.screen_change_spinner.bind(
    #         on_release=lambda j: self.dispatch('on_close'))
    #     Clock.schedule_once(self.bind_buttons)

    def get_current(self):
        universal_menu_section_button_list = ToggleButton.get_widgets('menu_section')
        universal_down_list = [button for button in universal_menu_section_button_list if
                               button.state == 'down' and button.config_type == self.config_type]
        button = universal_down_list[0]
        return button.uid

    def set_current(self, uid, *args):
        self.content.current_uid = uid

    def bind_buttons(self, *args):
        for button in self.menu.children:
            button.bind(on_release=partial(self.set_current, button.uid))

    def add_panel(self, panel, name, uid):
        '''This method is used by Settings to add new panels for possible
        display. Any replacement for MyContentPanel *must* implement
        this method.

        :Parameters:
            `panel`: :class:`SettingsPanel`
                It should be stored and the interface should provide a way to
                switch between panels.
            `name`:
                The name of the panel as a string. It may be used to represent
                the panel but may not be unique.
            `uid`:
                A unique int identifying the panel. It should be used to
                identify and switch between panels.

        '''

        self.content.add_panel(panel, name, uid)
        self.menu.add_item(name, uid)

    def remove_panel(self):
        pass

    def clear_panels(self):
        self.content.clear_panels()
        self.menu.clear_items()

    def on_close(self, *args):
        pass


class MenuSpinner(BoxLayout):
    '''The menu class used by :class:`SettingsWithSpinner`. It provides a
    sidebar with an entry for each settings panel.

    This widget is considered internal and is not documented. See
    :class:`MenuSidebar` for information on menus and creating your own menu
    class.

    '''
    selected_uid = NumericProperty(0)
    close_button = ObjectProperty(0)
    spinner = ObjectProperty()
    panel_names = DictProperty({})
    spinner_text = StringProperty()
    close_button = ObjectProperty()

    def add_item(self, name, uid):
        values = self.spinner.values
        if name in values:
            i = 2
            while name + ' {}'.format(i) in values:
                i += 1
            name = name + ' {}'.format(i)
        self.panel_names[name] = uid
        self.spinner.values.append(name)
        if not self.spinner.text:
            self.spinner.text = name

    def on_spinner_text(self, *args):
        text = self.spinner_text
        self.selected_uid = self.panel_names[text]


class MenuSidebar(FloatLayout):
    '''The menu used by :class:`InterfaceWithSidebar`. It provides a
    sidebar with an entry for each settings panel, which the user may
    click to select.

    '''

    selected_uid = NumericProperty(0)
    '''The uid of the currently selected panel. This may be used to switch
    between displayed panels, e.g. by binding it to the
    :attr:`~ContentPanel.current_uid` of a :class:`ContentPanel`.

    :attr:`selected_uid` is a
    :class:`~kivy.properties.NumericProperty` and defaults to 0.

    '''

    buttons_layout = ObjectProperty(None)
    '''(internal) Reference to the GridLayout that contains individual
    settings panel menu buttons.

    :attr:`buttons_layout` is an
    :class:`~kivy.properties.ObjectProperty` and defaults to None.

    '''

    close_button = ObjectProperty(None)
    '''(internal) Reference to the widget's Close button.

    :attr:`buttons_layout` is an
    :class:`~kivy.properties.ObjectProperty` and defaults to None.

    '''

    def add_item(self, name, uid):
        '''This method is used to add new panels to the menu.

        :Parameters:
            `name`:
                The name (a string) of the panel. It should be used
                to represent the panel in the menu.
            `uid`:
                The name (an int) of the panel. It should be used internally
                to represent the panel and used to set self.selected_uid when
                the panel is changed.

        '''

        label = SettingSidebarLabel(text=name, uid=uid, menu=self)
        if len(self.buttons_layout.children) == 0:
            label.selected = True
        if self.buttons_layout is not None:
            self.buttons_layout.add_widget(label)

    def on_selected_uid(self, *args):
        '''(internal) unselects any currently selected menu buttons, unless
        they represent the current panel.

        '''
        for button in self.buttons_layout.children:
            if button.uid != self.selected_uid:
                button.selected = False


class SettingSidebarLabel(Label):
    # Internal class, not documented.
    selected = BooleanProperty(False)
    uid = NumericProperty(0)
    menu = ObjectProperty(None)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self.selected = True
        self.menu.selected_uid = self.uid


if __name__ == '__main__':
    from kivy.app import App


    class SettingsApp(App):

        def build(self):
            s = Settings()
            s.add_kivy_panel()
            s.bind(on_close=self.stop)
            return s


    SettingsApp().run()


kv = """
# <SettingItem>:
#     size_hint_y: None
#     height: 70
#     rows: 1
#     canvas:
#         Color:
#             rgba: 47 / 255., 167 / 255., 212 / 255., .1
#         Rectangle:
#             pos: self.x, self.y + 1
#             size: self.size
#         Color:
#             rgb: .2, .2, .2
#         Rectangle:
#             pos: self.x, self.y - 2
#             size: self.width, 1
    # Label:
    #     size_hint_x: .6
    #     id: labellayout
    #     markup: True
    #     text: u'{0}\\n[size=13sp][color=999999]{1}[/color][/size]'.format(root.title or '', root.desc or '')
    #     font_size: '15sp'
    #     text_size: self.size
    #     valign: 'top'

"""

Builder.load_string(kv)
