
from kivy.uix.boxlayout import BoxLayout

from functools import partial

class ConcentricBoxLayout(BoxLayout):

    def add_widget(self, widget, *args, **kwargs):

        #widget.center = self.center

        self.bind(center=partial(widget.set_center, self.pos))

        # if self.orientation == 'horizontal':
        #     #widget.center_y = self.center_y
        #     self.bind(center=widget.update_shape_list_pos)
        # elif self.orientation == 'vertical':
        #     self.bind(center=widget.update_shape_list_pos)
        #     #widget.center_x = self.center_x



        super(ConcentricBoxLayout, self).add_widget(widget, *args, **kwargs)