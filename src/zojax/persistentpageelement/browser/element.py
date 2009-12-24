##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.component import getMultiAdapter
from zope.traversing.browser import absoluteURL

from z3c.form.interfaces import IFieldWidget, IActionHandler

from zojax.wizard.button import WizardButton
from zojax.layoutform import button, Fields, PageletEditSubForm
from zojax.content.forms.form import AddForm
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.content.forms.interfaces import IEditContentWizard
from zojax.persistentpageelement.interfaces import _, IPersistentPageElement


def customWidget(field, request):
    widget = getMultiAdapter((field, request), IFieldWidget)

    widget.rows = 30
    widget.style = u'width: 98%; font-family: monospace; font-size: 130%'

    return widget


class AddPageElementForm(AddForm):

    fields = Fields(IPersistentPageElement)
    fields['source'].widgetFactory = customWidget


class EditPageElementForm(PageletEditSubForm):

    fields = Fields(IPersistentPageElement).omit('title', 'description')
    fields['source'].widgetFactory = customWidget

    def update(self):
        super(EditPageElementForm, self).update()

        if self.context.errors:
            IStatusMessage(self.request).add(self.context.errors[1], 'error')


# back action
class BackButton(WizardButton):

    def actionHandler(self):
        return self.wizard.redirect('%s/'%absoluteURL(
                self.wizard.__parent__.__parent__, self.request))


backButton = BackButton(title = _(u'Back'), weight = 502)
