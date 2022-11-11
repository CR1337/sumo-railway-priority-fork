/****************************************************************************/
// Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
// Copyright (C) 2001-2022 German Aerospace Center (DLR) and others.
// This program and the accompanying materials are made available under the
// terms of the Eclipse Public License 2.0 which is available at
// https://www.eclipse.org/legal/epl-2.0/
// This Source Code may also be made available under the following Secondary
// Licenses when the conditions for such availability set forth in the Eclipse
// Public License 2.0 are satisfied: GNU General Public License, version 2
// or later which is available at
// https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
// SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later
/****************************************************************************/
/// @file    GNEMeanData.cpp
/// @author  Pablo Alvarez Lopez
/// @date    Nov 2022
///
// Class for representing MeanData
/****************************************************************************/
#include <config.h>

#include <netedit/GNENet.h>
#include <netedit/GNEViewNet.h>
#include <netedit/GNEViewParent.h>
#include <netedit/elements/data/GNEMeanData.h>
#include <netedit/frames/common/GNESelectorFrame.h>
#include <netedit/frames/data/GNEEdgeDataFrame.h>
#include <utils/gui/div/GLHelper.h>
#include <utils/gui/div/GUIParameterTableWindow.h>
#include <utils/gui/globjects/GLIncludes.h>
#include <utils/gui/globjects/GUIGLObjectPopupMenu.h>
#include <utils/gui/div/GUIDesigns.h>

#include "GNEMeanData.h"
#include "GNEDataInterval.h"


// ===========================================================================
// member method definitions
// ===========================================================================

// ---------------------------------------------------------------------------
// GNEMeanData - methods
// ---------------------------------------------------------------------------

GNEMeanData::GNEMeanData(const SumoXMLTag tag, FXIcon* icon, const GUIGlObjectType type, GNEDataInterval* dataIntervalParent,
                               const Parameterised::Map& parameters,
                               const std::vector<GNEJunction*>& junctionParents,
                               const std::vector<GNEEdge*>& edgeParents,
                               const std::vector<GNELane*>& laneParents,
                               const std::vector<GNEAdditional*>& additionalParents,
                               const std::vector<GNEDemandElement*>& demandElementParents,
                               const std::vector<GNEMeanData*>& genericDataParents) :
    GUIGlObject(),
    Parameterised(parameters),
    GNEHierarchicalElement(dataIntervalParent->getNet(), tag, junctionParents, edgeParents, laneParents, additionalParents, demandElementParents, genericDataParents) {
}


GNEMeanData::~GNEMeanData() {}


GUIGlObject*
GNEMeanData::getGUIGlObject() {
    return this;
}


GUIGLObjectPopupMenu*
GNEMeanData::getPopUpMenu(GUIMainWindow& app, GUISUMOAbstractView& parent) {
    GUIGLObjectPopupMenu* ret = new GUIGLObjectPopupMenu(app, parent, *this);
    // build header
    buildPopupHeader(ret, app);
    // build menu command for center button and copy cursor position to clipboard
    buildCenterPopupEntry(ret);
    buildPositionCopyEntry(ret, app);
    // buld menu commands for names
    GUIDesigns::buildFXMenuCommand(ret, "Copy " + getTagStr() + " name to clipboard", nullptr, ret, MID_COPY_NAME);
    GUIDesigns::buildFXMenuCommand(ret, "Copy " + getTagStr() + " typed name to clipboard", nullptr, ret, MID_COPY_TYPED_NAME);
    new FXMenuSeparator(ret);
    // build selection and show parameters menu
    buildShowParamsPopupEntry(ret);
    // show option to open additional dialog
    if (myTagProperty.hasDialog()) {
        GUIDesigns::buildFXMenuCommand(ret, ("Open " + getTagStr() + " Dialog").c_str(), getACIcon(), &parent, MID_OPEN_ADDITIONAL_DIALOG);
        new FXMenuSeparator(ret);
    } else {
        GUIDesigns::buildFXMenuCommand(ret, ("Cursor position in view: " + toString(getPositionInView().x()) + "," + toString(getPositionInView().y())).c_str(), nullptr, nullptr, 0);
    }
    return ret;
}


GUIParameterTableWindow*
GNEMeanData::getParameterWindow(GUIMainWindow& app, GUISUMOAbstractView& /* parent */) {
    // Create table
    GUIParameterTableWindow* ret = new GUIParameterTableWindow(app, *this);
    // Iterate over attributes
    for (const auto& tagProperty : myTagProperty) {
        // Add attribute and set it dynamic if aren't unique
        if (tagProperty.isUnique()) {
            ret->mkItem(tagProperty.getAttrStr().c_str(), false, getAttribute(tagProperty.getAttr()));
        } else {
            ret->mkItem(tagProperty.getAttrStr().c_str(), true, getAttribute(tagProperty.getAttr()));
        }
    }
    // close building
    ret->closeBuilding();
    return ret;
}


void
GNEMeanData::deleteGLObject() {
    myNet->deleteMeanData(this, myNet->getViewNet()->getUndoList());
}


void
GNEMeanData::selectGLObject() {
    if (isAttributeCarrierSelected()) {
        unselectAttributeCarrier();
    } else {
        selectAttributeCarrier();
    }
    // update information label
    myNet->getViewNet()->getViewParent()->getSelectorFrame()->getSelectionInformation()->updateInformationLabel();
}


void
GNEMeanData::updateGLObject() {
    updateGeometry();
}


const Parameterised::Map&
GNEMeanData::getACParametersMap() const {
    return getParametersMap();
}

/****************************************************************************/