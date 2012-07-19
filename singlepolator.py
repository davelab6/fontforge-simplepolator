#!/usr/bin/python
# -*- coding: utf-8 -*-
# FontForge Singlepolator V0.1-git
#
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
#
# A simple macro to interpolate compatible glyphs inside FontForge
# To easily apply the Gunnlaugur SE Briem's method
# http://66.147.242.192/~operinan/2/2.3.3a/2.3.3.02.tests.htm
"""
Go to FontForge, File -> Preferences -> Script Menu, and add this
script file with Menu Name Singlepolate, and locate this file with
the [...] button.

Now select 3 cells, the first two containing source glyphs, the last 
one an empty encoding slot where the interpolated output will land. 
Then File, Script Menu, Singlepolate, input interpolation 
amount -- and voila.
"""
import fontforge

f = fontforge.activeFont()

amount = 0.461
isOk = True


if fontforge.hasUserInterface():
	s = fontforge.askString("Interpolate glyphs", "Please specify interpolation factor:", str(amount))
	try:
		amount = float(s)
	except:
		fontforge.postError("Bad value", "Expected number")
		isOk = False

if isOk:
	state = 1
	g1 = ""
	g2 = ""

	for enc in f.selection:
		print enc
		g = f.createMappedChar(enc)

		if state == 1:
				g1 = g
				state = 2
		elif state == 2:
				g2 = g
				state = 3
		else:
				g.preserveLayerAsUndo(1)
				g.layers[1] = g1.layers[1].interpolateNewLayer(g2.layers[1], amount)
				g.width = g1.width + (g2.width - g1.width)*amount
				g.vwidth = g1.vwidth + (g2.vwidth - g1.vwidth)*amount
				state = 1
