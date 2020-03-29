#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FontForge Simplepolator V0.1
#
# Copyright (c) 2012, Dave Crossland (dave@understandingfonts.com)
# Copyright (c) 2012, Michal Nowakowski (miszka@limes.com.pl)
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
"""
A FontForge plug-in to generate interpolated instances from 2 characters.

Inspired by the Simplepolator FontLab/RoboFont script by Pablo Impallari
found at http://www.impallari.com/projects/overview/simplepolation
to easily apply the Gunnlaugur SE Briem's method
http://66.147.242.192/~operinan/2/2.3.3a/2.3.3.02.tests.htm

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
	print(str(message))

def simplepolate(registerobject, font):
	# Ask user how many children to create, default is 5
	amount = 5
	s = fontforge.askString("Simple Glyph Interpolation", "How many children?", str(amount))
	try:
		amount = int(s)
	except:
		fontforge.postError("Bad value", "Expected whole number")

	# figure out the interpolation amount floats based on how many children the user requested
	interpolationamount = [0.0]
	calcamount = amount +1
	x = 1.0 / calcamount
	for y in range(1, calcamount):
		interpolationamount.append(x*y)
	interpolationamount.append(1.0)

	# get the souce glyphs from the selection -- this should be simpler...
	glyphs = []
	for g in font.selection.byGlyphs:
		glyphs.append(g)
	source1 = glyphs[0]
	source2 = glyphs[1]

	# get a name for the children - font-name-generator.py supplies gibberish() so if we have that available, lets use it
	try: 
		name = gibberish(1)
	except Exception as e:
		name = "simplepolation"
	name = fontforge.askString("Simple Glyph Interpolation", "Children names?", str(name))

	# create all the children
	for x in range(amount+2):
		glyphname = str(name) + '.'+ str(x+1)
		g = font.createChar(-1, glyphname)
		g.preserveLayerAsUndo(1)
		# interpolate the top layer
		g.layers[1] = source1.layers[1].interpolateNewLayer(source2.layers[1], interpolationamount[x])
		# interpolate the width
		g.width = source1.width + (source2.width - source1.width)*interpolationamount[x]
		# interpolate the vwidth
		g.vwidth = source1.vwidth + (source2.vwidth - source1.vwidth)*interpolationamount[x]
		# let folks know what we did
		message = "Simplepolator created '%s' that is %s%% '%s' and %s%% '%s'" % (glyphname, int(100-interpolationamount[x]*100), source1.glyphname, int(interpolationamount[x]*100), source2.glyphname)
		note(message)

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
