#!/usr/bin/python
# -*- coding: utf-8 -*-
# FontForge Simplepolator Fonts V0.3-git
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
THIS DOESN"T WORK YET :(

A FontForge plug-in to generate interpolated instances from 2 fonts.

Inspired by the Simplepolator FontLab/RoboFont script by Pablo Impallari
found at http://www.impallari.com/projects/overview/simplepolation
to easily apply the Gunnlaugur SE Briem's method
http://66.147.242.192/~operinan/2/2.3.3a/2.3.3.02.tests.htm

Copy to ~/.FontForge/python/ and then find "Simplepolate Fonts" in the Tools menu,
when 2 fonts are selected.
"""

import fontforge

def note(message):
	fontforge.logWarning(str(message))
	print str(message)

def simplepolateFonts(registerobject, font):
	# Ask user how many children to create, default is 5
	amount = 5
	s = fontforge.askString("Simple Font Interpolation", "How many children?", str(amount))
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

        # TODO: This should ask the user to choose which is source1 and source2
	# get the souce fonts from the 2 currently open (check for only 2 open is in shouldWeAppear())
	fonts = fontforge.fonts()
        source1 = fonts[0]
	source2 = fonts[1]

	# get a name for the children - font-name-generator.py supplies gibberish() so if we have that available, lets use it
	name = source1.familyname + " Simp"
	newName = fontforge.askString("Simplepolate Fonts", "Base family name?", str(name))
        
        # create all the children
	for x in range(amount+2):
	        # TODO I thought this would work but it doesn't
		# newFont = source1.interpolateFonts(interpolationamount[x],source2.path)
		# TODO and I thought this would work because it does on its own, but if its even just repeated twice right next to each other, it doesn't work!! :(
                source1.interpolateFonts(interpolationamount[x],source2.path)
                newFontName = newName + ' ' + str(int(interpolationamount[x]*100)).zfill(3)
                newFont = fontforge.activeFont()
                # Set PostScript Style Name (FamilyName-Style)
		newFont.weight = "Regular"
		newFont.fontname = newFontName.replace(' ', '') + '-' + newFont.weight
		# Set PostScript Family Name (Family Name)
		newFont.familyname = newFontName
		# Set PostScript Full Name (Family Name Style)
		newFont.fullname = newFontName + ' ' + font.weight
		# let folks know what we did
                message = "Simplepolated %s: %s%%/%s%% %s/%s" % (newFont.fullname, int(100-interpolationamount[x]*100), int(interpolationamount[x]*100), source1.fontname, source2.fontname)
		note(message)

# Only enable Tool menu item if 2 characters are selected
def shouldWeAppear(registerobject, font):
	fonts = fontforge.fonts()
	if len(fonts) == 2:
		return True
	else:
		return False

# Register this PlugIn in the Tools menu
if fontforge.hasUserInterface():
	#  keyShortcut="Ctl+Shft+n"
	keyShortcut = None
	menuText = "Simplepolate Fonts"
	fontforge.registerMenuItem(simplepolateFonts,shouldWeAppear,None,"Font",keyShortcut,menuText);