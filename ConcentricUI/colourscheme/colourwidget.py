""" This is the base for all concentric ui widgets """

from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import AliasProperty, StringProperty, ColorProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import rgba


class MasterColour(object):
    pseudo_bind_master_colour_attribute = StringProperty('foreground_colour', allownone=True)
    _master_colour = ColorProperty()

    def get_master_colour(self):
        """ I could also get it from the shape list, in concentric shapes.
            and for some other widgets this could be self.background_color or even maybe self.color """
        return self._master_colour

    def set_master_colour(self, value, *args):
        """ This function is 'continued' in concentricshapes """

        if value == None:
            return

        if all((True if type(x) == str else False for x in value)):
            colour_attribute_for_master_colour = ''.join(value)
        else:
            colour_attribute_for_master_colour = None
        if colour_attribute_for_master_colour:
            if colour_attribute_for_master_colour[0] == '#':
                self._master_colour = rgba(colour_attribute_for_master_colour)
                self.pseudo_bind_master_colour_attribute = None
            elif hasattr(self, colour_attribute_for_master_colour):
                self.pseudo_bind_master_colour_attribute = colour_attribute_for_master_colour
            else:
                raise Exception("{} doesnt start with a '#' to denote its an rgba value"
                                ", nor is the value found as an attribute of this class {}".format(value, self))
        elif type(value) in (list, tuple, ColorProperty):
            self._master_colour = tuple(value)
            self.pseudo_bind_master_colour_attribute = None
        elif issubclass(type(value), list):
            self._master_colour = tuple(value)
            self.pseudo_bind_master_colour_attribute = None
        else:
            raise Exception("Couldn't set value {} as master colour")

        """ This function is 'continued' in concentricshapes """

        self.do_colour_update()

    def do_colour_update(self, *args):
        pass

    def set_master_to_colour_attribute(self, colour_attribute_for_master_colour, *args):
        self.master_colour = getattr(self, colour_attribute_for_master_colour)

    master_colour = AliasProperty(get_master_colour, set_master_colour)

    def pseudo_bind_master_colour(self, attribute, wid, value):
        if self.pseudo_bind_master_colour_attribute == attribute:
            self.master_colour = value
            self.pass_master_colour_to_children(wid, value)

    """ the bellow function could use a list of widgets to apply the scheme to """

    def pass_master_colour_to_children(self, wid, colour):
        """ this function is expanded on in subclasses of colourwidget """
        pass


