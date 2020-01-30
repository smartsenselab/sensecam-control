"""
Library for configuring AXIS cameras
"""
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth


# pylint: disable= #R0904
# pylint: disable= #R0914


class CameraConfiguration:
    """
    Module for configuration cameras AXIS
    """

    def __init__(self, ip, user, password):
        self.cam_ip = ip
        self.cam_user = user
        self.cam_password = password

    def factory_reset_default(self):  # 5.1.3
        """
        Reload factory default. All parameters except Network.BootProto, Network.IPAddress,
        Network. SubnetMask, Network.Broadcast and Network.DefaultRouter are set to their factory
        default values.

        Returns:
            Success (OK) or Failure (Settings or syntax are probably incorrect).


        """
        url = 'http://' + self.cam_ip + '/axis-cgi/factorydefault.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def hard_factory_reset_default(self):  # 5.1.4
        """
        Reload factory default. All parameters are set to their factory default value.

        Returns:
            Success (OK) or Failure (error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/hardfactorydefault.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def restart_server(self):  # 5.1.6
        """
        Restart server.

        Returns:
            Success (OK) or Failure (error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/restart.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_server_report(self):  # 5.1.7
        """
        This CGI request generates and returns a server report. This report is useful as an
        input when requesting support. The report includes product information, parameter
        settings and system logs.

        Returns:
            Success (OK and server report content text) or Failure (error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/serverreport.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_system_log(self):  # 5.1.8.1
        """
        Retrieve system log information. The level of information included in the log is set
        in the Log. System parameter group.

        Returns:
            Success (OK and system log content text) or Failure (error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/systemlog.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_system_access_log(self):  # 5.1.8.2
        """
        Retrieve client access log information. The level of information included in the log
        is set in the Log.Access parameter group.

        Returns:
            Success (OK and access log content text) or Failure (error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/accesslog.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_date_and_time(self):  # 5.1.9.1
        """
        Get the system date and time.

        Returns:
            Success (OK and time and date content text) or Failure (error and description).
                example: <month> <day>, <year> <hour>:<minute>:<second>
                Error example: Request failed: <error message>

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/date.cgi?action=get'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def set_date(self, year_date: int = None, month_date: int = None,
                 day_date: int = None):  # 5.1.9.2
        """
        Change the system date.

        Args:
            year_date: current year.
            month_date: current month.
            day_date: current day.

        Returns:
            Success (OK) or Failure (Request failed: <error message>).

        """
        payload = {
            'action': 'set',
            'year': year_date,
            'month': month_date,
            'day': day_date
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/date.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def set_time(self, hour: int = None, minute: int = None, second: int = None,
                 timezone: str = None):  # 5.1.9.2
        """
        Change the system time.

        Args:
            hour: current hour.
            minute: current minute.
            second: current second.
            timezone: specifies the time zone that the new date and/or time is given in. The camera
            translates the time into local time using whichever time zone has been specified through
            the web configuration.

        Returns:
            Success (OK) or Failure (Request failed: <error message>).

        """
        payload = {
            'action': 'set',
            'hour': hour,
            'minute': minute,
            'second': second,
            'timezone': timezone
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/date.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_image_size(self):  # 5.2.1
        """
        Retrieve the actual image size with default image settings or with given parameters.

        Returns:
            Success (OK and image size content text) or Failure (Error and description).
                example:
                    image width = <value>
                    image height = <value>
        """
        url = 'http://' + self.cam_ip + '/axis-cgi/imagesize.cgi?camera=1'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            # vector = resp.text.split()
            # print(vector[3], 'x', vector[7])
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_video_status(self, camera_status: int = None):  # 5.2.2
        """
        Video encoders only. Check the status of one or more video sources.

        Args:
            camera_status: video source

        Returns:
            Success (OK and video status content text) or Failure (Error and description).
            example:
                Video 1 = <information>
        """
        payload = {
            'status': camera_status
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/videostatus.cgi?'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def get_bitmap_request(self, resolution: str = None, camera: str = None,
                           square_pixel: int = None):  # 5.2.3.1
        """
        Request a bitmap image.

        Args:
            resolution: resolution of the returned image. Check the product’s Release notes for
            supported resolutions.
            camera: select a video source or the quad stream.
            square_pixel: enable/disable square pixel correction. Applies only to video encoders.

        Returns:
            Success ('image save' and save the image in the file folder) or Failure (Error and
            description).

        """
        payload = {
            'resolution': resolution,
            'camera': camera,
            'square_pixel': square_pixel
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/bitmap/image.bmp'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            now = datetime.datetime.now()
            with open(str(now.strftime("%d-%m-%Y_%Hh%Mm%Ss")) + ".bmp", 'wb') as var:
                var.write(resp.content)
            return str('Image saved')

        text = str(resp)
        text += str(resp.text)
        return text

    def get_jpeg_request(self, resolution: str = None, camera: str = None,
                         square_pixel: int = None, compression: int = None,
                         clock: int = None, date: int = None, text: int = None,
                         text_string: str = None, text_color: str = None,
                         text_background_color: str = None, rotation: int = None,
                         text_position: str = None, overlay_image: int = None,
                         overlay_position: str = None):  # 5.2.4.1
        """
        The requests specified in the JPEG/MJPG section are supported by those video products
        that use JPEG and MJPG encoding.

        Args:
            resolution: Resolution of the returned image. Check the product’s Release notes.
            camera: Selects the source camera or the quad stream.
            square_pixel: Enable/disable square pixel correction. Applies only to video encoders.
            compression: Adjusts the compression level of the image.
            clock: Shows/hides the time stamp. (0 = hide, 1 = show)
            date: Shows/hides the date. (0 = hide, 1 = show)
            text: Shows/hides the text. (0 = hide, 1 = show)
            text_string: The text shown in the image, the string must be URL encoded.
            text_color: The color of the text shown in the image. (black, white)
            text_background_color: The color of the text background shown in the image.
            (black, white, transparent, semitransparent)
            rotation: Rotate the image clockwise.
            text_position: The position of the string shown in the image. (top, bottom)
            overlay_image: Enable/disable overlay image.(0 = disable, 1 = enable)
            overlay_position:The x and y coordinates defining the position of the overlay image.
            (<int>x<int>)

        Returns:
            Success ('image save' and save the image in the file folder) or Failure (Error and
            description).

        """
        payload = {
            'resolution': resolution,
            'camera': camera,
            'square_pixel': square_pixel,
            'compression': compression,
            'clock': clock,
            'date': date,
            'text': text,
            'text_string': text_string,
            'text_color': text_color,
            'text_background_color': text_background_color,
            'rotation': rotation,
            'text_position': text_position,
            'overlay_image': overlay_image,
            'overlay_position': overlay_position
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/jpg/image.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            now = datetime.datetime.now()
            with open(str(now.strftime("%d-%m-%Y_%Hh%Mm%Ss")) + ".jpg", 'wb') as var:
                var.write(resp.content)
            return str('Image saved')

        text = str(resp)
        text += str(resp.text)
        return text

    def get_type_camera(self):
        """
        Request type camera.

        Returns:
            return type camera, Network camera or ptz camera

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi?action=list&group=Brand.ProdType'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            vector = resp.text.split('=')
            return vector[1].replace('\r', '')

        text = str(resp)
        text += str(resp.text)
        return text

    def get_dynamic_text_overlay(self):  # 5.2.5.1
        """
        Get dynamic text overlay in the image.

        Returns:
            Success (dynamic text overlay) or Failure (Error and description).

        """
        url = 'http://' + self.cam_ip + '/axis-cgi/dynamicoverlay.cgi?action=gettext'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password))

        if resp.status_code == 200:
            return resp.text

        text = str(resp)
        text += str(resp.text)
        return text

    def set_dynamic_text_overlay(self, text: str = None, camera: str = None):  # 5.2.5.1
        """
        Set dynamic text overlay in the image.

        Args:
            text: text to set overlay
            camera: select video source or the quad stream. ( default: default camera)

        Returns:
            OK if the camera set text overlay or error and description

        """
        payload = {
            'action': 'settext',
            'text': text,
            'camera': camera
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/dynamicoverlay.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def check_profile(self, name: str = None):  # 0
        """
        Check if the profile exists

        Args:
            name: profile name

        Returns:
            Return 1 or 0

        """
        payload = {
            'action': 'list',
            'group': 'root.StreamProfile'
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        text2 = resp.text.split('\n')
        if resp.status_code == 200:
            for i, _ in enumerate(text2):
                text3 = text2[i].split('Name=')
                if len(text3) > 1 and text3[1] == name:
                    return 1
            return 0

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def create_profile(self, name: str, *, resolution: str = None, video_codec: str = None,
                       fps: int = None, compression: int = None, h264_profile: str = None,
                       gop: int = None, bitrate: int = None, bitrate_priority: str = None):
        """
        Create stream profile.

        Args:
            name: profile name (str)
            resolution: resolution. (str : "1920x1080")
            video_codec: video codec. (str : "h264")
            fps: frame rate.
            compression: axis compression.
            h264_profile: profile h264. (str: "high")
            gop: Group of pictures.
            bitrate: video bitrate.
            bitrate_priority: video bitrate priority.

        Returns:
            Profile code and OK if the profile create or error and description.

        """
        if self.check_profile(name):
            return name + ' already exists. Remove the previous profile or change the name of ' \
                   'the profile to be created.'

        params = {
            'resolution': resolution,
            'videocodec': video_codec,
            'fps': fps,
            'compression': compression,
            'h264profile': h264_profile,
            'videokeyframeinterval': gop,
            'videobitrate': bitrate,
            'videobitratepriority': bitrate_priority
        }

        params_filtred = {key: value for (key, value) in params.items() if value is not None}
        text_params = urllib.parse.urlencode(params_filtred)
        payload = {
            'action': 'add',
            'template': 'streamprofile',
            'group': 'StreamProfile',
            'StreamProfile.S.Name': name,
            'StreamProfile.S.Parameters': text_params
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        soup = BeautifulSoup(resp.text, features="lxml")
        if resp.status_code == 200:
            return soup.body.get_text()

        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def create_user(self, user: str, password: str, sgroup: str, *, group: str = 'users', comment: str = None):
        # 5.1.2
        """
        Create user.

        Args:
            user: user name
            password: password
            group: An existing primary group name of the account.
            sgroup: security group (admin, operator, viewer)
            comment: user description

        Returns:
            Success (Created account <account name>) or Failure (Error and description).

        """
        if self.check_user(user):
            return user + ' already exists.'

        if sgroup == 'admin':
            sgroup = 'admin:operator:viewer:ptz'
        elif sgroup == 'operator':
            sgroup = 'operator:viewer:ptz'
        elif sgroup == 'ptz':
            sgroup = 'viewer:ptz'

        payload = {
            'action': 'add',
            'user': user,
            'pwd': password,
            'grp': group,
            'sgrp': sgroup,
            'comment': comment
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/pwdgrp.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        soup = BeautifulSoup(resp.text, features="lxml")
        if resp.status_code == 200:
            return soup.body.get_text()

        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def update_user(self, user: str, *, password: str = None, group: str = 'users',
                    sgroup: str = None, comment: str = None):  # 5.1.2
        """
        Update user params.

        Args:
            user: user name
            password: new password or current password to change others params.
            group: An existing primary group name of the account.
            sgroup: security group. (admin, operator, viewer)
            comment: user description.

        Returns:
            Success (OK) or Failure (Error and description).

        """
        if not self.check_user(user):
            return user + ' does not exists.'

        if sgroup == 'admin':
            sgroup = 'admin:operator:viewer:ptz'
        elif sgroup == 'operator':
            sgroup = 'operator:viewer:ptz'
        elif sgroup == 'ptz':
            sgroup = 'viewer:ptz'

        payload = {
            'action': 'update',
            'user': user,
            'pwd': password,
            'grp': group,
            'sgrp': sgroup,
            'comment': comment
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/pwdgrp.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        soup = BeautifulSoup(resp.text, features="lxml")
        if resp.status_code == 200:
            return soup.body.get_text()

        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def remove_user(self, user: str):  # 5.1.2
        """
        Remove user.
        Args:
            user:  user name

        Returns:
            Success (OK) or Failure (Error and description).
        """
        if not self.check_user(user):
            return user + 'does not exists.'

        payload = {
            'action': 'remove',
            'user': user
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/pwdgrp.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        soup = BeautifulSoup(resp.text, features="lxml")
        if resp.status_code == 200:
            return soup.body.get_text()

        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def check_user(self, name: str):  # 0
        """
        Check if user exists
        Args:
            name: user name

        Returns:
            Success (0 = doesn't exist, 1 exist) or Failure (Error and description).
        """
        payload = {
            'action': 'get'
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/pwdgrp.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            text2 = resp.text.split('\n')
            for i, _ in enumerate(text2):  # for i in range(len(text2)):
                text3 = text2[i].split('users=')
                if len(text3) > 1:
                    text4 = text3[1].replace('"', '').replace('\r', '').split(',')
                    for j, _ in enumerate(text4):
                        if text4[j] == name:
                            return 1
            return 0

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.resp_text())
        return text2

    def set_hostname(self, hostname: str = None, *, set_dhcp: str = None):  # 0
        """
        Configure how the device selects a hostname, with the possibility to set a static hostname and/or enable
        auto-configuration by DHCP.

        Args:
            hostname: hostname
            set_dhcp: auto-configuration by DHCP. (yes, no)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'Network.HostName': hostname,
            'Network.VolatileHostName.ObtainFromDHCP': set_dhcp
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def set_stabilizer(self, stabilizer: str = None, *, stabilizer_margin: int = None):  # 0
        """
        Set electronic image stabilization (EIS).

        Args:
            stabilizer: stabilizer value ("on" or "off")
            stabilizer_margin: stabilization margin (0 to 200)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.Stabilizer': stabilizer,
            'ImageSource.I0.Sensor.StabilizerMargin': stabilizer_margin  # 0 a 200
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def set_capture_mode(self, capture_mode: str = None):
        """
        Set capture mode.

        Args:
            capture_mode: capture mode. (1 = 1080, 2 = 720 - camera Full HD)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor': capture_mode
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def set_wdr(self, wdr: str = None, *, contrast: int = None):
        """
        WDR - Forensic Capture - Wide Dynamic Range can improve the exposure when there is a
        considerable contrast between light and dark areas in an image.
        Args:
            wdr: WDR value (on, off)
            contrast: contrast level.

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.WDR': wdr,
            'ImageSource.I0.Sensor.LocalContrast': contrast
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def set_appearance(self, *, brightness: int = None, contrast: int = None,
                       saturation: int = None, sharpness: int = None):
        """
        Image Appearance Setting.

        Args:
            brightness: adjusts the image brightness.
            contrast: adjusts the image's contrast.
            saturation: adjusts color saturation. (Color level)
            sharpness: controls the amount of sharpening applied to the image.

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.Brightness': brightness,
            'ImageSource.I0.Sensor.ColorLevel': saturation,
            'ImageSource.I0.Sensor.Sharpness': sharpness,
            'ImageSource.I0.Sensor.Contrast': contrast
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        soup = BeautifulSoup(resp.text, features="lxml")
        text2 = str(resp)
        text2 += str(soup.get_text())
        return text2

    def set_ir_cut_filter(self, ir_cut: str = None, *, shift_level: int = None):
        """
        IR cut filter settings.

        Args:
            ir_cut: IR value. (Off to allow the camera to 'see' infrared light, set to On during
            daylight or bright light conditions to cut out infrared light, Automatic the camera will
            automatically switch between On and Off, according to the current lighting conditions)
            shift_level: This setting can be used to change when the camera shifts into night mode.

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.DayNight.IrCutFilter': ir_cut,
            'ImageSource.I0.DayNight.ShiftLevel': shift_level
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password), params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    # "flickerfree60" "flickerfree50" "flickerreduced60" "flickerreduced50" "auto" "hold"
    # "auto" "center" "spot"(pontual) "upper" "lower" "left" "right" "custom"
    def set_exposure(self, *, exposure: str = None, exposure_window: str = None,
                     max_exposure_time: int = None,
                     max_gain: int = None, exposure_priority_normal: int = None,
                     lock_aperture: str = None, exposure_value: int = None):
        """
        Exposure Settings.

        Args:
            exposure: exposure  mode. (flickerfree60, flickerfree50, flickerreduced60,
            flickerreduced50, auto, hold)
            exposure_window: This setting determines which part of the image will be used to
            calculate the exposure. (auto, center, spot, upper, lower, left, right, custom)
            max_exposure_time: maximum shutter time (MS)
            max_gain: maximum gain
            exposure_priority_normal: commitment blur / noise
            lock_aperture: lock the shutter aperture
            exposure_value: exposure level

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.Exposure': exposure,  # modo de exposição (exposure)
            'ImageSource.I0.Sensor.ExposureWindow': exposure_window,  # zona de exposição
            'ImageSource.I0.Sensor.MaxExposureTime': max_exposure_time,  # Obturador maximo em MS
            'ImageSource.I0.Sensor.MaxGain': max_gain,  # ganho maximo
            'ImageSource.I0.Sensor.ExposurePriorityNormal': exposure_priority_normal,
            # compromisso desfoque/ruido
            'ImageSource.I0.DCIris.Enable': lock_aperture,  # travar abertura - yes or no
            'ImageSource.I0.Sensor.ExposureValue': exposure_value  # nivel de exposição
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_custom_exposure_window(self, top: int = None, bottom: int = None, left: int = None,
                                   right: int = None):
        """
        Set custom exposition zone.

        Args:
            top: upper limit
            bottom: lower limit
            left: left limit
            right: right limit

        Returns:
            Success (OK) or Failure (Error and description).

        """
        # se passar como pixel atualizar para os valores de 0 a 9999
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.CustomExposureWindow.C0.Top': top,
            'ImageSource.I0.Sensor.CustomExposureWindow.C0.Bottom': bottom,
            'ImageSource.I0.Sensor.CustomExposureWindow.C0.Left': left,
            'ImageSource.I0.Sensor.CustomExposureWindow.C0.Right': right
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_backlight(self, backlight: str = None):
        """
        Backlight compensation makes the subject appear clearer when the image background is too
        bright, or the subject is too dark.

        Args:
            backlight: backlight value. (true, false)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'PTZ.Various.V1.BackLight': backlight,

        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_highlight(self, highlight: int = None):
        """
        The Axis product will detect a bright light from a source such as a torch or car headlights
        and mask that image area. This setting is useful when the camera operates in a very dark
        area where a bright light may overexpose part of the image and prevent the operator from
        seeing other parts of the scene.

        Args:
            highlight: highlight value. (0, 1)

        Returns:
            Success (OK) or Failure (Error and description).
        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.HLCSensitivity': highlight,

        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_image_setings(self, *, defog: str = None, noise_reduction: str = None,
                          noise_reduction_tuning: int = None, image_freeze_ptz: str = None):
        """
        Image Settings.

        Args:
            defog: detect the fog effect and automatically remove it to get a clear image. (on, off)
            noise_reduction: noise reduction function (on, off)
            noise_reduction_tuning: Noise Reduction Adjustment level (0 to 100)
            image_freeze_ptz: freeze the image while the camera is moving during a pan, tilt or zoom
            operation. (on, off)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'ImageSource.I0.Sensor.Defog': defog,
            'ImageSource.I0.Sensor.NoiseReduction': noise_reduction,
            'ImageSource.I0.Sensor.NoiseReductionTuning': noise_reduction_tuning,
            'PTZ.UserAdv.U1.ImageFreeze': image_freeze_ptz
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_ntp_server(self, ntp_server: str = None):
        """
            Configure NTP server.
        Args:
            ntp_server: link or IP server

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'Time.NTP.Server': ntp_server,
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def set_pan_tilt_zoom_enable(self, *, pan_enable: str = None, tilt_enable: str = None,
                                 zoom_enable: str = None):
        """
            Turns PTZ control on and off.

        Args:
            pan_enable: pan enabled value (true, false)
            tilt_enable: tilt enabled value (true, false)
            zoom_enable: zoom enabled value (true, false)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'action': 'update',
            'PTZ.Various.V1.PanEnabled': pan_enable,
            'PTZ.Various.V1.TiltEnabled': tilt_enable,
            'PTZ.Various.V1.ZoomEnabled': zoom_enable
        }
        url = 'http://' + self.cam_ip + '/axis-cgi/param.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def auto_focus(self, focus: str = None):  # on or off
        """
        Enable or disable automatic focus

        Args:
            focus: focus value (on, off)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'autofocus': focus
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/com/ptz.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2

    def auto_iris(self, iris: str = None):
        """
        Enable or disable automatic iris control

        Args:
            iris: iris value (on, off)

        Returns:
            Success (OK) or Failure (Error and description).

        """
        payload = {
            'autoiris': iris
        }

        url = 'http://' + self.cam_ip + '/axis-cgi/com/ptz.cgi'
        resp = requests.get(url, auth=HTTPDigestAuth(self.cam_user, self.cam_password),
                            params=payload)

        if resp.status_code == 200:
            return resp.text

        text2 = str(resp)
        text2 += str(resp.text)
        return text2
