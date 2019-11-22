"""
Library for control AXIS PTZ cameras using Onvif
"""
import logging
from onvif import ONVIFCamera

logging.basicConfig(filename='log-onvif-config.log', filemode='w', level=logging.DEBUG)
logging.info('Started')


#pylint: disable=R0904
class CameraConfiguration:
    """
    Module for configuration cameras AXIS using Onvif
    """

    def __init__(self, ip, user, password):
        self.__cam_ip = ip
        self.__cam_user = user
        self.__cam_password = password


    def camera_start(self):
        """
        Creates the connection to the camera using the onvif protocol

        Returns:
            Return the ptz service object and media service object
        """
        mycam = ONVIFCamera(self.__cam_ip, 80, self.__cam_user, self.__cam_password)
        logging.info('Create media service object')
        media = mycam.create_media_service()
        logging.info('Get target profile')
        media_profile = media.GetProfiles()[0]
        logging.info('Camera working!')

        self.mycam = mycam
        self.camera_media_profile = media_profile
        self.camera_media = media
        self.mycam = mycam

        return self.mycam

    ######## DEVICEMGMT #########
    # https://www.onvif.org/onvif/ver10/device/wsdl/devicemgmt.wsdl

    def set_user(self, name, password, user_level):
        """
        This operation updates the settings for one or several users on a device for
        authentication purposes.
        Args:
            name: user name.
            password: user password.
            user_level: user level.

        Returns:
            Return onvif's response
        """
        params = {'Username': name, 'Password': password, 'UserLevel': user_level}
        return self.mycam.devicemgmt.SetUser(params)

    def create_user(self, username, password, user_level):
        """
        This operation creates new device users and corresponding credentials on a device
        for authentication.
        Args:
            username: user name
            password: user password
            user_level: user level

        Returns:
            Return onvif's response
        """
        params = self.mycam.devicemgmt.create_type('CreateUsers')
        params.User = {'Username': username, 'Password': password, 'UserLevel': user_level}
        return self.mycam.devicemgmt.CreateUsers(params)

    def delete_users(self, username):
        """
        This operation deletes users on a device.
        Args:
            username: user name

        Returns:
            Return onvif's response
        """
        params = self.mycam.devicemgmt.create_type('DeleteUsers')
        params.Username = username
        return self.mycam.devicemgmt.DeleteUsers(params)

    def set_discovery_mode(self, discovery_mode):  # enum { 'Discoverable', 'NonDiscoverable' }
        """
        This operation sets the discovery mode operation of a device.
        Args:
            discovery_mode: Indicator of discovery mode. (Discoverable, NonDiscoverable)

        Returns:
            Return onvif's response.
        """
        params = self.mycam.devicemgmt.create_type('SetDiscoveryMode')
        params.DiscoveryMode = discovery_mode
        return self.mycam.devicemgmt.SetDiscoveryMode(params)

    def set_dns(self, type_dns, ipv4, ipv6):
        """
        This operation sets the DNS settings on a device.
        Args:
            type_dns: Indicates if the address is an IPv4 or IPv6 address.
            ipv4: IPv4 address.
            ipv6: IPv6 address.

        Returns:
            Return onvif's response.
        """
        params = self.mycam.devicemgmt.create_type('SetDNS')
        params.FromDHCP = 1
        params.SearchDomain = 0
        params.DNSManual = {'Type': type_dns, 'IPv4Address': ipv4, 'IPv6Address': ipv6}
        return self.mycam.devicemgmt.SetDNS(params)

    def get_hostname(self):
        """
        This operation is used to get the hostname from a device.

        Returns:
            Return its hostname configurations.
        """
        return self.mycam.devicemgmt.GetHostname()

    def get_ip_address_filter(self):
        """
        This operation gets the IP address filter settings from a device.

        Returns:
            Return its ip address configurations
        """
        return self.mycam.devicemgmt.GetIPAddressFilter()

    def get_device_information(self):
        """
        This operation gets basic device information from the device.

        Returns:
            Return camera information. (Manufacturer, Model, FirmwareVersion, etc)
        """
        return self.mycam.devicemgmt.GetDeviceInformation()

    def get_discovery_mode(self):
        """
        This operation gets the discovery mode of a device.

        Returns:
            Return discovery information.
        """
        return self.mycam.devicemgmt.GetDiscoveryMode()

    def get_dns(self):
        """
        This operation gets the DNS settings from a device.

        Returns:
            Return its DNS configurations.
        """
        return self.mycam.devicemgmt.GetDNS()

    def get_dynamic_dns(self):
        """
        This operation gets the dynamic DNS settings from a device.

        Returns:
            Return its dynamic DNS configurations
        """
        return self.mycam.devicemgmt.GetDynamicDNS()

    def get_network_default_gateway(self):
        """
        This operation gets the default gateway settings from a device.

        Returns:
            Return configured default gateway address(es)
        """
        return self.mycam.devicemgmt.GetNetworkDefaultGateway()

    def get_network_interfaces(self):
        """
        This operation gets the network interface configuration from a device.

        Returns:
            Return of network interface configuration settings as defined by the
            NetworkInterface type
        """
        return self.mycam.devicemgmt.GetNetworkInterfaces()

    def get_network_protocols(self):
        """
        This operation gets defined network protocols from a device.

        Returns:
            return configured network protocols
        """
        return self.mycam.devicemgmt.GetNetworkProtocols()

    def get_ntp(self):
        """
        This operation gets the NTP settings from a device.

        Returns:
            Return NTP server settings
        """
        return self.mycam.devicemgmt.GetNTP()

    def get_system_date_and_time(self):
        """
        This operation gets the device system date and time.

        Returns:
            Return of the daylight saving setting and of the manual system date and time
            (if applicable) or indication of NTP time (if applicable)
        """
        return self.mycam.devicemgmt.GetSystemDateAndTime()

    def get_users(self):
        """
        This operation lists the registered users and corresponding credentials on a device.

        Returns:
            Return registered device users and their credentials (onvif users)
        """
        return self.mycam.devicemgmt.GetUsers()

    def get_wsdl_url(self):
        """
        Request a URL that can be used to retrieve the complete schema and WSDL definitions of a
        device.

        Returns:
            Return a URL entry point where all the necessary product specific WSDL and schema
            definitions can be retrieved
        """
        return self.mycam.devicemgmt.GetWsdlUrl()

    def set_hostname(self, new_hostname):
        """
        This operation sets the hostname on a device.

        Args:
            new_hostname: new hostname

        Returns:
            Return onvif's response
        """
        return self.mycam.devicemgmt.SetHostname(new_hostname)

    def system_reboot(self):
        """
        This operation reboots the device.

        Returns:
            Return contains the reboot message sent by the device
        """
        confirmation = input("Do you want to reboot the camera? (Y or N)\n")
        if confirmation in ('Y', 'y'):
            return self.mycam.devicemgmt.SystemReboot()
        return None

    def start_system_restore(self):
        """
        This operation initiates a system restore from backed up configuration data using the
        HTTP POST mechanism.

        Returns:
            Return HTTP URL to which the backup file may be uploaded and expected down time
        """
        confirmation = input("Do you want to system restore? (Y or N)\n")
        if confirmation in ('Y', 'y'):
            return self.mycam.devicemgmt.StartSystemRestore()
        return None



    ######## MEDIA #########
    # https://www.onvif.org/onvif/ver10/media/wsdl/media.wsdl

    def get_profiles(self): #video profiles
        """
        This command lists all configured video profiles in a device.

        Returns:
            Returns list of video settings.
        """
        return self.camera_media.GetProfiles()

    def get_audio_decoder_configurations(self):
        """
        This operation requests decoder configuration.

        Returns:
            Return decoder configuration.
        """
        return self.camera_media.GetAudioDecoderConfigurations()

    def get_video_analytics_configurations(self):
        """
        This operation fetches the video analytics configuration.

        Returns:
            Return video analytics configuration
        """
        return self.camera_media.GetVideoAnalyticsConfigurations()

    def get_video_encoder_configurations(self):
        """
        This operation request the encoder configuration.

        Returns:
            Return encoder configuration
        """
        return self.camera_media.GetVideoEncoderConfigurations()

    def get_video_source_configurations(self):
        """
        This operation request the video source configuration.

        Returns:
            Return video source configuration.
        """
        return self.camera_media.GetVideoSourceConfigurations()

    def get_video_sources(self):
        """
        This operation lists all available physical video inputs of the device.

        Returns:
            Return all available physical video inputs
        """
        return self.camera_media.GetVideoSources()
