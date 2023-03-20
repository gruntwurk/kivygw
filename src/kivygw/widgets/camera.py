import logging

from kivy.uix.camera import Camera

from ..utils.cameras import CameraInventory

__all__ = [
    "GWCamera",
]
LOG = logging.getLogger("kivygw")


class GWCamera(Camera):
    '''
    Subclass of the Kivy Camera widget that gets configured according to the given CameraInfo.
    '''
    def __init__(self, **kwargs):
        assert not self.play
        LOG.debug(f"CameraInventory = {str(CameraInventory())}")

        self.camera_info = CameraInventory().active_camera
        assert self.camera_info is not None
        LOG.debug(f"cam = {self.camera_info}")
        self.index = self.camera_info.adjusted_port()
        if self.camera_info.width:
            self.resolution = (self.camera_info.width, self.camera_info.height)
        else:
            self.resolution = (self.camera_info.default_width, self.camera_info.default_height)
        LOG.debug(f"self.resolution = {self.resolution}")
        super().__init__(**kwargs)

    def close(self):
        self.play = False
        self.camera_info.close()
