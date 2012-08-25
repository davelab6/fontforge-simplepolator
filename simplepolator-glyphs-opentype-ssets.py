#!/usr/bin/python
# -*- coding: utf-8 -*-
# FontForge Simplepolator Glyphs OpenType V0.3
#
# Copyright (c) 2012, Dave Crossland (dave@understandingfonts.com)
# Copyright (c) 2012, Michal Nowakowski (miszka@limes.com.pl)
# Copyright (c) 2012, Khaled Hosney (khaledhosny@eglug.org)
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
A FontForge plug-in to generate interpolated instances from 2 characters,
and assign them as Stylistic Set variants of the first character.

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
    print str(message)

def simplepolate(registerobject, font):
    # Ask user how many children to create, default is 5
    amount = 5
    s = fontforge.askString("Simplepolate", "How many children? (1-8)", str(amount))
    try:
        amount = int(s)
    except:
        fontforge.postError("Bad value", "Expected whole number")
        return
    if 1 <= amount >= 9:
            fontforge.postError("Bad value", "1 to 9, please")
            return

    # figure out the interpolation amount floats based on how many children the user requested
    interpolationamount = []
    calcamount = amount +1
    x = 1.0 / calcamount
    for y in range(1, calcamount):
        interpolationamount.append(x*y)
    interpolationamount.append(1.0)

    # get the souce glyphs from the selection -- this would be simpler in robofab :)
    glyphs = []
    for g in font.selection.byGlyphs:
        glyphs.append(g)
    source1 = glyphs[0]
    source2 = glyphs[1]

    name = source1.glyphname
    print "Adding %s Style Sets to %s" % (amount, name)

    # create all the children
    for x in range(amount+1):
        # create the style set name
        ss = 'ss'+ str(x+1).zfill(2)
        glyphname = str(name) + '.' + ss
        # create a char slot
        g = font.createChar(-1, glyphname)
        # make this undoable
        g.preserveLayerAsUndo(1)
        # interpolate the top layer
        g.layers[1] = source1.layers[1].interpolateNewLayer(source2.layers[1], interpolationamount[x])
        # interpolate the width
        g.width = source1.width + (source2.width - source1.width)*interpolationamount[x]
        # interpolate the vwidth
        g.vwidth = source1.vwidth + (source2.vwidth - source1.vwidth)*interpolationamount[x]        

        # add lookup for each ss, eg ss01, if it doesn't already exist
        lookup = str(ss)
        if lookup not in font.gsub_lookups:
            flags = ("","")
            featureScriptLangTuple = ((lookup,(("latn",("dflt")),)),)
            # featureScriptLangTuple = (('ss07', (('latn', 'dflt'),)),)
            font.addLookup(lookup, "gsub_single",   (), featureScriptLangTuple)

        # check for existing subtables
        if len(font.getLookupSubtables(lookup)) == 0:
            subtable = lookup + '-0'
            font.addLookupSubtable(lookup, subtable)
        else:
            subtable = font.getLookupSubtables(lookup)[0]
        # add the substitution
        source1.addPosSub(subtable,glyphname)

        # merge the subtables (thanks to khaled hosney for this!)
        for lookup in font.gsub_lookups:
            while 1 < len(font.getLookupSubtables(lookup)):
                font.mergeLookupSubtables(font.getLookupSubtables(lookup)[1], font.getLookupSubtables(lookup)[0])
        
        # let folks know what we did
        message = "  Created %s %s%%/%s%% %s/%s (%s:%s)" % (glyphname, int(100-interpolationamount[x]*100), int(interpolationamount[x]*100), source1.glyphname, source2.glyphname, lookup, subtable)
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
    menuText = "Simplepolate 2 Glyphs"
    fontforge.registerMenuItem(simplepolate,shouldWeAppear,None,"Font",keyShortcut,menuText);
