# Axis Vapix/Onvif Python

This library is designed to provide control and configuration of Axis cameras using the Onvif and Vapix protocol.

**VAPIX®** is Axis' own open API (Application Programming Interface) using standard protocols enabling integration into a wide range of solutions on different platforms.  

**VAPIX®** provides functionality for requesting images, controlling Pan Tilt Zoom, controlling Input and Output ports, retrieve and control internal settings, to manage Events, record and retrieve video to/from the SD card, and much, much more. Almost all functionality available in Axis products can be controlled using VAPIX®, some functions are even only supported via VAPIX®, for example, to retrieve Bitmap images.

**ONVIF (Open Network Video Interface Forum)** is a global and open industry forum with the goal of facilitating the development and use of a global open standard for the interface of physical IP-based security products. ONVIF creates a standard for how IP products within video surveillance and other physical security areas can communicate with each other. ONVIF is an organization started in 2008 by Axis Communications, Bosch Security Systems and Sony.

## Installation
Install the package through pip: 

````
pip install sensecam-control
````
## Execution

Example of use:

````
from sensecam_control import vapix_control
from sensecam_control import onvif_control


Camera1 = vapix_control.CameraControl(<ip>, <login>, <password>)
Camera2 = onvif_control.CameraControl(<ip>, <login>, <password>)

Camera1.absolute_move(10, 20, 1)
Camera1.absolute_move(10, 20, 1, 50)

Camera2.absolute_move(0.02, 0.60, 0.0)
Camera2.relative_move(0.3, -0.2, 0)

````



## Functions
### Vapix Control

* `absolute_move(pan, tilt, zoom, speed)` - Operation to move pan, tilt or zoom to a absolute destination.
    - pan (float): pans the device relative to the (0,0) position. Values (-180.0 … 180.0)
    - tilt (float): tilts the device relative to the (0,0) position. Values (-180.0 … 180.0)
    - zoom (int): zooms the device n steps. Values (1 … 9999)
    - speed (int): speed move camera. Values (1 … 100)

* `continuous_move(pan, tilt, zoom)` - Operation for continuous Pan/Tilt and Zoom movements.
    - pan (int): Speed of movement of Pan. (-100 … 100)
    - tilt (int): Speed of movement of Tilt. (-100 … 100)
    - zoom (int): Speed of movement of Zoom. (-100 … 100)

* `relative_move(pan, tilt, zoom, speed)` - Operation for Relative Pan/Tilt and Zoom Move.
    - pan (float): Pans the device n degrees relative to the current position. (-360.0 … 360.0)
    - tilt (float): Tilts the device n degrees relative to the current position. (-360.0 … 360.0)
    - zoom (int): Zooms the device n steps relative to the current position. (-9999 … 9999)
    - speed (int): speed move camera. (1 … 100)

* `stop_move()` - Operation to stop ongoing pan, tilt and zoom movements of absolute relative and continuous type.

* `center_move(pos_x, pos_y, speed)` - Used to send the coordinates for the point in the image where the user clicked. This information is then used by the server to calculate the pan/tilt move required to (approximately) center the clicked point.
    - pos_x (int): value of the X coordinate.
    - pos_y (int): value of the Y coordinate.
    - speed (int): speed move camera. (-100 … 100)

* `area_zoom(pos_x, pos_y, zoom, speed)` - Centers on positions x,y (like the center command) and zooms by a factor of z/100.
    - pos_x (int): value of the X coordinate.
    - pos_y (int): value of the Y coordinate.
    - zoom (int): zooms by a factor.
    - speed (int): speed move camera. (-100 … 100)

* `move(position, speed)` - Moves the device 5 degrees in the specified direction.
    - position (str): position to move. (home, up, down, left, right, upleft, upright, downleft...)
    - speed (int): speed move camera.

* `go_home_position(speed)` -  Operation to move the PTZ device to it's "home" position.
    - speed (int): speed move camera. (-100 … 100)

* `get_ptz()` - Operation to request PTZ status.

* `go_to_server_preset_name(name, speed)` - Move to the position associated with the preset on server.
    - name (str): name of preset position server.
    - speed (int): speed move camera. (-100 … 100)

* `go_to_server_preset_no(number, speed)` - Move to the position associated with the specified preset position number.
    - number (int): number of preset position server.
    - speed (int): speed move camera. (-100 … 100)
            
* `go_to_device_preset(preset_pos, speed)` - Bypasses the presetpos interface and tells the device to go directly to the preset position number stored in the device, where the is a device-specific preset position number.
    - preset_pos (int): number of preset position device.
    - speed (int): speed move camera. (-100 … 100)
            
