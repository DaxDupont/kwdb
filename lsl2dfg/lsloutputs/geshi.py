#!/usr/bin/env python

# geshi.py - This is a LSL2dfg.py output module for GeSHi PHP Generic Syntax Highlighting.
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

# Python3 does not have this function, so this replaces it with equivalent behavior.
def cmp(a, b):
  return (a > b) - (a < b)

def output(document, defaultdescs, databaseversion, infilename, outfilename, lang, tag):

  version = "0.0.20230603000"

  keywords = []
  types = []
  constants = []
  functions = []
  events = []
  deprecated = []
  unimplemented = []
  godmode = []

  for element in document:
    if element["cat"] == "keyword":
      if "status" not in element or element["status"] == "normal":
        if element["name"] not in ("default", "print"):
          keywords.append(element["name"])
        else:
          functions.append(element["name"])
      elif element["status"] in ("deprecated", "unimplemented"):
        unimplemented.append(element["name"])
      else:
        raise Exception("Unknown status in '%s' keyword: %s" % (element["name"], element["status"]))
    elif element["cat"] == "type":
      types.append(element["name"])
    elif element["cat"] == "constant":
      if "status" not in element or element["status"] == "normal":
        constants.append(element["name"])
      elif element["status"] in ("deprecated", "unimplemented"):
        deprecated.append(element["name"])
      else:
        raise Exception("Unknown status in '%s' constant: %s" % (element["name"], element["status"]))
    elif element["cat"] == "function":
      if "status" in element:
        if element["status"] == "deprecated":
          deprecated.append(element["name"])
        elif element["status"] == "unimplemented":
          unimplemented.append(element["name"])
        elif element["status"] == "godmode":
          godmode.append(element["name"])
        elif element["status"] == "normal":
          functions.append(element["name"])
        else:
          raise Exception("Unknown status: " + element["status"])
      else:
        functions.append(element["name"])
    elif element["cat"] == "event":
      events.append(element["name"])

  keywords.sort()
  types.sort()
  constants.sort()
  try:
    functions.sort(key=lambda x: x.lower())
  except:
    functions.sort(lambda x,y: cmp(x.lower(), y.lower()))
  events.sort()
  deprecated.sort()
  unimplemented.sort()
  godmode.sort()

  if infilename is not None:
    inf = open(infilename, "r")
  else:
    inf = sys.stdin

  try:
    geshi = inf.readlines()

  finally:
    if infilename is not None:
      inf.close()

  if outfilename is not None:
    outf = open(outfilename, "w")
  else:
    outf = sys.stdout

  try:

    for line in geshi:
      if line.startswith("<<< %s KEYWORDS VERSION >>>" % tag):
        outf.write(" * Generated by LSL2 Derived Files Generator.\n * Database version: %s; output module version: %s\n"
          % (databaseversion, version))
      elif line.startswith("<<< %s KEYWORDS KEYWORDS >>>" % tag):
        for element in keywords:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS CONSTANTS >>>" % tag):
        for element in constants:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS EVENTS >>>" % tag):
        for element in events:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS TYPES >>>" % tag):
        for element in types:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS FUNCTIONS >>>" % tag):
        for element in functions:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS DEPRECATED >>>" % tag):
        for element in deprecated:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS UNIMPLEMENTED >>>" % tag):
        for element in unimplemented:
          outf.write("            '" + element + "',\n")
      elif line.startswith("<<< %s KEYWORDS GODMODE >>>" % tag):
        for element in godmode:
          outf.write("            '" + element + "',\n")
      else:
        outf.write(line)

  finally:
    if outfilename is not None:
      outf.close()

pass
