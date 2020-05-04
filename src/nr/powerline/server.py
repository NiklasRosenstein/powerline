# -*- coding: utf8 -*-
# Copyright (c) 2020 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import json
import nr.sumtype
import os
import socket as _socket
import traceback

from nr.databind.core import Field, Struct
from nr.databind.json import JsonMixin


class Request(Struct, JsonMixin):
  path = Field(str)
  escape_unprintable = Field(bool, default=True)
  exit_code = Field(int, default=0)


class Address(nr.sumtype.Sumtype):
  Ipv4 = nr.sumtype.Constructor('host,port')
  UnixFile = nr.sumtype.Constructor('filename')

  @Ipv4.member
  def type(self) -> int:
    return _socket.AF_INET

  @UnixFile.member
  def type(self) -> int:
    return _socket.AF_UNIX

  @Ipv4.member
  def bind(self, socket: _socket.socket):
    socket.bind((self.host, self.port))

  @Ipv4.member
  def connect(self, socket: _socket.socket):
    socket.connect((self.host, self.port))

  @UnixFile.member
  def bind(self, socket: _socket.socket):
    socket.bind(self.filename)

  @UnixFile.member
  def connect(self, socket: _socket.socket):
    socket.connect(self.filename)


class PowerlineServer:

  def __init__(self, conf: Address, powerline: 'Powerline') -> None:
    self._conf = conf
    self._powerline = powerline

  def run_forever(self):
    socket = _socket.socket(self._conf.type())
    self._conf.bind(socket)
    socket.listen(5)
    socket.settimeout(0.1)
    try:
      while True:
        try:
          conn, address = socket.accept()
        except _socket.timeout:
          continue
        self._handle_connection(conn, address)
    finally:
      socket.close()
      if isinstance(self._conf, Address.UnixFile):
        os.remove(self._conf.filename)

  def _handle_connection(self, conn, address):
    from . import PowerlineContext

    try:
      request = Request.from_json(json.loads(conn.makefile().readline().strip()))
      context = PowerlineContext(request.path, request.exit_code)
      result = self._powerline.render(context,
        escape_unprintable=request.escape_unprintable)
    except Exception as exc:
      result = traceback.format_exc()

    conn.makefile('w').write(result)
    conn.close()