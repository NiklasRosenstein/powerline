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

default_powerline = {
  'plugins': [
    {
      'type': 'text',
      'text': ' ● ',
      'is-server-indicator': True,
      'style': 'red black bold',
      'indicator-style': 'green black bold'
    },
    {
      'type': 'venv',
      'style': 'bg:black italic'
    },
    {
      'type': 'cwd',
      'breadcrumbs': {}
    },
    {
      'type': 'git',
      'icons': None
    },
    {
      'type': 'text',
      'text': ' $ ',
      'is-status-indicator': True
    }
  ]
}

bash_src = '''
_POWERLINE_ALT="$PS1"
function _powerline_make_request() {
  local payload
  payload=$(jq -n --arg pwd "$PWD" --arg ec "$1" --arg env "$(env)" '{path: $pwd, exit_code: $ec, environ: $env}' 2>/dev/null)
  if [[ $? != 0 ]]; then
    payload='{"path": "'"$PWD"'", "exit_code": '"$1"'}'
  fi
  echo "$payload" | nc -U ~/.local/powerline/daemon.sock 2>/dev/null
  return $?
}
function _powerline_bootstrapper() {
  _powerline_make_request $1
  if [ $? != 0 ]; then
    if which nr-powerline >/dev/null; then
      nr-powerline --start
      if ! ( nr-powerline --status --exit-code >/dev/null ); then
        2> echo "Could not start powerline daemon."
        echo "$_POWERLINE_ALT"
      else
        _powerline_make_request $1
      fi
    else
      echo "$_POWERLINE_ALT"
    fi
  fi
}
function _update_ps1() {
  PS1="`_powerline_bootstrapper $?` "
}
if [[ $TERM != linux && ! $PROMPT_COMMAND =~ _update_ps1 ]]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi
'''
