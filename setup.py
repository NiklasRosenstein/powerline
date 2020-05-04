# automatically created by shore 0.0.22

import io
import re
import setuptools
import sys

with io.open('src/nr/powerline/__init__.py', encoding='utf8') as fp:
  version = re.search(r"__version__\s*=\s*'(.*)'", fp.read()).group(1)

with io.open('README.md', encoding='utf8') as fp:
  long_description = fp.read()

requirements = ['nr.databind.core >=0.0.6,<0.1.0', 'nr.databind.json >=0.0.6,<0.1.0', 'nr.interface >=0.0.2,<0.1.0', 'nr.sumtype >=0.0.3,<0.1.0', 'nr.utils.process >=0.0.3,<0.1.0']

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
    ]
  },
  cmdclass = {},
  keywords = [],
  classifiers = [],
)
