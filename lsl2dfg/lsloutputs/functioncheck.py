#!/usr/bin/env python

# constantvaluecheck.py - This is a LSL2dfg.py output module to generate a script
# that checks the existance of functions and that they accept the number and
# type of parameters they claim, and that their return value, when it exists, can
# be assigned to a variable of the given type.
#
# (C) Copyright 2013 Sei Lisa.
# Sei Lisa is the author's username in the Second Life online virtual world.
#
# This file is part of LSL2 Derived Files Generator.
#
#    LSL2 Derived Files Generator is free software: you can redistribute it
#    and/or modify it under the terms of the GNU Lesser General Public License
#    as published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    LSL2 Derived Files Generator is distributed in the hope that it will be
#    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with LSL2 Derived Files Generator. If not, see
#    <http://www.gnu.org/licenses/>.
#
# Second Life is a trademark of Linden Research, Inc.


import sys

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  version = "0.0.20130627000"

  if infilename is not None:
    inf = open(infilename, "r")
  else:
    inf = sys.stdin

  try:
    inputlines = inf.readlines()

  finally:
    if infilename is not None:
      inf.close()

  if outfilename is not None:
    outf = open(outfilename, "w")
  else:
    outf = sys.stdout

  try:

    for line in inputlines:
      if line.startswith("<<< %s HEADER >>>" % tag):
        outf.write('llOwnerSay("Generated by LSL2 Derived Files Generator. Database version: %s; output module version: %s");\n'
          % (databaseversion, version))

      elif line.startswith("<<< %s KEYWORDS >>>" % tag):

        count = 0
        for element in document:
          if element['cat'] == 'function':
            name = element['name']
            paramstr = ''
            if 'params' in element:
              first = True
              for param in element['params']:
                if first:
                  first = False
                else:
                  paramstr = paramstr + ','
                paramstr = paramstr + param['type'][0]
            retvalchecker = ''
            if 'type' in element:
              retvalchecker = element['type'][0] + ' = '

            outf.write("%s%s(%s);\n" % (retvalchecker, name, paramstr))
      else:
        outf.write(line.encode('utf8'))

  finally:
    if outfilename is not None:
      outf.close()

pass
