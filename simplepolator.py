#!/usr/bin/python
# -*- coding: utf-8 -*-
# FontForge Simplepolator V0.1-git
#
# Copyright (c) 2012, Dave Crossland (dave@understandingfonts.com)
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#   EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Inspired by the Simplepolator FontLab/RoboFont script 
# by Pablo Impallari  - www.impallari.com/projects/overview/simplepolation
#
# A simple macro to interpolate compatible glyphs inside FontLab.
# To easily apply the Gunnlaugur SE Briem's method
# http://66.147.242.192/~operinan/2/2.3.3a/2.3.3.02.tests.htm
"""
A FontForge plug-in to generate 5 interpolated instances from 2 characters.

Copy to ~/.FontForge/python/ and then find "Simplepolator" in the Tools menu,
active when 2 characters are selected.
"""

import fontforge

def copyAndPaste(font, source, target):
	font.selection.select(source)
	font.copy()
	font.selection.select(target)
	font.paste()

def note(message):
	fontforge.logWarning(str(message))
	print str(message)

def simplepolate(registerobject, font):
	note("get the first 2 glyphs")
	font = fontforge.activeFont()
	glyphs = []
	for g in font.selection.byGlyphs:
	  glyphs.append(g)
	source1 = glyphs[0]
	source2 = glyphs[1]

	note("interpolate 3 new glyphs")
	try: 
		out1 = font.createInterpolatedGlyph(source1,source2,0.25)
		out2 = font.createInterpolatedGlyph(source1,source2,0.50)
		out3 = font.createInterpolatedGlyph(source1,source2,0.75)
	except EnvironmentError as string:
		note(str(string))

	note("create 5 new characters")
	for x in range(1,6):
		font.createChar(-1,"interpolation.%s" % x)

	note("create 5 new glyphs")
	try:
		copyAndPaste(font, source1, "interpolation.1")
		copyAndPaste(font, out1, "interpolation.2")
		copyAndPaste(font, out2, "interpolation.3")
		copyAndPaste(font, out3, "interpolation.4")
		copyAndPaste(font, source2, "interpolation.5")
	except:
		pass

# Only enable Tool menu item if 2 characters are selected
def shouldWeAppear(registerobject, font):
	font = fontforge.activeFont()
	glyphs = []
	for g in font.selection.byGlyphs:
	  glyphs.append(g)
	if len(glyphs) == 2:
		return True
	else:
		return False

# Register this PlugIn in the Tools menu
if fontforge.hasUserInterface():
	#  keyShortcut="Ctl+Shft+n"
	keyShortcut = None
	menuText = "Simplepolate"
	fontforge.registerMenuItem(simplepolate,shouldWeAppear,None,"Font",keyShortcut,menuText);