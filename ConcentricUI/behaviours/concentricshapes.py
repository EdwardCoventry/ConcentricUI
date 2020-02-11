""" Some notes go here """

all__ = ('ConcentricShapes',)

from kivy.clock import Clock

#from kivy.uix.image import Image
from kivy.uix.image import AsyncImage

AsyncImage.anim_delay.defaultvalue = -1


from itertools import zip_longest

from kivy.graphics import Color
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, ListProperty, ReferenceListProperty, \
    AliasProperty, OptionProperty, StringProperty

from ConcentricUI.colourscheme.colourwidget import ColourWidget


class ConcentricShapes(ColourWidget):
    trim = OptionProperty(True, options=(True, False, 'state', 'focus', ('state', 'focus')))

    show_trim = BooleanProperty(False)

    allow_concentric = BooleanProperty(True)

    outer_alpha_store = NumericProperty(allownone=True)

    collision_layer = ObjectProperty('inner')
    collision_ratio = NumericProperty(1)

    image_size = StringProperty('inner')
    image_source = StringProperty()
    button_source = StringProperty()
    image = ObjectProperty()

    outer_shape = ObjectProperty()
    inner_shape = ObjectProperty()

    # def set_image(self, *args):
    #     image = self.image
    #     self.shape_list[-1].source = image

    def on_button_source(self, wid, button_source):
        self.image_source = "textures\\buttons\\{}_button.png".format(button_source)

    def on_show_trim(self, wid, show_trim):

        if not self.colour_instruction_list:
            return
        if self.trim:
            if show_trim:
                self.colour_instruction_list[0].a = self.outer_alpha_store
                self.outer_alpha_store = None
            else:
                self.outer_alpha_store = self.colour_instruction_list[0].a
                self.colour_instruction_list[0].a = 0
        else:
            pass

    """ The most lovely thing about circles is that their width == height
        and even that doesn't do their infinite simplicity justice """

    def get_diameter(self):
        """ This occurs when you want to get the diameter """
        return min(self.height, self.width)

    def set_diameter(self, value):
        """ I'm not too sure what would happen if the diameter was set..
            but i suppose that it would change the size
            meaning that the widget would only take up the size of the circle itself.
            To be seen. """
        self.size = value, value

    diameter = AliasProperty(get_diameter, set_diameter, bind=['width', 'height'])

    shape_list = ListProperty()
    shape_count = NumericProperty()
    shape_size_hint_list = ListProperty([0.5, 0.7, 1])
    shape_colour_list = ListProperty()
    shape_allow_collision_list = ListProperty()
    colour_instruction_list = ListProperty()
    # master_colour = ListProperty()

    #  perhaps i just want to import certain behaviours from concentric shapes, but i dont want to draw an actual shape
    draw_shape_toggle = False

    font_ratio = NumericProperty(0.7)

    def get_shape_dictionary(self):
        """ This occurs when you want to get the shape dictionary """

        #  fixme implement some test for the length of each list
        shape_dictionary_list = [
            {'shape_size_hint': shape_size_hint,
             'shape_colour': shape_colour,
             'shape_allow_collision': shape_allow_collision}
            for shape_size_hint, shape_colour, shape_allow_collision
            in zip_longest(self.shape_size_hint_list, self.shape_colour_list, self.shape_allow_collision_list)
        ]

        sorted_by_size_hint = list(reversed(sorted(shape_dictionary_list, key=lambda k: k['shape_size_hint'])))

        return sorted_by_size_hint

    def set_shape_dictionary(self, value):
        """ This occurs when you want to set the shape dictionary """

        sorted_by_size_hint = list(reversed(sorted(value, key=lambda k: k['shape_size_hint'])))

        self.shape_size_hint_list = [x['shape_size_hint'] for x in sorted_by_size_hint]
        self.shape_colour_list = [x['shape_colour'] for x in sorted_by_size_hint]
        self.shape_allow_collision_list = [x['shape_allow_collision'] for x in sorted_by_size_hint]

    shape_dictionary = AliasProperty(get_shape_dictionary, set_shape_dictionary,
                                     bind=['shape_size_hint_list', 'shape_colour_list'])

    def __init__(self, **kwargs):

        #self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # if 'anchor_x' in kwargs:
        #     kwargs.pop('anchor_x')
        # if 'left' in kwargs:
        #     kwargs.pop('left')
        # if 'anchor_y' in kwargs:
        #     kwargs.pop('anchor_y')
        # if 'top' in kwargs:
        #     kwargs.pop('top')

        super(ConcentricShapes, self).__init__(**kwargs)

        if 'shape_dictionary' in kwargs:
            shape_dictionary = kwargs.pop('shape_dictionary')
            self.shape_dictionary = shape_dictionary
        # else:
        #     self.set_secondary_colours()

        if not self.shape_size_hint_list:
            self.shape_size_hint_list = [1, ]

        """ this will hopefully facilitate setting the master colour to a string,
            declaring a colour attribute from the active colour scheme """
        # try: string_master_colour = ''.join(self.master_colour)
        # except: string_master_colour = None
        # if not string_master_colour:
        #     string_master_colour = 'foreground_colour'

        # print('maaaaybe', string_master_colour)

        # #  do it here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if self.shape_colour_list:
            pass
        # elif string_master_colour:
        #     pass
        # self.master_colour = getattr(self, string_master_colour)
        # elif not self.master_colour:
        #     self.master_colour = self.foreground_colour
        #
        # print('!!!!!!!', string_master_colour, self.master_colour)

        # self.set_secondary_colours()

        self.draw_shapes()
        self.bind(pos=self.update_shape_list_pos,
                  size=Clock.schedule_once(self.update_shape_list_size, 0),
                  master_colour=Clock.schedule_once(self.set_secondary_colours, -1),
                  image_source=self.do_image_source)


        # if self.master_colour and self.use_master_colour not in ('foreground_colour', 'background_colour', 'text_colour', 'trim_colour'):
        #     if self.__class__.__name__ == 'ScreenChangeSpinner':
        #         print('kkkkkkkkkkkkkkkkkkkkkk', 'self.master_colour', self.master_colour, 'self.use_master_colour', self.use_master_colour)
        #     self.set_secondary_colours()

        # if self.trim is True:

    def draw_shapes(self):

        if not self.draw_shape_toggle:
            return

        if not self.shape_dictionary:
            return

        self.colour_instruction_list = []

        with self.canvas.before:
            shape_dictionary = self.shape_dictionary if self.allow_concentric else [self.shape_dictionary[0]]
            for i, dictionary in enumerate(shape_dictionary):

                image_flag = False

                shape_colour = dictionary['shape_colour']
                if not shape_colour:
                    #  placeholder color
                    shape_colour = (1, 1, 1, 1)
                colour_instruction = Color(*shape_colour)
                self.colour_instruction_list.append(colour_instruction)
                shape = self.draw_shape(image_source=False, **dictionary)

                if i == 0:
                    self.outer_shape = shape
                    self.outer_shape_dictionary = dictionary
                elif i == len(shape_dictionary) - 1:
                    self.inner_shape = shape
                    self.inner_shape_dictionary = dictionary

                self.shape_list.append(shape)
        #
        # if self.image_source:
        #     shape = self.draw_image(self.image_source)
        #     self.shape_list.append(shape)
    def do_image_source(self, wid, source, *args):

        if self:
            if not self.image:
                self.image = AsyncImage(source=source)

                self.bind(pos=self.set_image_size_and_pos,
                          size=self.set_image_size_and_pos,
                          trim_colour=self.set_image_colour)

                self.add_widget(self.image)
            else:
                self.image.source = source


    def set_image_size_and_pos(self, *args):
        if self.image:
            if self.image_size == 'inner':
                self.image.size = self.inner_shape.size
                self.image.pos = self.inner_shape.pos
            elif self.image_size == 'outer':
                self.image.size = self.outer_shape.size
                self.image.pos = self.outer_shape.pos
            else:
                raise Exception("shape size {} not recognised."
                                "only 'inner' and 'outer' are supported"
                                .format(self.image_size))

    def set_image_colour(self, wid, colour, *args):


        self.image.color = colour

    # def draw_image(self, source):
    #
    #     print(':@@@@@@@@@@@@@@@@@@@', self.image_source)
    #
    #     if source:
    #
    #         if self.image_size == 'inner':
    #             dictionary = self.inner_shape_dictionary
    #         elif self.image_size == 'outer':
    #             dictionary = self.outer_shape_dictionary
    #         else:
    #             raise Exception("shape size {} not recognised."
    #                             "only 'inner' and 'outer' are supported"
    #                             .format(source))
    #
    #         dictionary['shape_colour'] = self.trim_colour
    #
    #         print('ddddddddd', dictionary)
    #
    #         self.image = self.draw_shape(image_source=source, **dictionary)
    #
    #     self.shape_list.append(self.image)
    #
    #     return self.image

    def draw_shape(self, **kwargs):
        raise Exception("Hey! This class is not meant to be used directly and this method is meant to be overwritten!")


    def set_center(self, center, *args):
        self.center = center
        self.update_shape_list_pos()


    def update_shape_list_pos(self, *args):

        for shape in self.shape_list:
            #  fixme aww i dont get to use an AliasProperty
            #  i believe it may be impossible, as Elipsis doesn't have a center x, center y, etc..
            #  come to think of it that's the very reason that i'm adding it
            pass
            shape.set_center(self.center)

        Clock.schedule_once(self.set_image_size_and_pos, -1)

    def update_shape_list_size(self, *args):
        for shape, size_hint in zip(self.shape_list, self.shape_size_hint_list):
            pass

            shape.set_size(self.size, size_hint)
            shape.set_center(self.center)

        self.update_shape_list_pos()

    def get_inner_shape_width(self):

        if not self.shape_list:
            return None

        return self.shape_list[-1].size[0]

    def set_inner_shape_width(self, value, *args):

        if not self.shape_list:
            return None

        self.shape_list[-1].width = value

    def get_inner_shape_height(self, *args):

        if not self.shape_list:
            return None

        return self.shape_list[-1].size[1]

    def set_inner_shape_height(self, value, *args):

        if not self.shape_list:
            return None

        self.shape_list[-1].height = value

    def get_inner_shape_x(self):

        if not self.shape_list:
            return None

        return self.shape_list[-1].pos[0]

    def set_inner_shape_x(self, value):

        if not self.shape_list:
            return None

        self.shape_list[-1].pos[0] = value

    def get_inner_shape_y(self):

        if not self.shape_list:
            return None

        return self.shape_list[-1].pos[1]

    def set_inner_shape_y(self, value):

        if not self.shape_list:
            return None

        self.shape_list[-1].pos[1] = value

    def get_inner_shape_right(self):

        if not self.shape_list:
            return None

        return self.inner_x + self.inner_width

    def set_inner_shape_right(self, value):

        if not self.shape_list:
            return None

        self.inner_x = value - self.inner_width

    def get_inner_shape_top(self):

        if not self.shape_list:
            return None

        return self.inner_y + self.inner_height

    def set_inner_shape_top(self, value):

        if not self.shape_list:
            return None

        self.inner_y = value - self.inner_height

    inner_width = AliasProperty(get_inner_shape_width, set_inner_shape_width, bind=['size', 'shape_size_hint_list'])
    inner_height = AliasProperty(get_inner_shape_height, set_inner_shape_height, bind=['size', 'shape_size_hint_list'])
    inner_x = AliasProperty(get_inner_shape_x, set_inner_shape_x, bind=['size', 'pos', 'shape_size_hint_list'])
    inner_y = AliasProperty(get_inner_shape_y, set_inner_shape_y, bind=['size', 'pos', 'shape_size_hint_list'])
    inner_right = AliasProperty(get_inner_shape_right, set_inner_shape_right, bind=['inner_x', 'inner_width'])
    inner_top = AliasProperty(get_inner_shape_top, set_inner_shape_top, bind=['inner_y', 'inner_height'])

    inner_size = ReferenceListProperty(inner_width, inner_height)
    inner_pos = ReferenceListProperty(inner_x, inner_y)

    # def to_inner(self, x, y, relative=True):
    #     '''Transform parent coordinates to local coordinates. See
    #     :mod:`~kivy.uix.relativelayout` for details on the coordinate systems.
    #
    #     :Parameters:
    #         `relative`: bool, defaults to False
    #             Change to True if you want to translate coordinates to
    #             relative widget coordinates.
    #     '''
    #     if relative:
    #         return (x - self.inner_x, y - self.inner_y)
    #     return (x, y)

    """ maybe not a great idea but for now i shall just make these functions work for any layer """

    def get_inner_x_at_y(self, y, layer='inner', ratio=None, both_coordinates=False):

        # if layer is not None and ratio is not None:
        #     raise Exception("ratio is for providing a sort of throw away custom sized shape."
        #                     " you cant specify a shape and a ratio!"
        #                     " I suppose you should manually set layer to None in order to use ratio")

        if ratio is None:
            scale_bounds = False
        else:
            scale_bounds = ratio

        if not (type(layer) == int or layer in ('inner', 'outer')):
            raise Exception("layer must be int, or 'inner' or 'outer'. not {}".format(layer))

        if layer == 'inner':
            layer = -1
        elif layer == 'outer':
            layer = 0

        if not self.draw_shape_toggle:
            # if ratio != None:
            #     raise Exception("ratio was specified but draw shape toggle was off. what to do...")
            return self.x

        _, local_y = self.shape_list[layer].to_inner_center(0, y)

        # if ratio is not None:
        #     # print(local_y)
        #     # local_y -= self.center_y
        #     # print(local_y)
        #     local_y *= ratio
        #     # print(local_y)
        #     # local_y += self.center_y
        #     # print(local_y)

        x_at_y = self.shape_list[layer].get_inner_x_at_y(local_y, scale_bounds=scale_bounds)

        if not both_coordinates:
            return x_at_y
        else:
            if x_at_y:
                return -x_at_y, x_at_y
            else:
                return None, None

    def get_inner_y_at_x(self, x, layer='inner', ratio=None, both_coordinates=False):

        if ratio is None:
            scale_bounds = False
        else:
            scale_bounds = ratio

        if not (type(layer) == int or layer in ('inner', 'outer')):
            raise Exception("layer must be int, or 'inner' or 'outer'. not {}".format(layer))

        if layer == 'inner':
            layer = -1
        elif layer == 'outer':
            layer = 0

        if not self.draw_shape_toggle:
            return self.y

        local_x, _ = self.shape_list[layer].to_inner_center(x, 0)

        # if ratio is not None:
        #     #print('========================================')
        #     #local_x -= self.center_x
        #     local_x *= ratio
        #     #local_x += self.center_x
        y_at_x = self.shape_list[layer].get_inner_y_at_x(local_x, scale_bounds=scale_bounds)

        if not both_coordinates:
            return y_at_x
        else:
            if y_at_x:
                return -y_at_x, y_at_x
            else:
                return None, None

    def get_inner_pos_at_pos(self, pos, both_coordinates=False):
        raise Exception('not yet implemented. need to think about this one')

    def get_inner_width_at_y(self, y, layer='inner'):

        if not (type(layer) == int or layer in ('inner', 'outer')):
            raise Exception("layer must be int, or 'inner' or 'outer'. not {}".format(layer))

        if layer == 'inner':
            layer = -1
        elif layer == 'outer':
            layer = 0

        if not self.draw_shape_toggle:
            return self.width

        min_x, max_x = self.get_inner_x_at_y(y, layer=layer, both_coordinates=True)

        if not min_x or not max_x:
            return None
        return max_x - min_x

    def get_inner_height_at_x(self, x, layer='inner'):

        if not (type(layer) == int or layer in ('inner', 'outer')):
            raise Exception("layer must be int, or 'inner' or 'outer'. not {}".format(layer))

        if layer == 'inner':
            layer = -1
        elif layer == 'outer':
            layer = 0

        if not self.draw_shape_toggle:
            return self.height

        min_y, max_y = self.get_inner_y_at_x(x, layer=layer, both_coordinates=True)

        if not min_y or not max_y:
            return None
        return max_y - min_y

    def get_inner_size_at_pos(self, pos, layer='inner'):

        if not (type(layer) == int or layer in ('inner', 'outer')):
            raise Exception("layer must be int, or 'inner' or 'outer'. not {}".format(layer))

        if layer == 'inner':
            layer = -1
        elif layer == 'outer':
            layer = 0

        if not self.draw_shape_toggle:
            return self.size

        x, y = pos

        width = self.get_inner_width_at_y(y, layer=layer)
        height = self.get_inner_height_at_x(x, layer=layer)

        return width, height

    def collide_point(self, x, y, layer=None, ratio=None):

        '''

        Overwritten to actually reflect the shape!

        '''

        if layer is None:
            layer = self.collision_layer

        if ratio is None:
            ratio = self.collision_ratio

        if not self.draw_shape_toggle:
            return super(ConcentricShapes, self).collide_point(x, y)

        local_x, local_y = self.shape_list[-1].to_inner_center(x, y)


        inner_x, inner_right = self.get_inner_x_at_y(y, layer=layer, ratio=ratio, both_coordinates=True)
        inner_top, inner_y = self.get_inner_y_at_x(x, layer=layer, ratio=ratio, both_coordinates=True)

        # print('===============================================')
        # print(inner_x, local_x, inner_right)
        # print(inner_top, local_y, inner_y)
        # print('===============================================')

        if not all((inner_x, inner_right, inner_y, inner_top)):
            return False

        return inner_x <= local_x <= inner_right and inner_top <= local_y <= inner_y

    """ COLOURS """

    # master_colour = ListProperty()

    @staticmethod
    def set_colour_by_size_hint(colour, size_hint, min_size_hint):
        # size_hint_remainder = 1 - size_hint
        # if not size_hint_remainder:
        #     size_hint_remainder = 1

        original_alpha = colour[3] if len(colour) > 3 else None

        colour_scalar = (size_hint - min_size_hint)

        uncapped_colour_list = [x + colour_scalar for x in colour]
        max_colour_value = max(uncapped_colour_list)
        if max_colour_value > 1:
            capped_colour_list = [x / max_colour_value for x in uncapped_colour_list]
            # capped_colour_list = [x if x < 1 else 1 for x in uncapped_colour_list]

            if original_alpha is not None:
                capped_colour_list[3] = original_alpha

            return capped_colour_list

        else:
            return uncapped_colour_list

    def set_secondary_colours(self, *args):

        if not self.master_colour and self.shape_colour_list:
            self.master_colour = self.shape_colour_list[0]

        if self.master_colour and self.shape_list:

            shape_dictionary = self.shape_dictionary
            min_size_hint = min(self.shape_size_hint_list)
            for shape in shape_dictionary:
                base_colour = self.master_colour
                # if i:
                colour_size_hint = shape['shape_size_hint']
                # else:
                #     colour_size_hint = 1
                auto_colour = self.set_colour_by_size_hint(base_colour, colour_size_hint, min_size_hint)


                shape['shape_colour'] = auto_colour

            self.shape_dictionary = shape_dictionary

            self.get_shape_dictionary()

            #if self.needs_text_colour:
            if True:
                #  not my favourite bit of code, but as colour property will fill in as [1, 1, 1, 1], what else can i do
                self.text_colour = shape_dictionary[0]['shape_colour']
            #if self.needs_trim_colour:
            if True:
                self.trim_colour = shape_dictionary[0]['shape_colour']
                #self.set_image_colour(self.trim_colour)

        # for shape, colour in zip(self.shape_list, self.shape_colour_list):
        #     shape.update_colour(colour)

        # for colour_instruction, colour in zip(self.colour_instruction_list, self.shape_colour_list):
        #     colour_instruction.rgba = colour

        return

    # def get_master_colour(self):
    #     print('this is super good hahah')
    #     super(self, ConcentricShapes).get_master_colour()
    #
    #     self.set_secondary_colours()

    def on_shape_colour_list(self, wid, shape_colour_list):
        if self.colour_instruction_list:
            for instruction, colour in zip(self.colour_instruction_list, shape_colour_list):
                instruction.rgba = colour
            if not self.show_trim and self.allow_concentric:
                self.outer_alpha_store = instruction.a
                self.colour_instruction_list[0].a = 0
            # self.colour_instruction_list[0].a = 1 if self.show_trim else 0

    # def on_master_colour(self, wid=None, master_colour=None):
    #     if master_colour:
    #         #self.set_secondary_colours(master_colour)
    #         if self.shape_list:
    #             self.set_secondary_colours(master_colour)
    #
    # def on_shape_colour_list(self, wid, colour_list):
    #     if self.colour_instruction_list:
    #         for colour, instruction in zip(colour_list, self.colour_instruction_list):
    #             if colour and instruction:
    #                 instruction.rgba = colour

    def set_colours_from_widget(self, widget):
        super(ConcentricShapes, self).set_colours_from_widget(widget)
        # self.master_colour = self.foreground_colour
        # self.shape_colour_list[0] = self.trim_colour

    #
    # def set_colour_scheme(self):
    #     #  super will set master colour to foreground, and get background, trim and text colours
    #     super(ConcentricShapes, self).set_colour_scheme()
    #
    #     self.shape_colour_list[-1] = self.trim_colour

    def do_colour_update(self, *args):
        super(ConcentricShapes, self).do_colour_update(*args)
        self.set_secondary_colours()

    def get_inner_colour(self):

        if not self.shape_colour_list:
            return None

        return self.shape_colour_list[0]

    def set_inner_colour(self, value):

        if not self.shape_colour_list:
            return None

        self.shape_colour_list[0] = value
        self.set_secondary_colours()

    inner_colour = AliasProperty(get_inner_colour, set_inner_colour, bind=['shape_colour_list'])

    def get_outer_colour(self, *args):

        if not self.shape_colour_list:
            return None

        if self.trim:
            return self.trim_colour
        else:
            return self.shape_colour_list[0]

        # print(self, self.trim, self.show_trim, '*****'*60)
        #
        # if not self.shape_colour_list:
        #     return None
        #
        # # if self.show_trim:
        # #     outer_colour = self.trim_colour
        # # else:
        # #     outer_colour = (0, 0, 0, 0)
        #
        # if self.trim and self.show_trim:
        #     """ this wants the trim badly """
        #     print('not so sure about this one', self.trim_colour)
        #     outer_colour = self.trim_colour
        #
        # elif self.trim and not self.show_trim:
        #     """ this wants the trim, but trim is denied to it. hence nothing shows """
        #     print('eegehhehehehhehhheh', self)
        #     outer_colour = (0, 0, 0, 0)
        #
        # elif not self.trim and self.show_trim:
        #     """ this is a weird one. it doesnt want the trim, but it's told to have it.
        #         i think it should just be ignored """
        #     #raise Exception("this shouldnt really happen? or if it does try to implement what you want")
        #     print('oh yeah this occurs!', self.shape_colour_list[-1])
        #     outer_colour = self.trim_colour
        #
        #
        # if not self.trim and not self.show_trim:
        #     """ this just doesnt care about or want trim """
        #     print('this would make sense', self.shape_colour_list[-1])
        #     outer_colour = self.shape_colour_list[0]
        #     outer_colour = (0, 0, 0, 0)
        #
        # if self.colour_instruction_list and outer_colour:
        #     self.colour_instruction_list[0].rgba = outer_colour

        return outer_colour

    def set_outer_colour(self, value):

        if not self.shape_colour_list:
            return None

        self.shape_colour_list[0] = value
        self.set_secondary_colours()

    outer_colour = AliasProperty(get_outer_colour, set_outer_colour,
                                 bind=['shape_colour_list', 'colour_instruction_list', 'trim'])