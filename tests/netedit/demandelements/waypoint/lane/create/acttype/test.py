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
# @date    2019-07-16

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

# go to demand mode
netedit.supermodeDemand()

# go to waypoint mode
netedit.stopMode()

# change waypoint type with a valid value
netedit.changeStopType("waypointLane")

# set invalid value
netedit.changeDefaultValue(netedit.attrs.waypointLane.create.actType, ";;;;;;;;;;")

# try to create waypoint
netedit.leftClick(referencePosition, 400, 185)

# set invalid value
netedit.changeDefaultValue(netedit.attrs.waypointLane.create.actType, "")

# try to create waypoint
netedit.leftClick(referencePosition, 390, 185)

# set valid value
netedit.changeDefaultValue(netedit.attrs.waypointLane.create.actType, "dummy Act")

# create waypoint
netedit.leftClick(referencePosition, 380, 185)

# set valid value
netedit.changeDefaultValue(netedit.attrs.waypointLane.create.actType, "singing")

# create waypoint
netedit.leftClick(referencePosition, 370, 185)

# Check undo redo
netedit.undo(referencePosition, 2)
netedit.redo(referencePosition, 2)

# save Netedit config
netedit.saveNeteditConfig(referencePosition)

# quit netedit
netedit.quit(neteditProcess)