* `list_preset_device()` - List the presets positions stored in the device.

* `list_all_preset()` - List all available presets position.

* `set_speed(speed)` - Sets the head speed of the device that is connected to the specified camera.
    - speed (int): speed value. (-100 … 100)

* `get_speed()` - Requests the camera's speed of movement.

### Vapix Configuration
* `factory_reset_default()` - Reload factory default. All parameters except Network.BootProto, Network.IPAddress, Network. SubnetMask, Network.Broadcast and Network.DefaultRouter are set to their factory default values.

* `hard_factory_reset_default()` - Reload factory default. All parameters are set to their factory default value.

* `restart_server()` - Restart server.

* `get_server_report()` - This CGI request generates and returns a server report. This report is useful as an input when requesting support. The report includes product information, parameter settings and system logs.

* `get_system_log()` - Retrieve system log information. The level of information included in the log is set in the Log. System parameter group.

* `get_system_access_log()` - Retrieve client access log information. The level of information included in the log is set in the Log.Access parameter group.

* `get_date_and_time()` - Get the system date and time.

* `set_date(year_date, month_date, day_date)` - Change the system date.
    - year_date (int): current year.
    - month_date (int): current month.
    - day_date (int): current day.

* `set_time(hour, minute, second, timezone)` - Change the system time.
    - hour (int): current hour.
    - minute (int): current minute.
    - second (int): current second.
    - timezone (str): specifies the time zone that the new date and/or time is given in. The camera
            translates the time into local time using whichever time zone has been specified through
            the web configuration.

* `get_image_size()` - Retrieve the actual image size with default image settings or with given parameters.

* `get_video_status(camera_status)` - Video encoders only. Check the status of one or more video sources.
    - camera_status (int): video source.

* `get_bitmap_request(resolution, camera, square_pixel)` - Request a bitmap image.
    - resolution (str): resolution of the returned image. Check the product’s Release notes for
            supported resolutions.
    - camera (str): select a video source or the quad stream. (1, 2, ...,quad) 
    - square_pixel (int): enable/disable square pixel correction. Applies only to video encoders.


* `get_jpeg_request(resolution, camera, square_pixel, compression, clock, date, text, text_string, text_color, text_background_color, rotation, text_position, overlay_image, overlay_position)` - The requests specified in the JPEG/MJPG section are supported by those video products that use JPEG and MJPG encoding.
    - resolution (str): Resolution of the returned image. Check the product’s Release notes.
    - camera (str): selects the source camera or the quad stream. (1, 2, ...,quad) 
    - square_pixel (int): enable/disable square pixel correction. Applies only to video encoders. (1, 0)
    - compression (int): adjusts the compression level of the image. (0 … 100)
    - clock (int): shows/hides the time stamp. (0 = hide, 1 = show)
    - date (int): shows/hides the date. (0 = hide, 1 = show)
    - text (int): shows/hides the text. (0 = hide, 1 = show)
    - text_string (str): the text shown in the image, the string must be URL encoded.
    - text_color (str): the color of the text shown in the image. (black, white)
    - text_background_color (str): the color of the text background shown in the image. (black, white, transparent, semitransparent)
    - rotation (int): totate the image clockwise. (0, 90, 180, 270)
    - text_position (str): the position of the string shown in the image. (top, bottom)
    - overlay_image (int): tnable/disable overlay image.(0 = disable, 1 = enable)
    - overlay_position (str): the x and y coordinates defining the position of the overlay image. ('< int >x< int >' or < int >,< int >)

* `get_type_camera()` - Request type camera.

* `get_dynamic_text_overlay()` - Get dynamic text overlay in the image.

* `set_dynamic_text_overlay(text, camera)` - Set dynamic text overlay in the image.
     - text (str): text to set overlay.
     - camera (str): select video source or the quad stream. ( default: default camera)

* `check_profile(name)` - Check if the profile exists.
    - name (str): profile name

* `create_profile(name: str, *, resolution, videocodec, fps, compression, h264profile, gop, bitrate, bitratepriority)` - Create stream profile.
    - name (str): profile name.
    - resolution (str): resolution.
    - videocodec (str): video codec. (h264, mjpg)
    - fps (int): frame rate.
    - compression (int): adjusts the compression level of the image. (0 … 100)
    - h264profile (str): profile h264. (high, main, baseline)
    - gop (int): Group of pictures. (1 ... 1023)
    - bitrate (int): video bitrate.
    - bitratepriority (str): video bitrate priority. (framerate, quality)

