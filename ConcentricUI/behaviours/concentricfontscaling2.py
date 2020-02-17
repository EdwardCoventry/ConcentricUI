
from weakref import ref

from kivy.uix.behaviors import togglebutton
from kivy.properties import ObjectProperty

class ConcentricFontScaling(object):

    __font_groups = {}

    font_group = ObjectProperty(None, allownone=True)
    '''Group of the button. If `None`, no font_group will be used (the button will be
    independent). If specified, :attr:`font_group` must be a hashable object, like
    a string. Only one button in a font_group can be in a 'down' state.

    :attr:`font_group` is a :class:`~kivy.properties.ObjectProperty` and defaults to
    `None`.
    '''

    def on_font_group(self, *largs):
        font_groups = ConcentricFontScaling.__font_groups
        if self._previous_font_group:
            font_group = font_groups[self._previous_font_group]
            for item in font_group[:]:
                if item() is self:
                    font_group.remove(item)
                    break
        font_group = self._previous_font_group = self.font_group
        if font_group not in font_groups:
            font_groups[font_group] = []
        r = ref(self, ConcentricFontScaling._clear_font_groups)
        font_groups[font_group].append(r)

    def _set_font_group(self, current):
        if self.font_group is None:
            return
        font_group = self.__font_groups[self.font_group]
        for item in font_group[:]:
            widget = item()
            if widget is None:
                font_group.remove(item)
            if widget is current:
                continue
            #widget.font_size = minimum_group_font_size

    @staticmethod
    def _clear_font_groups(wk):
        # auto flush the element when the weak reference have been deleted
        font_groups = ConcentricFontScaling.__font_groups
        for font_group in list(font_groups.values()):
            if wk in font_group:
                font_group.remove(wk)
                break

    @staticmethod
    def get_widgets(font_group_name):
        '''Return a list of the widgets contained in a specific font_group. If the
        font_group doesn't exist, an empty list will be returned.

        .. note::

            Always release the result of this method! Holding a reference to
            any of these widgets can prevent them from being garbage collected.
            If in doubt, do::

                l = ToggleButtonBehavior.get_widgets('myfont_group')
                # do your job
                del l

        .. warning::

            It's possible that some widgets that you have previously
            deleted are still in the list. The garbage collector might need
            to release other objects before flushing them.
        '''
        font_groups = ConcentricFontScaling.__font_groups
        if font_group_name not in font_groups:
            return []
        return [x() for x in font_groups[font_group_name] if x()][:]
