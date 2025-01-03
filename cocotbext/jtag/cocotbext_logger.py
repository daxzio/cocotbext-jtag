"""

Copyright (c) 2023-2025 Daxzio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import logging
from datetime import datetime
from typing import Union


class CocoTBExtLogger:
    def __init__(
        self, name: str = "default", enable: bool = True, start_year: int = 2023
    ) -> None:
        current_year = datetime.now().year
        if start_year == current_year:
            self.copyright_year = f"{start_year}"
        else:
            self.copyright_year = f"{start_year}-{current_year}"
        self.name = name
        self.log = logging.getLogger(f"cocotb.{self.name}")
        if enable:
            self.enable_logging()

    def siunits(self, value: Union[int, float]) -> str:
        if value >= 1000_000:
            return f"{value/1000000} M"
        elif value >= 1000:
            return f"{value/1000} k"
        else:
            return f"{value} "

    def enable_logging(self) -> None:
        self.log.setLevel(logging.DEBUG)

    def disable_logging(self) -> None:
        self.log.setLevel(logging.WARNING)
