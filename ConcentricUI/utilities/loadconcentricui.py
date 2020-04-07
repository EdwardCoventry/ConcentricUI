from kivy.utils import platform

if platform == 'win':
    from sys import path

    if platform == 'win':
        contentric_path = "C:\\Users\\Eddco\\\code\\concentricui\\"
        if contentric_path not in path:
            path.append(contentric_path)