from kivy.app import App
from kivy.core.window import Window

from kivygw.app_support.dialogs import ask_user_yes_no

__all__ = [
    'add_confirm_exit',
]


def add_confirm_exit(app: App):
    """
    Sets up the app to have the user confirm closing the app.

    :param app: The kivy app to enhance.
    """
    def prevent_close(*args):
        ask_user_yes_no('Are you sure you want to close the app?', on_yes=app.shutdown)
        return True  # prevent closing immediately; wait for the shutdown method to stop the app if confirmed

    def shutdown(yes_i_am_sure=True):
        if yes_i_am_sure:
            app.stop()

    app.prevent_close = prevent_close
    app.shutdown = shutdown
    Window.bind(on_request_close=app.prevent_close)
