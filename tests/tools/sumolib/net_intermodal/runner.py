#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2023 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    runner.py
# @author  Jakob Erdmann
# @date

from __future__ import absolute_import
from __future__ import print_function


import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
import sumolib.net  # noqa


def printSorted(d):
    return ' '.join(["%s:%s" % (k, d[k]) for k in sorted(d.keys())])


net = sumolib.net.readNet(sys.argv[1], withInternal=True, withLatestPrograms=True)
print("list of all edges")
for edge in net.getEdges():
    print(edge.getID())

print("list of internal edgeIDs of node 'C' (attribute)")
for edgeID in net.getNode("C").getInternal():
    print(edgeID)

print("list of internal edgeIDs of node 'C' (complete)")
node = net.getNode("C")
for edge in net.getEdges():
    if edge.getFromNode() == node and edge.getToNode() == node:
        print(edge.getID())

for laneID in ["SC_0", ":C_w2_0"]:
    lane = net.getLane(laneID)
    print("connections from %s:\n%s" % (
        lane.getID(),
        '\n'.join(list(map(str, lane.getOutgoing())))))
    print("outgoing internal lanes of %s: %s" % (
        lane.getID(), ' '.join(
            [net.getLane(c.getViaLaneID()).getID()
             if c.getViaLaneID() != "" else ""
             for c in lane.getOutgoing()])))

for laneID in ["CN_0", ":C_w2_0"]:
    lane2 = net.getLane(laneID)
    print("lanes to %s: %s" % (lane2.getID(), ' '.join(sorted([li.getID() for li in lane2.getIncoming()]))))

internal_edge = net.getEdge(":C_0")
internal_lane = net.getLane(":C_0_0")
internal_lane_cons = internal_lane.getOutgoing()
print("connections from %s:\n%s" % (internal_lane.getID(),
                                    '\n'.join(map(str, internal_lane_cons))))
internal_lane_incoming = sorted(internal_lane.getIncoming())
print("lanes to %s: %s" % (internal_lane.getID(),
                           ' '.join([li.getID() for li in internal_lane_incoming])))
assert(internal_edge.getFunction() == 'internal')
assert(internal_edge.isSpecial())
assert(internal_lane.getEdge().isSpecial())
assert(internal_edge.getFromNode().getID() == "C")
assert(internal_edge.getToNode().getID() == "C")

# params
print("edgeParams",     printSorted(net.getEdge("CE").getParams()))
print("laneParams",     printSorted(net.getLane("CE_0").getParams()))
print("laneParams",     printSorted(net.getLane("CE_1").getParams()))
print("junctionParams", printSorted(net.getNode("C").getParams()))
print("tlsParams",      printSorted(net.getTLS("C").getPrograms()["0"].getParams()))

# functions
print("getNeighboringEdges", ' '.join(sorted([e.getID() for e, _ in net.getNeighboringEdges(100, 0, 10)])))
print("getNeighboringLanes", ' '.join(sorted([ln.getID() for ln, _ in net.getNeighboringLanes(100, 0, 10)])))
print("getNeighboringNodes only for incoming edges",
      ' '.join(sorted([n.getID() for n in net.getNode("N").getNeighboringNodes(False, True)])))
print("getNeighboringNodes only for outgoing edges",
      ' '.join(sorted([n.getID() for n in net.getNode("S").getNeighboringNodes(True, False)])))
print("getNeighboringNodes", ' '.join(sorted([n.getID() for n in net.getNode("C").getNeighboringNodes()])))
