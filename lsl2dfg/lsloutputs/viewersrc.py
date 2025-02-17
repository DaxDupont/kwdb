#!/usr/bin/env python

# viewersrc.py - This is a LSL2dfg.py output module generating function calls for lscript_compile.cpp viewer file.
#
# (C) Copyright 2013, 2024 Sei Lisa.
# Sei Lisa is the author's username in the Second Life(R) online virtual world.
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
# Second Life is a registered trademark of Linden Research, Inc.


import sys

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  version = "0.0.20140615000"

  def fpformat(s):
    s = str(float(s))
    if len(s) > 1 and s[-2:] == '.0':
      s = s[:-1]
    return s
  type2char = {"integer":"i", "float":"f", "string":"s", "key":"k", "vector":"v",
               "rotation":"q", "quaternion":"q", "list":"l", "bool":"i"}

  marker = "<<< %s KEYWORDS >>>" % tag

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
      if not line.startswith(marker):
        outf.write(line)
      else:
        outf.write("\n// Generated by LSL2 Derived Files Generator. Database version: %s; output module version: %s\n"
          % (databaseversion, version))

        for element in document:
          if element["cat"] == "function":
            delay = "0"
            energy = "10"
            if "delay" in element:
              delay = element["delay"]
            if "energy" in element:
              energy = element["energy"]
            delay = fpformat(delay)
            energy = fpformat(energy)

            rettype = "NULL"
            if "type" in element:
              rettype = '"' + type2char[element["type"]] + '"'

            params = "NULL"
            if "params" in element:
              params = '"'
              for param in element["params"]:
                params = params + type2char[param["type"]]
              params = params + '"'

            godmode = ""
            if "status" in element and element["status"] == "godmode":
              godmode = ", TRUE"

            outf.write('\taddFunction(%sf, %sf, dummy_func, "%s", %s, %s%s);\n'
              % (energy, delay, element["name"], rettype, params, godmode))

  finally:
    if outfilename is not None:
      outf.close()

pass
