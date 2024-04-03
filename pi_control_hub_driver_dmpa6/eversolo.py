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

import asyncio
import json

import aiohttp
import requests


async def connect_device_async(
        ip_address: str,
        port: int = 9529,
        client_name: str = None,
        client_uuid: str = None) -> dict:
    """This function makes a connection to the the Eversolo device.

    Parameters
    ----------
    `ip_address`: `str``
        IP address of the Eversolo device
    `port`: ìnt``
        Port of service running on the Eversolo device; default is 9529.
    `client_name`: `str``
        Name of client that wants to connect.
    `client_uuid`: `str`
        UUID of the client."""

    assert client_name is not None, "client_name must be given"
    assert client_uuid is not None, "device_uuid must be given"

    async with aiohttp.ClientSession() as session:
        url = f"http://{ip_address}:{port}/ZidooControlCenter/connect?name={client_name}&uuid={client_uuid}&tag=0&type=1"
        async with session.get(url) as response:
            response_payload = await response.json()
            return response_payload

def connect_device(
        ip_address: str,
        port: int = 9529,
        client_name: str = None,
        client_uuid: str = None) -> dict:
    """This function makes a connection to the the Eversolo device.

    Parameters
    ----------
    `ip_address`: `str``
        IP address of the Eversolo device
    `port`: ìnt``
        Port of service running on the Eversolo device; default is 9529.
    `client_name`: `str``
        Name of client that wants to connect.
    `client_uuid`: `str`
        UUID of the client."""

    assert client_name is not None, "client_name must be given"
    assert client_uuid is not None, "device_uuid must be given"

    url = f"http://{ip_address}:{port}/ZidooControlCenter/connect?name={client_name}&uuid={client_uuid}&tag=0&type=1"
    response = requests.get(url, timeout=10)
    response_body = json.loads(response.text)
    return response_body

async def _execute_command(ip_address: str, port: int = 9529, uri: str = "") -> dict:
    """Execute a command."""
    async with aiohttp.ClientSession() as session:
        url = f"http://{ip_address}:{port}{uri}"
        async with session.get(url) as response:
            response_text = await response.text()
            response_json = json.loads(response_text)
            return response_json

async def play_or_pause(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/playOrPause")
    if response["status"] != 200:
        pass
        # TODO

async def increase_volume(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooControlCenter/RemoteControl/sendkey?key=Key.VolumeUp")
    if response["status"] != 200:
        pass
        # TODO

async def decrease_volume(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooControlCenter/RemoteControl/sendkey?key=Key.VolumeDown")
    if response["status"] != 200:
        pass
        # TODO

async def next_track(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/playNext")
    if response["status"] != 200:
        pass
        # TODO

async def previous_track(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/playLast")
    if response["status"] != 200:
        pass
        # TODO

async def change_vu_display(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/changVUDisplay")
    if response["status"] != 200:
        pass
        # TODO

async def toggle_screen(ip_address: str, port: int = 9529):
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setPowerOption?tag=screen")
    if response["status"] != 200:
        pass
        # TODO

async def set_input_internal_player(ip_address: str, port: int = 9529):
    """Set the input port to the internal player input port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setInputList?tag=XMOS&index=4")
    if response["status"] != 200:
        pass
        # TODO

async def set_input_bluetooth(ip_address: str, port: int = 9529):
    """Set the input port to the bluetooth input port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setInputList?tag=BT&index=4")
    if response["status"] != 200:
        pass
        # TODO

async def set_input_usb(ip_address: str, port: int = 9529):
    """Set the input port to the usb input port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setInputList?tag=USB&index=4")
    if response["status"] != 200:
        pass
        # TODO

async def set_input_optical(ip_address: str, port: int = 9529):
    """Set the input port to the optical input port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setInputList?tag=SPDIF&index=4")
    if response["status"] != 200:
        pass
        # TODO

async def set_input_coax(ip_address: str, port: int = 9529):
    """Set the input port to the coax input port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setInputList?tag=RCA&index=4")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_balxlr(ip_address: str, port: int = 9529):
    """Set the output port to the balanced XLR output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=XLR&index=0")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_analog_rca(ip_address: str, port: int = 9529):
    """Set the output port to the analog RCA output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=RCA&index=0")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_xlr_rca(ip_address: str, port: int = 9529):
    """Set the output port to the XLR/RCA output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=XLRRCA&index=0")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_hdmi(ip_address: str, port: int = 9529):
    """Set the output port to the HDMI output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=HDMI&index=0")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_spdif(ip_address: str, port: int = 9529):
    """Set the output port to the SPDIF output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=SPDIF&index=0")
    if response["status"] != 200:
        pass
        # TODO

async def set_output_usb(ip_address: str, port: int = 9529):
    """Set the output port to the USB (DAC) output port."""
    response = await _execute_command(ip_address, port=port, uri="/ZidooMusicControl/v2/setOutInputList?tag=USB&index=0")
    if response["status"] != 200:
        pass
        # TODO
