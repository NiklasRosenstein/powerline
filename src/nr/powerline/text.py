# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2020, Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# this software and associated documentation files (the "Software"), to deal in
# Software without restriction, including without limitation the rights to use,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the
# and to permit persons to whom the Software is furnished to do so, subject to
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# USE OR OTHER DEALINGS IN THE SOFTWARE.

from . import chars, Pen, PowerlineContext, PowerlinePlugin
from nr import ansiterm as ansi
from nr.databind.core import Field, FieldName, Struct
from nr.interface import implements, override
from typing import Iterable, List


@implements(PowerlinePlugin)
class TextPlugin(Struct):
  style = Field(ansi.Style, default=None)
  is_status_indicator = Field(bool, FieldName('is-status-indicator'), default=False)
  bad_status_style = Field(ansi.Style, default=ansi.parse_style('bg:red bold'))
  text = Field(str)

  @override
  def render(self, context: PowerlineContext) -> Iterable[Pen]:
    if self.is_status_indicator and context.exit_code != 0:
      style = self.bad_status_style
    else:
      style = self.style or context.default_style
    yield Pen.Text(self.text, style)
    yield Pen.Flipchar(chars.RIGHT_TRIANGLE)