# class MasterTextColour(object):
#
#     pseudo_bind_master_text_colour_attribute = StringProperty('', allownone=True)
#     _master_text_colour = ColorProperty()
#
#     def get_master_text_colour(self):
#         """ I could also get it from the shape list, in concentric shapes.
#             and for some other widgets this could be self.background_color or even maybe self.color """
#         return self._master_text_colour
#
#     def set_master_text_colour(self, value):
#         """ This function is 'continued' in concentricshapes """
#
#         if all((True if type(x) == str else False for x in value)):
#             colour_attribute_for_master_text_colour = ''.join(value)
#         else:
#             colour_attribute_for_master_text_colour = None
#         if colour_attribute_for_master_text_colour:
#             if colour_attribute_for_master_text_colour[0] == '#':
#                 self._master_text_colour = rgba(colour_attribute_for_master_text_colour)
#             elif hasattr(self, colour_attribute_for_master_text_colour):
#                 self.pseudo_bind_master_text_colour_attribute = colour_attribute_for_master_text_colour
#             else:
#                 raise Exception("{} doesnt start with a '#' to denote its an rgba value"
#                                 ", nor is the value found as an attribute of this class {}".format(value, self))
#         elif type(value) in (list, tuple, ColorProperty):
#             self._master_text_colour = tuple(value)
#             self.pseudo_bind_master_text_colour_attribute = None
#         elif issubclass(type(value), list):
#             self._master_text_colour = tuple(value)
#             self.pseudo_bind_master_text_colour_attribute = None
#         else:
#             raise Exception("Couldn't set value {} as master_text colour")
#
#         """ This function is 'continued' in concentricshapes """
#
#         self.do_colour_update()
#
#     def do_colour_update(self, *args):
#         pass
#
#     def set_master_text_to_colour_attribute(self, colour_attribute_for_master_text_colour, *args):
#         self.master_text_colour = getattr(self, colour_attribute_for_master_text_colour)
#
#     master_text_colour = AliasProperty(get_master_text_colour, set_master_text_colour)
#
#     def pseudo_bind_master_text_colour(self, attribute, wid, value):
#         if self.pseudo_bind_master_text_colour_attribute == attribute:
#             self.master_text_colour = value
#             self.pass_master_text_colour_to_children(wid, value)
#
#     """ the bellow function could use a list of widgets to apply the scheme to """
#     def pass_master_text_colour_to_children(self, wid, colour):
#         """ this function is expanded on in subclasses of colourwidget """
#         pass
#
# class MasterTrimColour(object):
#
#     pseudo_bind_master_trim_colour_attribute = StringProperty('', allownone=True)
#     _master_trim_colour = ColorProperty()
#
#     def get_master_trim_colour(self):
#         """ I could also get it from the shape list, in concentric shapes.
#             and for some other widgets this could be self.background_color or even maybe self.color """
#         return self._master_trim_colour
#
#     def set_master_trim_colour(self, value):
#         """ This function is 'continued' in concentricshapes """
#
#         if all((True if type(x) == str else False for x in value)):
#             colour_attribute_for_master_trim_colour = ''.join(value)
#         else:
#             colour_attribute_for_master_trim_colour = None
#         if colour_attribute_for_master_trim_colour:
#             if colour_attribute_for_master_trim_colour[0] == '#':
#                 self._master_trim_colour = rgba(colour_attribute_for_master_trim_colour)
#             elif hasattr(self, colour_attribute_for_master_trim_colour):
#                 self.pseudo_bind_master_trim_colour_attribute = colour_attribute_for_master_trim_colour
#             else:
#                 raise Exception("{} doesnt start with a '#' to denote its an rgba value"
#                                 ", nor is the value found as an attribute of this class {}".format(value, self))
#         elif type(value) in (list, tuple, ColorProperty):
#             self._master_trim_colour = tuple(value)
#             self.pseudo_bind_master_trim_colour_attribute = None
#         elif issubclass(type(value), list):
#             self._master_trim_colour = tuple(value)
#             self.pseudo_bind_master_trim_colour_attribute = None
#         else:
#             raise Exception("Couldn't set value {} as master_trim colour")
#
#         """ This function is 'continued' in concentricshapes """
#
#         self.do_colour_update()
#
#     def do_colour_update(self, *args):
#         pass
#
#     def set_master_trim_to_colour_attribute(self, colour_attribute_for_master_trim_colour, *args):
#         self.master_trim_colour = getattr(self, colour_attribute_for_master_trim_colour)
#
#     master_trim_colour = AliasProperty(get_master_trim_colour, set_master_trim_colour)
#
#     def pseudo_bind_master_trim_colour(self, attribute, wid, value):
#         if self.pseudo_bind_master_trim_colour_attribute == attribute:
#             self.master_trim_colour = value
#             self.pass_master_trim_colour_to_children(wid, value)
#
#     """ the bellow function could use a list of widgets to apply the scheme to """
#     def pass_master_trim_colour_to_children(self, wid, colour):
#         """ this function is expanded on in subclasses of colourwidget """
#         pass


class ColourProperties(MasterColour):  # , MasterTextColour, MasterTrimColour):
    background_colour = ColorProperty()
    foreground_colour = ColorProperty()
    trim_colour = ColorProperty()
    text_colour = ColorProperty()


