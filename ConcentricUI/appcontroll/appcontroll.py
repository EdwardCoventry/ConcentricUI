from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast


def close_app(*args):
    App.get_running_app().stop()
    if platform is not 'android':
        Window.close()


def minimise_app(*args):
    if platform is 'android':
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        intent = Intent(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_HOME)
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)
    else:
        Window.minimize()
    return True
