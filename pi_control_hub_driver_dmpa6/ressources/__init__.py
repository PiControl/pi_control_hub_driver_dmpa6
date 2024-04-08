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
__piirc_filepath = os.path.join(__directory, "eversolo-dmpa6.json")
__piirc_config: str = None

def get_piirc_config() -> str:
    global __piirc_config
    if __piirc_config is None:
        with open(__piirc_filepath, encoding="utf-8") as f:
            file_content: str = f.read()
            __piirc_config = file_content

    return __piirc_config


