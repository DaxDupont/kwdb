#!/usr/bin/env python

# constantvaluecheck.py - This is a LSL2dfg.py output module to generate a script
# that checks the values of the constants in the database.
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
      if not line.startswith("<<< %s KEYWORDS >>>" % tag):
        outf.write(line.encode('utf8'))
      else:
        outf.write('llOwnerSay("Generated by LSL2 Derived Files Generator. Database version: %s; output module version: %s");\n'
          % (databaseversion, version))

        opened = False
        count = 0
        for element in document:
          if element['cat'] == 'constant':
            if opened:
              outf.write(",")
            else:
              outf.write('c([\n')
              opened = True
            name = element['name']
            val = element['value']
            qval = val.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
            if element['type'] == 'key':
              fmtstr = '(key)"%(qval)s",%(name)s\n'
            elif element['type'] == 'string':
              fmtstr = '"%(qval)s",%(name)s\n'
            else:
              fmtstr = '%(val)s,%(name)s\n'
            
            try:
              outf.write((fmtstr % {'name': name, 'val': val, 'qval': qval}).encode('ascii'))
            except UnicodeEncodeError:
              escapeval = ''.join("%%%02X" % ord(c) for c in val.encode('utf8'))
              outf.write('llUnescapeURL("%(escapeval)s"),%(name)s\n' % {'name': name, 'escapeval': escapeval})

            count = count + 1
            if count >= 20: # long enough to save memory and short enough for the sublists to fit in memory
              outf.write(']);\n')
              opened = False
              count = 0

        if opened:
          outf.write(']);\n')

  finally:
    if outfilename is not None:
      outf.close()

pass
