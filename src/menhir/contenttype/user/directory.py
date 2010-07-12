# -*- coding: utf-8 -*-

import grokcore.component as grok

from dolmen import content
from dolmen.app.content import icon
from dolmen.app.authentication.plugins import PrincipalFolderPlugin
from zope.container.interfaces import INameChooser
from menhir.contenttype.user import MF as _

class Directory(PrincipalFolderPlugin):
    icon("directory.png")
    content.name(_("User directory"))
    content.require('dolmen.security.ManageUsers')


class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        # here, raise UserError on some tests.
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