* `create_user(user, password, sgroup, *, group, comment)` - Create user.
    - user (str): the user account name (1-14 characters), a non-existing user account name. Valid characters are a-z, A-Z and 0-9.
    - password (str): the unencrypted password (1-64 characters) for the account. ASCII characters from character code 32 to 126 are valid.
    - group (str): an existing primary group name of the account. The recommended value for this argument is 'users' [default]. (users, root)
    - sgroup (str): security group. (admin, operator, viewer, ptz)
    - comment (str): user description.

* `update_user(user, password, *, group, sgroup, comment)` - Update user params.
    - user (str): user name
    - password (str): new password or current password to change others params.
    - group (str): an existing primary group name of the account. The recommended value for this argument is 'users' [default]. (users, root)
    - sgroup (str): security group. (admin, operator, viewer, ptz)
    - comment (str): user description.

* `remove_user(user)` - Remove user.
    - user (str):  user name

* `check_user(name)` - Check if user exists.
    - user (str):  user name

* `set_hostname(hostname, *, set_dhcp)` - Configure how the device selects a hostname, with the possibility to set a static hostname and/or enable auto-configuration by DHCP.
    - hostname (str):  hostname
    - set_dhcp: enable auto-configuration by DHCP. (yes, no)

* `set_stabilizer( stabilizer, *, stabilizer_margin)` - Set electronic image stabilization (EIS).
    - stabilizer (str): stabilizer value (on, off)
    - stabilizer_margin: stabilization margin (0 ... 200)

* `set_capture_mode(capture_mode)` - Set capture mode.
    - capture_mode (str): capture mode.

* `set_wdr(wdr, *, contrast)` - WDR - Forensic Capture - Wide Dynamic Range can improve the exposure when there is a considerable contrast between light and dark areas in an image.
    - wdr (str): WDR value (on, off)
    - contrast (int): contrast level.
            
* `set_appearance(*, brightness, contrast, saturation, sharpness)` - Image Appearance Setting.
    - brightness (int): adjusts the image brightness.
    - contrast (int): adjusts the image's contrast.
    - saturation (int): adjusts color saturation - color level.
    - sharpness (int): controls the amount of sharpening applied to the image.

* `set_ir_cut_filter(ir_cut, *, shift_level)` - IR cut filter settings.
- ir_cut (str): IR value. (on, off, auto)
    - shift_level (int): This setting can be used to change when the camera shifts into night mode.


* `set_exposure(*, exposure, exposure_window, max_exposure_time, max_gain, exposure_priority_normal, lock_aperture, exposure_value)` - Exposure Settings.
    - exposure (str): exposure  mode. (flickerfree60, flickerfree50, flickerreduced60,
            flickerreduced50, auto, hold)
    - exposure_window (str): This setting determines which part of the image will be used to
            calculate the exposure. (auto, center, spot, upper, lower, left, right, custom)
    - max_exposure_time (int): maximum shutter time (MS).
    - max_gain (int): maximum gain.
    - exposure_priority_normal (int): commitment blur / noise.
    - lock_aperture (str): lock the shutter aperture.
    - exposure_value (int): exposure level.

* `set_custom_exposure_window(top, bottom, left, right)` - Set custom exposition zone.
    - top (int): upper limit.
    - bottom (int): lower limit.
    - left (int): left limit.
    - right (int): right limit.

* `set_backlight(backlight)` - Backlight compensation makes the subject appear clearer when the image background is too bright, or the subject is too dark.
    - backlight (str): backlight value. (true, false)
    
* `set_highlight(highlight)` - The Axis product will detect a bright light from a source such as a torch or car headlights and mask that image area. This setting is useful when the camera operates in a very dark area where a bright light may overexpose part of the image and prevent the operator from seeing other parts of the scene.
    - highlight (str): highlight value. (0, 1)
    
* `set_image_setings(*, defog, noise_reduction, noise_reduction_tuning, image_freeze_ptz)` - Image Settings.
    - defog (str): detect the fog effect and automatically remove it to get a clear image. (on, off)
    - noise_reduction (str): noise reduction function (on, off)
    - noise_reduction_tuning (int): Noise Reduction Adjustment level (0 to 100)
    - image_freeze_ptz (str): freeze the image while the camera is moving during a pan, tilt or zoom operation. (on, off)
            
* `set_ntp_server(ntp_server)` - Configure NTP server.
    - ntp_server (str): ntp server.

* `set_pan_tilt_zoom_enable(*, pan_enable, tilt_enable, zoom_enable)` - Turns PTZ control on and off.
    - pan_enable (str): pan enabled value (true, false)
    - tilt_enable (str): tilt enabled value (true, false)
    - zoom_enable (str): zoom enabled value (true, false)
    
