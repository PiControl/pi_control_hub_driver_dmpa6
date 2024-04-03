"""
   Copyright 2024 Thomas Bonk

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from typing import Any, Awaitable, Callable, List

import lirc
from pi_control_hub_driver_api import DeviceCommand

from pi_control_hub_driver_dmpa6.eversolo import (change_vu_display,
                                                  decrease_volume,
                                                  increase_volume, next_track,
                                                  play_or_pause, power_off,
                                                  previous_track,
                                                  set_input_bluetooth,
                                                  set_input_coax,
                                                  set_input_internal_player,
                                                  set_input_optical,
                                                  set_input_usb,
                                                  set_output_analog_rca,
                                                  set_output_balxlr,
                                                  set_output_hdmi,
                                                  set_output_spdif,
                                                  set_output_usb,
                                                  set_output_xlr_rca,
                                                  toggle_screen)
from pi_control_hub_driver_dmpa6.icons import (in_bluetooth, in_coax,
                                               in_internal_player, in_optical,
                                               in_usb, out_analog_rca,
                                               out_balxlr, out_hdmi, out_spdif,
                                               out_usb_dac, out_xlr_rca,
                                               play_next, play_pause,
                                               play_previous, toggle_display,
                                               toggle_power, toggle_vu,
                                               volume_down, volume_up)

CallbackType = Callable[[str], Awaitable[Any]]

class DmpA6HttpDeviceCommand(DeviceCommand):
    """A command that is doing a HTTP request to execute the command"""
    def __init__(
            self,
            cmd_id: int,
            title: str,
            icon: bytes,
            device_id: str,
            callback: CallbackType):
        DeviceCommand.__init__(self, cmd_id=cmd_id, title=title, icon=icon)
        self._ip_address = device_id
        self._callback = callback

    async def execute(self):
        """
        Execute the command. This method must be implemented by the specific command.

        Raises
        ------
        `DeviceCommandException` in case of an error while executing the command.
        """
        await self._callback(self._ip_address)

class DmpA6PowerToggleCommand(DeviceCommand):
    """Power toggle command via LIRC"""
    def __init__(
            self,
            cmd_id: int,
            title: str,
            icon: bytes,
            device_id: str):
        DeviceCommand.__init__(self, cmd_id=cmd_id, title=title, icon=icon)
        self._ip_address = device_id
        try:
            self._lirc_client = lirc.Client()
        except lirc.exceptions.LircdConnectionError:
            self._lirc_client = None

    async def execute(self):
        """
        Execute the command. This method must be implemented by the specific command.

        Raises
        ------
        `DeviceCommandException` in case of an error while executing the command.
        """
        if self._lirc_client is None:
            await power_off(self._ip_address)
        else:
            # use lirc to toggle power
            pass


# Command IDs
TOGGLE_POWER = 1
TOGGLE_DISPLAY = 2
TOGGLE_VU = 3
VOLUME_UP = 4
VOLUME_DOWN = 5
PLAY_PAUSE = 6
PLAY_NEXT = 7
PLAY_PREVIOUS = 8

INPUT_INTERNAL_PLAYER = 10
INPUT_BLUETOOTH = 11
INPUT_USB = 12
INPUT_OPTICAL = 13
INPUT_COAX = 14
OUTPUT_BALXLR = 15
OUTPUT_ANALOG_RCA = 16
OUTPUT_XLR_RCA = 17
OUTPUT_HDMI = 18
OUTPUT_SPDIF = 19
OUTPUT_USB_DAC = 20


def create_commands(device_id: str) -> List[DeviceCommand]:
    # TODO
    return [
        DmpA6PowerToggleCommand(TOGGLE_POWER, "On/Off", toggle_power(), device_id),

        DmpA6HttpDeviceCommand(TOGGLE_DISPLAY, "Display on/off", toggle_display(), device_id, toggle_screen),
        DmpA6HttpDeviceCommand(TOGGLE_VU, "Change VU", toggle_vu(), device_id, change_vu_display),
        DmpA6HttpDeviceCommand(VOLUME_UP, "Volume +", volume_up(), device_id, increase_volume),
        DmpA6HttpDeviceCommand(VOLUME_DOWN, "Volume -", volume_down(), device_id, decrease_volume),
        DmpA6HttpDeviceCommand(PLAY_PAUSE, "Play/Pause", play_pause(), device_id, play_or_pause),
        DmpA6HttpDeviceCommand(PLAY_NEXT, "Next Track", play_next(), device_id, next_track),
        DmpA6HttpDeviceCommand(PLAY_PREVIOUS, "Previous Track", play_previous(), device_id, previous_track),

        DmpA6HttpDeviceCommand(INPUT_INTERNAL_PLAYER, "Input: Internal Player", in_internal_player(), device_id, set_input_internal_player),
        DmpA6HttpDeviceCommand(INPUT_BLUETOOTH, "Input: Bluetooth", in_bluetooth(), device_id, set_input_bluetooth),
        DmpA6HttpDeviceCommand(INPUT_USB, "Input: USB", in_usb(), device_id, set_input_usb),
        DmpA6HttpDeviceCommand(INPUT_OPTICAL, "Input: Optical", in_optical(), device_id, set_input_optical),
        DmpA6HttpDeviceCommand(INPUT_COAX, "Input: Coax", in_coax(), device_id, set_input_coax),

        DmpA6HttpDeviceCommand(OUTPUT_BALXLR, "Output: Balanced XLR", out_balxlr(), device_id, set_output_balxlr),
        DmpA6HttpDeviceCommand(OUTPUT_ANALOG_RCA, "Output: Analog RCA", out_analog_rca(), device_id, set_output_analog_rca),
        DmpA6HttpDeviceCommand(OUTPUT_XLR_RCA, "Output: XLR/RCA", out_xlr_rca(), device_id, set_output_xlr_rca),
        DmpA6HttpDeviceCommand(OUTPUT_HDMI, "Output: HDMI", out_hdmi(), device_id, set_output_hdmi),
        DmpA6HttpDeviceCommand(OUTPUT_SPDIF, "Output: ", out_spdif(), device_id, set_output_spdif),
        DmpA6HttpDeviceCommand(OUTPUT_USB_DAC, "Output: ", out_usb_dac(), device_id, set_output_usb),
    ]
