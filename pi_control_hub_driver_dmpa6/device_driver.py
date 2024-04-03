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

import dbm
import json
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import List, Tuple
from uuid import UUID, uuid4

from pi_control_hub_driver_api import (AuthenticationMethod,
                                       CommandNotFoundException, DeviceCommand,
                                       DeviceDriver, DeviceDriverDescriptor,
                                       DeviceInfo, DeviceNotFoundException)
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

from pi_control_hub_driver_dmpa6.commands import INPUT_BLUETOOTH, INPUT_COAX, INPUT_INTERNAL_PLAYER, INPUT_OPTICAL, INPUT_USB, OUTPUT_ANALOG_RCA, OUTPUT_BALXLR, OUTPUT_HDMI, OUTPUT_SPDIF, OUTPUT_USB_DAC, OUTPUT_XLR_RCA, PLAY_NEXT, PLAY_PAUSE, PLAY_PREVIOUS, TOGGLE_DISPLAY, TOGGLE_POWER, TOGGLE_VU, VOLUME_DOWN, VOLUME_UP, create_commands
from pi_control_hub_driver_dmpa6.design_patterns import SingletonMeta

from .eversolo import connect_device, connect_device_async


class DmpA6DeviceDriver(DeviceDriver):
    """The driver that communicates with an Eversolo DMP-A6 device."""
    def __init__(self, device_info: DeviceInfo):
        DeviceDriver.__init__(self, device_info)
        self._commands = create_commands(device_info.device_id)

    async def get_commands(self) -> List[DeviceCommand]:
        """Return the commands that are supported by this device.

        Returns
        -------
        The commands that are supported by this device.

        Raises
        ------
        `DeviceDriverException` in case of an error.
        """
        return self._commands

    async def get_command(self, cmd_id: int) -> DeviceCommand:
        """Return the command with the given ID.

        Parameters
        ----------
        cmd_id : int
            The numeric ID of the command.

        Returns
        -------
        The command for the ID.

        Raises
        ------
        `CommandNotFoundException` if the command is not known.

        `DeviceDriverException` in case of an other error.
        """
        result = list(filter(lambda c: c.id == cmd_id, await self.get_commands()))
        if len(result) > 0:
            return result[0]
        raise CommandNotFoundException(self.name, cmd_id)

    @property
    def remote_layout_size(self) -> Tuple[int, int]:
        """
        The size of the remote layout.

        Returns
        -------
        A tuple with the width and height of the layout
        """
        return 3, 9

    @property
    def remote_layout(self) -> List[List[int]]:
        """
        The layout of the remote.

        Returns
        -------
        The layout as a list of columns.
        """
        return [
            [TOGGLE_POWER, TOGGLE_DISPLAY, TOGGLE_VU],
            [VOLUME_DOWN, -1, VOLUME_UP],
            [PLAY_PREVIOUS, PLAY_PAUSE, PLAY_NEXT],
            [-1, -1, -1],
            [INPUT_INTERNAL_PLAYER, INPUT_BLUETOOTH, INPUT_USB],
            [INPUT_OPTICAL, -1, INPUT_COAX],
            [-1, -1, -1],
            [OUTPUT_BALXLR, OUTPUT_ANALOG_RCA, OUTPUT_XLR_RCA],
            [OUTPUT_HDMI, OUTPUT_SPDIF, OUTPUT_USB_DAC]
        ]

    async def execute(self, command: DeviceCommand):
        """
        Executes the given command.

        Parameters
        ----------
        command : DeviceCommand
            The command that shall be executed

        Raises
        ------
        `DeviceCommandException` in case of an error while executing the command.
        """
        await command.execute()

    @property
    async def is_device_ready(self) -> bool:
        """
        A flag the determines whether the device is ready.

        Returns
        -------
        true if the device is ready, otherwise false.
        """
        try:
            await connect_device_async(
                self.device_id,
                client_name="PiControlHub",
                client_uuid="f6c4ad46-f0d3-11ee-a951-0242ac120002")
            return True
        except Exception:
            return False


