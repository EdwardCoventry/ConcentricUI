from threading import Thread

from ConcentricUI.utilities.killablethread import KillableThread


#  https://stackoverflow.com/questions/14234547/threads-with-decorators
def run_in_thread(fn):
    def run(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t  # <-- this is new!

    return run


def run_in_killable_thread(fn):
    def run(*args, **kwargs):
        t = KillableThread(target=fn, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t  # <-- this is new!

    return run