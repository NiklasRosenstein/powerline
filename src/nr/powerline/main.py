
from __future__ import print_function
from . import daemon
from nr.utils.process import spawn_daemon
import argparse
import os


def default_powerline():
  from nr.powerline import PowerLine
  p = PowerLine()
  p.set_pen('white', 'magenta')
  p.add_part(' {c.DIRECTORY} {session.cwd} ')#!{c.RIGHT_TRIANGLE} ')
  git = p.get_plugin('git')
  if git.project:
    p.set_pen(None, 'blue')
    p.add_part(' {c.BRANCH} {git.branch} ')#!{c.RIGHT_TRIANGLE}')
  p.clear_pen()
  return p


def main(argv=None, prog=None):
  parser = argparse.ArgumentParser(prog=prog)
  parser.add_argument('--daemon', action='store_true')
  parser.add_argument('--detach', action='store_true')
  parser.add_argument('--client', action='store_true')
  parser.add_argument('--auto', action='store_true')
  args = parser.parse_args(argv)

  socket_file = os.path.expanduser('~/.local/powerline/daemon.sock')
  socket_conf = daemon.SocketConf.UnixFile(socket_file)
  if args.client or (args.auto and os.path.exists(socket_file)):
    print(daemon.PowerlineClient(socket_conf).request('.'), end='')
    return

  if args.daemon and os.path.exists(socket_file):
    return

  filename = os.getenv('NR_POWERLINE_SCRIPT', '')
  if filename:
    scope = {}
    with open(filename) as fp:
      exec(fp.read(), scope)
    powerline = scope['get_powerline']()
  else:
    powerline = default_powerline()

  def _run_daemon():
    os.makedirs(os.path.dirname(socket_file), exist_ok=True)
    daemon.PowerlineDaemon(socket_conf, powerline).run_forever()

  if args.daemon or args.auto:
    if args.detach or args.auto:
      spawn_daemon(_run_daemon)
    else:
      _run_daemon()
  if not args.daemon or args.auto:
    powerline.print_()
