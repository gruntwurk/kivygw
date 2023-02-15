import logging

from kivy.uix.camera import Camera

from ..utils.cameras import CameraInfo
from ..app_support.dialogs import inform_user

LOG = logging.getLogger("kivygw")


class GWCamera(Camera):
    '''
    Subclass of the Kivy Camera widget that automatically gets configured
    according to the CameraInfo() singleton.
    '''
    def __init__(self, **kwargs):
        assert not self.play
        cam = CameraInfo()
        LOG.debug(f"cam = {cam}")
        self.index = cam.adjusted_port
        if cam.width:
            self.resolution = (cam.width, cam.height)
        LOG.debug(f"self.resolution = {self.resolution}")
        try:
            super().__init__(**kwargs)
        except AttributeError:
            if cam.port != 0:
                orig_port = cam.port
                cam.port = 0
                self.index = cam.adjusted_port
                try:
                    super().__init__(**kwargs)
                    inform_user(f"Camera #{orig_port} was not found. Using camera #0.")
                except AttributeError as e:
                    raise SystemError("Unable to initialize any camera.") from e

    def close(self):
        self.play = False
        CameraInfo().close()


__all__ = [
    "GWCamera",
]