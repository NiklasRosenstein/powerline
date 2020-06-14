# This file was automatically generated by Shore. Do not edit manually.
# For more information on Shore see https://pypi.org/project/nr.shore/

from __future__ import print_function
import io
import os
import re
import setuptools
import sys

with io.open('src/nr/powerline/__init__.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

readme_file = 'README.md'
if os.path.isfile(readme_file):
  with io.open(readme_file, encoding='utf8') as fp:
    long_description = fp.read()
else:
  print("warning: file \"{}\" does not exist.".format(readme_file), file=sys.stderr)
  long_description = None

requirements = ['nr.ansiterm >=0.0.1,<0.1.0', 'nr.databind.core >=0.0.6,<0.1.0', 'nr.databind.json >=0.0.6,<0.1.0', 'nr.interface >=0.0.2,<0.1.0', 'nr.sumtype >=0.0.3,<0.1.0', 'nr.utils.process >=0.0.3,<0.1.0']

setuptools.setup(
  name = 'nr.powerline',
  version = version,
  author = 'Niklas Rosenstein',
  author_email = 'rosensteinniklas@gmail.com',
  description = 'Package description here.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  url = 'https://git.niklasrosenstein.com/NiklasRosenstein/powerline',
  license = 'MIT',
  packages = setuptools.find_packages('src', ['test', 'test.*', 'docs', 'docs.*']),
  package_dir = {'': 'src'},
  include_package_data = True,
  install_requires = requirements,
  extras_require = {},
  tests_require = [],
  python_requires = None, # TODO: '>=3.5,<4.0.0',
  data_files = [],
  entry_points = {
    'console_scripts': [
      'nr-powerline = nr.powerline:main',
    ],
    'nr.powerline.plugins': [
      'cwd = nr.powerline.cwd:CwdPlugin',
      'git = nr.powerline.git:GitPlugin',
      'text = nr.powerline.text:TextPlugin',
      'venv = nr.powerline.venv:VenvPlugin',
    ]
  },
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