class ZeroconfBrowser(ServiceListener, metaclass=SingletonMeta):
    def __init__(self):
        self._zeroconf = Zeroconf()
        self._browser = ServiceBrowser(self._zeroconf, "_adb._tcp.local.", self, delay=10)
        self._devices = []

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        DmpA6DeviceDriverDescriptor._logger.info("Service '%s' updated", name)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        DmpA6DeviceDriverDescriptor._logger.info("Service '%s' removed", name)

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            addresses = [address for address in info.parsed_addresses()]
            try:
                raw_device_info = connect_device(
                    addresses[0],
                    client_name="PiControlHub",
                    client_uuid="f6c4ad46-f0d3-11ee-a951-0242ac120002")
                device_info = DeviceInfo(
                    name=raw_device_info["device"]["name"],
                    device_id=raw_device_info["device"]["host"])
                self._devices.append(device_info)
            except Exception as ex:
                pass

    @property
    def devices(self) -> List[DeviceInfo]:
        return self._devices


class DmpA6DeviceDriverDescriptor(DeviceDriverDescriptor):
    """Eversolo DMP-A6 device driver descriptor"""

    _logger = logging.getLogger("DmpA6DeviceDriverDescriptor")

    def __init__(self):
        DeviceDriverDescriptor.__init__(
            self,
            UUID("8923777f-9761-4a9d-9747-479f8913f503"),                  # driver id
            "Eversolo DMP-A6",                                             # display name
            "PiControl Hub driver for controling Eversolo DMP-A6 devices", # description
        )
        self._zeroconf_browser = ZeroconfBrowser()
        self._cache_filepath = os.path.join(DeviceDriverDescriptor.get_config_path(), "eversolo.cache")
        self._filecache = dbm.open(self._cache_filepath, "c")

    def _cached_devices(self) -> List[DeviceInfo]:
        with dbm.open(self._cache_filepath, "c") as cache:
            if "cached_devices" in cache:
                jsn: str = cache["cached_devices"]
                devices_jsn = json.loads[jsn]
                devices = list(map(lambda d: DeviceInfo(d["name"], d["device_id"]), devices_jsn))
                return devices

            return self._zeroconf_browser.devices

    def _cache_devices(self, devices: List[DeviceInfo]):
        with dbm.open(self._cache_filepath, "c") as cache:
            devices_jsn = list(map(lambda d: {"name": d.name, "device_id": d.device_id}, devices))
            jsn: str = json.dumps(devices_jsn)
            cache["cached_devices"] = jsn

    async def get_devices(self) -> List[DeviceInfo]:
        """Returns a list with the available device instances."""
        if len(self._zeroconf_browser.devices) == 0:
            return self._cached_devices()

        self._cache_devices(self._zeroconf_browser.devices)
        return self._zeroconf_browser.devices

    async def get_device(self, device_id: str) -> DeviceInfo:
        """Gets the device with the given ID"""
        devices = list(filter(lambda d: d.device_id == device_id, await self.get_devices()))
        if len(devices) == 0:
            raise DeviceNotFoundException(device_id=device_id)
        return devices[0]

    @property
    def authentication_method(self) -> AuthenticationMethod:
        """The authentication method that is required when pairing a device."""
        return AuthenticationMethod.NONE

    @property
    def requires_pairing(self) -> bool:
        """This flag determines whether pairing is required to communicate with this device."""
        return False

    async def start_pairing(self, device_info: DeviceInfo, remote_name: str) -> Tuple[str, bool]:
        """Start the pairing process with the given device.

        Parameters
        ----------
        device_info : DeviceInfo
            The device to pair with.
        remote_name : str
            The name of the remote that will control this device.

        Returns
        -------
        A tuple consisting of a pairing request ID and a flag that determines whether the device
        provides a PIN. If the device is not found (None, False) is returned.
        """
        return str(uuid4()), False

    async def finalize_pairing(self, pairing_request: str, credentials: str, device_provides_pin: bool) -> bool:
        """Finalize the pairing process

        Parameters
        ----------
        pairing_request : str
            The pairing request ID returns by ``start_pairing``
        device_provides_pin : bool
            The flag that determines whether the device provides a PIN.
        """
        return True

    async def create_device_instance(self, device_id: str) -> DeviceDriver:
        """Create a device driver instance for the device with the given ID.

        Parameters
        ----------
        device_id : str
            The ID of the device.

        Returns
        -------
        The instance of the device driver or None in case of an error.
        """
        return DmpA6DeviceDriver(await self.get_device(device_id))

def get_driver_descriptor() -> DeviceDriverDescriptor:
    """This function returns an instance of the device-specific DeviceDriverDescriptor.

    Returns
    -------
    `AppleTvDeviceDriverDescriptor`: An instance of the DeviceDriverDescriptor.
    """
    _ = ZeroconfBrowser()
    return DmpA6DeviceDriverDescriptor()
