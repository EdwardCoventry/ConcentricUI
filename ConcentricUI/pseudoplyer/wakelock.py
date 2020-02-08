from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    View = autoclass('android.view.View')
    Params = autoclass('android.view.WindowManager$LayoutParams')
    autoclass('org.jnius.NativeInvocationHandler')
    from android.runnable import run_on_ui_thread


class WakeLock(object):

    def __init__(self):
        self._wake_lock = False

    #  fixme really you want a property that can be True or False, and the bellow functions are your setters

    @property
    def wake_lock(self):
        return self._wake_lock

    @wake_lock.setter
    def wake_lock(self, state):
        if self._wake_lock != state:
            #  if the state has changed
            self._wake_lock = state
            #  update the property
            #  and set the flag
            if state:
                self.set_wake_lock_flag()
            else:
                self.clear_wake_lock_flag()

    def set_wake_lock_flag(self, *args):
        if platform == 'android':
            self.android_setflag()

    def clear_wake_lock_flag(self, *args):
        if platform == 'android':
            self.android_clearflag()

    if platform == 'android':
        @run_on_ui_thread
        def android_setflag(self):
            try:
                PythonActivity.mActivity.getWindow().addFlags(Params.FLAG_KEEP_SCREEN_ON)
            except Exception as e:
                print('COULD NOT SET WAKE LOCK ON: ', e)

    if platform == 'android':
        @run_on_ui_thread
        def android_clearflag(self):
            try:
                PythonActivity.mActivity.getWindow().clearFlags(Params.FLAG_KEEP_SCREEN_ON)
            except Exception as e:
                print('COULD NOT SET WAKE LOCK OFF:', e)
