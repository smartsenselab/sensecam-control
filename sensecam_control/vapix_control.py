"""
Library for control AXIS PTZ cameras using Vapix
"""
import time
import logging
import sys
import requests
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup

logging.basicConfig(filename='vapix.log', filemode='w', level=logging.DEBUG)
logging.info('Started')

# pylint: disable=R0904


class CameraControl:
    """
    Module for control cameras AXIS using Vapix
    """

    def __init__(self, ip, user, password):
        self.__cam_ip = ip
        self.__cam_user = user
        self.__cam_password = password

    @staticmethod
    def __merge_dicts(*dict_args) -> dict:
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts

        Args:
            *dict_args: argument dictionary

        Returns:
            Return a merged dictionary
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def _camera_command(self, payload: dict):
        """
        Function used to send commands to the camera
        Args:
            payload: argument dictionary for camera control

        Returns:
            Returns the response from the device to the command sent

        """
        logging.info('camera_command(%s)', payload)

        base_q_args = {
            'camera': 1,
            'html': 'no',
            'timestamp': int(time.time())
        }

        payload2 = CameraControl.__merge_dicts(payload, base_q_args)

        url = 'http://' + self.__cam_ip + '/axis-cgi/com/ptz.cgi'

        resp = requests.get(url, auth=HTTPDigestAuth(self.__cam_user, self.__cam_password),
                            params=payload2)

        if (resp.status_code != 200) and (resp.status_code != 204):
            soup = BeautifulSoup(resp.text, features="lxml")
            logging.error('%s', soup.get_text())
            if resp.status_code == 401:
                sys.exit(1)

        return resp

    def absolute_move(self, pan: float = None, tilt: float = None, zoom: int = None,
                      speed: int = None):
        """
        Operation to move pan, tilt or zoom to a absolute destination.

        Args:
            pan: pans the device relative to the (0,0) position.
            tilt: tilts the device relative to the (0,0) position.
            zoom: zooms the device n steps.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent.

        """
        return self._camera_command({'pan': pan, 'tilt': tilt, 'zoom': zoom, 'speed': speed})

    def continuous_move(self, pan: int = None, tilt: int = None, zoom: int = None):
        """
        Operation for continuous Pan/Tilt and Zoom movements.

        Args:
            pan: speed of movement of Pan.
            tilt: speed of movement of Tilt.
            zoom: speed of movement of Zoom.

        Returns:
            Returns the response from the device to the command sent.

        """
        pan_tilt = str(pan) + "," + str(tilt)
        return self._camera_command({'continuouspantiltmove': pan_tilt, 'continuouszoommove': zoom})

    def relative_move(self, pan: float = None, tilt: float = None, zoom: int = None,
                      speed: int = None):
        """
        Operation for Relative Pan/Tilt and Zoom Move.

        Args:
            pan: pans the device n degrees relative to the current position.
            tilt: tilts the device n degrees relative to the current position.
            zoom: zooms the device n steps relative to the current position.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent.

        """
        return self._camera_command({'rpan': pan, 'rtilt': tilt, 'rzoom': zoom, 'speed': speed})

    def stop_move(self):
        """
        Operation to stop ongoing pan, tilt and zoom movements of absolute relative and
        continuous type

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'continuouspantiltmove': '0,0', 'continuouszoommove': 0})

    def center_move(self, pos_x: int = None, pos_y: int = None, speed: int = None):
        """
        Used to send the coordinates for the point in the image where the user clicked. This
        information is then used by the server to calculate the pan/tilt move required to
        (approximately) center the clicked point.

        Args:
            pos_x: value of the X coordinate.
            pos_y: value of the Y coordinate.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        pan_tilt = str(pos_x) + "," + str(pos_y)
        return self._camera_command({'center': pan_tilt, 'speed': speed})

    def area_zoom(self, pos_x: int = None, pos_y: int = None, zoom: int = None,
                  speed: int = None):
        """
        Centers on positions x,y (like the center command) and zooms by a factor of z/100.

        Args:
            pos_x: value of the X coordinate.
            pos_y: value of the Y coordinate.
            zoom: zooms by a factor.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        xyzoom = str(pos_x) + "," + str(pos_y) + "," + str(zoom)
        return self._camera_command({'areazoom': xyzoom, 'speed': speed})

    def move(self, position: str = None, speed: float = None):
        """
        Moves the device 5 degrees in the specified direction.

        Args:
            position: position to move. (home, up, down, left, right, upleft, upright, downleft...)
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'move': str(position), 'speed': speed})

    def go_home_position(self, speed: int = None):
        """
        Operation to move the PTZ device to it's "home" position.

        Args:
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'move': 'home', 'speed': speed})

    def get_ptz(self):
        """
        Operation to request PTZ status.

        Returns:
            Returns a tuple with the position of the camera (P, T, Z)

        """
        resp = self._camera_command({'query': 'position'})
        pan = float(resp.text.split()[0].split('=')[1])
        tilt = float(resp.text.split()[1].split('=')[1])
        zoom = float(resp.text.split()[2].split('=')[1])
        ptz_list = (pan, tilt, zoom)

        return ptz_list

    def go_to_server_preset_name(self, name: str = None, speed: int = None):
        """
        Move to the position associated with the preset on server.

        Args:
            name: name of preset position server.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'gotoserverpresetname': name, 'speed': speed})

    def go_to_server_preset_no(self, number: int = None, speed: int = None):
        """
        Move to the position associated with the specified preset position number.

        Args:
            number: number of preset position server.
            speed: speed move camera.

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'gotoserverpresetno': number, 'speed': speed})

    def go_to_device_preset(self, preset_pos: int = None, speed: int = None):
        """
        Bypasses the presetpos interface and tells the device to go directly to the preset
        position number stored in the device, where the is a device-specific preset position number.

        Args:
            preset_pos: number of preset position device
            speed: speed move camera

        Returns:
            Returns the response from the device to the command sent

        """
        return self._camera_command({'gotodevicepreset': preset_pos, 'speed': speed})

    def list_preset_device(self):
        """
        List the presets positions stored in the device.

        Returns:
            Returns the list of presets positions stored on the device.

        """
        return self._camera_command({'query': 'presetposcam'})

    def list_all_preset(self):
        """
        List all available presets position.

        Returns:
            Returns the list of all presets positions.

        """
        resp = self._camera_command({'query': 'presetposall'})
        soup = BeautifulSoup(resp.text, features="lxml")
        resp_presets = soup.text.split('\n')
        presets = []

        for i in range(1, len(resp_presets)-1):
            preset = resp_presets[i].split("=")
            presets.append((int(preset[0].split('presetposno')[1]), preset[1].rstrip('\r')))

        return presets

    def set_speed(self, speed: int = None):
        """
        Sets the head speed of the device that is connected to the specified camera.
        Args:
            speed: speed value.

        Returns:
            Returns the response from the device to the command sent.

        """
        return self._camera_command({'speed': speed})

    def get_speed(self):
        """
        Requests the camera's speed of movement.

        Returns:
            Returns the camera's move value.

        """
        resp = self._camera_command({'query': 'speed'})
        return int(resp.text.split()[0].split('=')[1])

    def info_ptz_comands(self):
        """
        Returns a description of available PTZ commands. No PTZ control is performed.

        Returns:
            Success (OK and system log content text) or Failure (error and description).

        """
        resp = self._camera_command({'info': '1'})
        return resp.text