* `auto_focus(focus)` - Enable or disable automatic focus.
    - focus (str): focus value (on, off)

* `auto_iris(iris)` - Enable or disable automatic iris control.
    - iris (str): iris value (on, off)

### Onvif Control
* `absolute_move(pan, tilt, zoom)` - Operation to move pan, tilt or zoom to a absolute destination.
    - pan (float): pans the device relative to the (0,0) position.
    - tilt (float): tilts the device relative to the (0,0) position.
    - zoom (float): zooms the device n steps.

* `continuous_move(pan, tilt, zoom)` - Operation for continuous Pan/Tilt and Zoom movements.
    - pan (float): speed of movement of Pan.
    - tilt (float): speed of movement of Tilt.
    - zoom (float): speed of movement of Zoom.
    
* `relative_move(pan, tilt, zoom)` - Operation for Relative Pan/Tilt and Zoom Move.
    - pan (float): pans the device n degrees relative to the current position.
    - tilt (float): tilts the device n degrees relative to the current position.
    - zoom (float): zooms the device n steps relative to the current position.
    
* `stop_move()` - Operation to stop ongoing pan, tilt and zoom movements of absolute relative and continuous type.

* `set_home_position()` - Operation to save current position as the home position.
    
* `go_home_position()` - Operation to move the PTZ device to it's "home" position.
   
* `get_ptz()` - Operation to request PTZ status.

* `set_preset(preset_name)` - The command saves the current device position parameters.
    - preset_name (str): Name for preset.
    
* `get_preset()` - Operation to request all PTZ presets.

* `get_preset_complete()` - Operation to request all PTZ presets.

* `remove_preset(preset_name)` - Operation to remove a PTZ preset.
    - preset_name (str): Preset name.
    
* `go_to_preset(preset_position)` - Operation to go to a saved preset position.
    - preset_position (str): preset name.

### Onvif Config
* `set_user(name, password, user_level)` - This operation updates the settings for one or several users on a device for authentication purposes.
    - name (str): user name.
    - password (str): user password.
    - user_level (str): user level.
    
* `create_user(username, password, user_level)` - This operation creates new device users and corresponding credentials on a device for authentication.
    - username (str): user name.
    - password (str): user password.
    - user_level (str): user level.
    
* `delete_users(username)` - This operation deletes users on a device.
    - username (str): user name.
    
* `get_users()` - This operation lists the registered users and corresponding credentials on a device.
    
* `set_discovery_mode(discovery_mode)` - This operation sets the discovery mode operation of a device.
    - discovery_mode (str): Indicator of discovery mode. (Discoverable, NonDiscoverable)
    
* `set_dns(type_dns, ipv4, ipv6)` - This operation sets the DNS settings on a device.
    - type_dns (str): Indicates if the address is an IPv4 or IPv6 address.
    - ipv4 (str): IPv4 address.
    - ipv6 (str): IPv6 address.
            
* `get_hostname()` - This operation is used to get the hostname from a device.

* `set_hostname(new_hostname)` - This operation sets the hostname on a device.
    - new_hostname (str): new hostname.

* ` get_ip_address_filter()` - This operation gets the IP address filter settings from a device.

* `get_device_information()` - This operation gets basic device information from the device.

* `get_discovery_mode()` -This operation gets the discovery mode of a device.

* `get_dns()` - This operation gets the DNS settings from a device.

* `get_dynamic_dns()` - This operation gets the dynamic DNS settings from a device.

* `get_network_default_gateway()` - This operation gets the default gateway settings from a device.

* `get_network_interfaces()` - This operation gets the network interface configuration from a device.

* `get_network_protocols()` - This operation gets defined network protocols from a device.

* `get_ntp()` - This operation gets the NTP settings from a device.

* `get_system_date_and_time()` - This operation gets the device system date and time.

* `get_wsdl_url()` - Request a URL that can be used to retrieve the complete schema and WSDL definitions of a device.
    
* `system_reboot()` - This operation reboots the device.

* `start_system_restore()` - This operation initiates a system restore from backed up configuration data using the HTTP POST mechanism.

* `get_profiles()` - This command lists all configured video profiles in a device.

* `get_audio_decoder_configurations()` - This operation requests decoder configuration.

* `get_video_analytics_configurations()` - This operation fetches the video analytics configuration.

* `get_video_encoder_configurations()` - This operation request the encoder configuration.

* `get_video_source_configurations()` - This operation request the video source configuration.

* `get_video_sources()` - This operation lists all available physical video inputs of the device.
