#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2023 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    test.py
# @author  Pablo Alvarez Lopez
# @date    2016-11-25

# import common functions for netedit tests
import os
import sys

testRoot = os.path.join(os.environ.get('SUMO_HOME', '.'), 'tests')
neteditTestRoot = os.path.join(
    os.environ.get('TEXTTEST_HOME', testRoot), 'netedit')
sys.path.append(neteditTestRoot)
import neteditTestFunctions as netedit  # noqa

# Open netedit
neteditProcess, referencePosition = netedit.setupAndStart(neteditTestRoot)

# recompute
netedit.rebuildNetwork()

# go to additional mode
netedit.additionalMode()

# select E2
netedit.changeElement("multiLaneAreaDetector")

# create E2 with default parameters
netedit.leftClick(referencePosition, 190, 250)
netedit.leftClick(referencePosition, 440, 250)
netedit.typeEnter()

# go to additional mode
netedit.inspectMode()

# inspect E2
netedit.leftClick(referencePosition, 320, 250)

# Change parameter frequency with a non valid value (non numeral)
netedit.modifyAttribute(netedit.attrs.E2Multilane.inspect.period, "dummyFrequency", True)

# Change parameter frequency with a non valid value (negative)
netedit.modifyAttribute(netedit.attrs.E2Multilane.inspect.period, "-100", True)

# Change parameter frequency with a valid value
netedit.modifyAttribute(netedit.attrs.E2Multilane.inspect.period, "120", True)

# Check undo redo
netedit.undo(referencePosition, 2)
netedit.redo(referencePosition, 2)

# save netedit config
netedit.saveNeteditConfig(referencePosition)

# quit netedit
netedit.quit(neteditProcess)