class ColourWidget(Widget, ColourProperties):
    pass

    #  screen shall be the default, but i shall make it be overridden by master colour, or a manual colour list
    colour_scheme = StringProperty('app')
    use_master_colour = StringProperty()

    needs_trim_colour = BooleanProperty(True)
    needs_text_colour = BooleanProperty(True)



    def __init__(self, **kwargs):

        super(ColourWidget, self).__init__(**kwargs)

        Clock.schedule_once(self.do_colour_scheme)

    def do_colour_scheme(self, *args):

        if self.colour_scheme == 'master':
            pass
        elif self.colour_scheme == 'root':
            root = None
            #  fixme come back to this to work out what exactly you want
            self.set_colours_from_widget(widget=root)
        elif self.colour_scheme == 'screen':
            screen = self.get_screen()


            self.set_colours_from_widget(widget=screen)
        elif self.colour_scheme == 'app':

            app = App.get_running_app()

            self.set_colours_from_widget(widget=app)
        elif self.colour_scheme == 'previous':
            widget = self.get_previous(self)
            self.set_colours_from_widget(widget=widget)

        self.set_master_colour(self.master_colour)
        # self.set_master_text_colour(self.master_text_colour)
        # self.set_master_trim_colour(self.master_trim_colour)

    def get_previous(self, *args):

        if hasattr(self, 'widget_walk_starting_point'):
            start = self.widget_walk_starting_point
        else:
            start = self

        for x in start.walk_reverse():
            if issubclass(type(x), ColourWidget):
                return x
        else:
            raise Exception("didnt get a previous widget."
                            "im not about to try to implement this so i'll just leave it at this for now")

    def get_screen(self, *args):

        if hasattr(self, 'widget_walk_starting_point'):
            start = self.widget_walk_starting_point
        else:
            start = self

        for x in start.walk_reverse():
            if issubclass(type(x), Screen):
                return x

    def set_colours_from_widget(self, widget, *args):

        if not widget:
            #  sometimes you just can't get what you want
            return

        self.foreground_colour = widget.foreground_colour
        self.background_colour = widget.background_colour
        self.trim_colour = widget.trim_colour
        self.text_colour = widget.text_colour

        if self.pseudo_bind_master_colour_attribute:
            colour = getattr(self, self.pseudo_bind_master_colour_attribute)
            # self.master_colour = colour
            self.pseudo_bind_master_colour(self.pseudo_bind_master_colour_attribute, self, colour)

        self.bind(foreground_colour=partial(self.pseudo_bind_master_colour, 'foreground_colour'),
                  background_colour=partial(self.pseudo_bind_master_colour, 'background_colour'),
                  trim_colour=partial(self.pseudo_bind_master_colour, 'trim_colour'),
                  text_colour=partial(self.pseudo_bind_master_colour, 'text_colour'),
                  )
        # self.bind(foreground_colour=partial(self.pseudo_bind_master_text_colour, 'foreground_colour'),
        #           background_colour=partial(self.pseudo_bind_master_text_colour, 'background_colour'),
        #           trim_colour=partial(self.pseudo_bind_master_text_colour, 'trim_colour'),
        #           text_colour=partial(self.pseudo_bind_master_text_colour, 'text_colour'),
        #           )
        # self.bind(foreground_colour=partial(self.pseudo_bind_master_trim_colour, 'foreground_colour'),
        #           background_colour=partial(self.pseudo_bind_master_trim_colour, 'background_colour'),
        #           trim_colour=partial(self.pseudo_bind_master_trim_colour, 'trim_colour'),
        #           text_colour=partial(self.pseudo_bind_master_trim_colour, 'text_colour'),
        #           )

    #
    #     # for x in self.walk():
    #     #     if issubclass(type(x), ColourWidget):
    #     #         x.master_colour = colour
    #
    #     for x in self.children:
    #         print(self, 'xxxxxxxxxxxxxxxxxxx', x)
    #         if issubclass(type(x), ColourWidget):
    #             x.master_colour = colour
