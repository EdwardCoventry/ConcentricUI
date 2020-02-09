from kivy.clock import Clock

from ConcentricUI.oblong.oblongtextinput import OblongTextInput

from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout

recycle_item = OblongTextInput

class ConcentricRecycleView(RecycleView):

    def __init__(self, **kwargs):
        super(ConcentricRecycleView, self).__init__(**kwargs)

        #self.data = [{'text': str(x)} for x in range(100)]

        # self.recycle_box_layout = RecycleBoxLayout(default_size=(None, None),
        #                                       default_size_hint=(1, None),
        #                                       size_hint_y=None,
        #                                       height=self.minimum_height,
        #                                       orientation='vertical')

    #     self.recycle_box_layout = RecycleBoxLayout(default_size_hint=(1, None),
    #                                           size_hint_y=None,
    #                                           orientation='vertical')
    #
    #     self.add_widget(self.recycle_box_layout)
    #
    #     Clock.schedule_once(self.on_height, 4)
    #
    #
    # def on_height(self, *args):
    #
    #     self.recycle_box_layout.default_size = (None, self.height/self.number_of_items)
    #
    #     self.recycle_box_layout.height = self.recycle_box_layout.minimum_height

#
# class ConcentricRecycleView(RecycleView):
#     def __init__(self, **kwargs):
#         super(ConcentricRecycleView, self).__init__(**kwargs)
