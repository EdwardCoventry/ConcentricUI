
from kivy.utils import platform

if platform == 'android':

    import android

    def request_android_permissions(permissions_list):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        required_permissions = [getattr(Permission, p.upper()) for p in permissions_list]

        # required_permissions = [Permission.INTERNET,
        #                         Permission.BLUETOOTH,
        #                         Permission.ACCESS_COARSE_LOCATION,
        #                         Permission.ACCESS_FINE_LOCATION,
        #                         Permission.READ_EXTERNAL_STORAGE,
        #                         Permission.WRITE_EXTERNAL_STORAGE]

        request_permissions(required_permissions, callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])
else:
    def request_android_permissions(permissions_list):
        print('youre on pc')

class RequestPermissions(object):

    def __init__(self):

        self.request_android_permissions = request_android_permissions
