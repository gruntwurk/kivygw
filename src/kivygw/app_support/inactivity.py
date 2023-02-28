from typing import Callable

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

__all__ = [
    "add_inactivity_timeout",
]


def add_inactivity_timeout(app: App, timeout_handler: Callable, inactivity_minutes=60):
    """
    Sets up an inactivity timeout for the given Kivy app. "Activity" meaning
    a touch (a button click) or a key press.

    IMPORTANT: Call this from within the `build()` method, not `__init__()`.

    This adds a `reset_timeout()` method to the app which can be called
    directly by any other activity that needs to be considered (e.g.
    periodically within a long-running computation, or while accessing an
    external resource).

    Alternatively, call `MY_APP.cancel_timeout()` to disable the timeout on the
    way in to the long-running activity, and then call `MY_APP.reset_timeout()`
    afterwards to re-enable it.

    :param app: The kivy app to enhance.
    :param timeout_handler: The method to call if a timeout occurs.
    :param inactivity_minutes: The timeout length in minutes. Defaults to 60.
    """
    app.inactivity_minutes = inactivity_minutes
    app.reset_event = None

    def cancel_timeout(*args):
        if app.reset_event:
            app.reset_event.cancel()

    def reset_timeout(*args):
        cancel_timeout()
        app.reset_event = Clock.schedule_once(timeout_handler, app.inactivity_minutes * 60)

    app.cancel_timeout = cancel_timeout
    app.reset_timeout = reset_timeout
    reset_timeout()
    Window.bind(on_touch_down=reset_timeout)
    Window.bind(on_key_down=reset_timeout)
