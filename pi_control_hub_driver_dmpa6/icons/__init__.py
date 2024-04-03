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

import os
import pathlib

__directory = pathlib.Path(__file__).parent.resolve()
__image_data = {}

def __read_icon(filename: str) -> bytes:
    filepath = os.path.join(__directory, filename)
    if filepath in __image_data:
        return __image_data[filepath]

    with open(os.path.join(__directory, filename), mode="rb") as f:
        data: bytes = f.read()
        __image_data[filepath] = data
        return data

def toggle_power() -> bytes: return __read_icon("toggle-power.png")
def toggle_display() -> bytes: return __read_icon("toggle-display.png")
def toggle_vu() -> bytes: return __read_icon("toggle-vu.png")
def volume_up() -> bytes: return __read_icon("volume-up.png")
def volume_down() -> bytes: return __read_icon("volume-down.png")
def play_pause() -> bytes: return __read_icon("play-pause.png")
def play_previous() -> bytes: return __read_icon("play-previous.png")
def play_next() -> bytes: return __read_icon("play-next.png")

def in_bluetooth() -> bytes: return __read_icon("in-bluetooth.png")
def in_coax() -> bytes: return __read_icon("in-coax.png")
def in_internal_player() -> bytes: return __read_icon("in-internal-player.png")
def in_optical() -> bytes: return __read_icon("in-optical.png")
def in_usb() -> bytes: return __read_icon("in-usb.png")
def out_analog_rca() -> bytes: return __read_icon("out-analog-rca.png")
def out_balxlr() -> bytes: return __read_icon("out-balxlr.png")
def out_hdmi() -> bytes: return __read_icon("out-hdmi.png")
def out_spdif() -> bytes: return __read_icon("out-spdif.png")
def out_usb_dac() -> bytes: return __read_icon("out-usb-dac.png")
def out_xlr_rca() -> bytes: return __read_icon("out-xlr-rca.png")
