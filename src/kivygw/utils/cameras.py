import logging
import cv2
import sys

from kivygw.utils.class_utils import Singleton

__all__ = [
    "CameraInfo",
    "CameraInventory",
]

MAX_PORT_NUMBER = 3
LOG = logging.getLogger("gwpy")


@Singleton
class CameraInventory():
    def __init__(self) -> None:
        self._inventory = {}
        self._active_camera_port = None
        self._searched_once = False
        self.find_cameras()

    @property
    def active_camera_port(self):
        if self._active_camera_port is None and len(self._inventory) > 0:
            self._active_camera_port.keys()[0]
        return self._active_camera_port

    @active_camera_port.setter
    def active_camera_port(self, value):
        if value not in self._inventory.keys():
            raise IndexError(f'{value} is not a valid camera port number.')
        self._active_camera_port = value

    @property
    def active_camera(self):
        if self._active_camera_port is None or self._active_camera_port not in self._inventory.keys():
            self._active_camera_port = None
            return None
        return self._inventory[self._active_camera_port]

    def check_camera(self, port, width=0, height=0) -> bool:
        """
        Adds the specified camera port to the inventory, if it's not already
        in the inventory and such a camera exists.

        NOTE: If this camera is added and no active port has been set yet, then
        this one will be set to be the active port.
        """
        if port in self._inventory.keys():
            return self._inventory[port] is not None
        cam = CameraInfo(port, width, height)
        if cam.test_open():
            self._inventory[port] = cam
            if self._active_camera_port is None:
                self._active_camera_port = port
            return True
        self._inventory[port] = None
        return False

    def find_cameras(self, max_port_number=MAX_PORT_NUMBER, force=False) -> dict:
        """
        Tests the camera ports and returns a dictionary of the available ports and
        their info.

        :param max_port_number: The highest port number to test. Default is 3.

        :return: A dictionary where the key is the (unadjusted) port number (0-based),
        and the value is an instance of CameraInfo.
        NOTE: The width/height are the CURRENT settings, not nec. the max resolution.

        """
        for port_number in range(max_port_number + 1):
            LOG.debug(f"Inspecting camera port_number = {port_number}")
            self.check_camera(port_number)
        LOG.debug(f"CameraInventory = {self.__str__()}")
        return self._inventory

    def __str__(self):
        results = []
        for port in self._inventory.keys():
            cam = self._inventory[port]
            results.append(f'{port}: {str(cam)}')
        results.append(f"Active port = {self.active_camera_port}")
        return "\n ".join(results)


class CameraInfo():
    def __init__(self, port=0, width=0, height=0) -> None:
        self._port = port
        self._width = width
        self._height = height
        self._default_width = 0
        self._default_height = 0
        self._video_capture = None

    @property
    def port(self):
        """
        The port number for the selected camera. Zero-based. Default is 0.
        """
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    # TODO How do we get the name of the camera device?

    def adjusted_port(self, port=None):
        """
        The adjusted port number for the selected camera. Adjusted means that
        the port number is ammended to specify the driver source (e.g.
        DirectShow on Windows).
        """
        if port is None:
            port = self._port
        if port is None:
            return None
        return port + (cv2.CAP_DSHOW if sys.platform == "win32" else 0)

    @property
    def width(self):
        """
        The resolution width of the selected camera. If not set prior to
        calling open(), then this will be set to the camera's default.
        """
        return self._width

    @property
    def default_width(self):
        """
        Queries the camera for its default resolution width.
        """
        if not self._default_width:
            self.test_open()
        return self._default_width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """
        The resolution height for the selected camera. If not set prior to
        calling open(), then this will be set to the camera's default.
        """
        return self._height

    @property
    def default_height(self):
        """
        Queries the camera for its default resolution height.
        """
        if not self._default_height:
            self.test_open()
        return self._default_height

    @height.setter
    def height(self, value):
        self._height = value

    def is_open(self):
        return self._video_capture and self._video_capture.isOpened()

    def test_open(self) -> bool:
        """
        Tests to see if the camera can be opened.

        NOTE: While we have it open, we remember the default resolution.

        :return: True if it is already open, or can be opened.
        """
        already_open = self.is_open()
        if not already_open:
            self._video_capture = cv2.VideoCapture(self.adjusted_port())
            if not self._video_capture.isOpened():
                return False
        self._default_width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self._default_height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if not already_open:
            self.close()
        return True

    def open(self) -> bool:
        """
        Opens the video capture device, and then either sets or gets the
        resolution. That is, if the height and width properties are set prior
        to calling this method, then those values will be used to set the
        device's resolution. Otherwise, whatever the device's default
        resolution is will be recorded in the height and width properties.

        :return: True if successfully opened.
        """
        # LOG.debug("self.adjusted_port = {}".format(self.adjusted_port()))
        self._video_capture = cv2.VideoCapture(self.adjusted_port())
        if not self._video_capture.isOpened():
            return False
        if self._width:
            self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, float(self._width))
        else:
            self._width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        if self._height:
            self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self._height))
        else:
            self._height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return True

    def is_reading(self):
        """
        :return: True if the camera is turned on. False if the camera is working,
            but not turned on.
        """
        assert self._video_capture is not None
        return self._video_capture.read()[0]

    def close(self):
        return cv2.destroyAllWindows()

    def __str__(self) -> str:
        return f"CameraInfo: port {self.port} ({self.adjusted_port()}), current: {self.width} x {self.height}, default: {self.default_width} x {self.default_height}"


