# -*- coding: utf-8 -*-

import grokcore.component as grok
import dolmen.content
from dolmen.app.authentication.plugins import PrincipalFolderPlugin
from zope.container.interfaces import INameChooser
from zope.exceptions.interfaces import UserError
from zope.pluggableauth.interfaces import IAuthenticatorPlugin


class IDirectory(IAuthenticatorPlugin):
    """Marker interface.
    """


class Directory(PrincipalFolderPlugin):
    #dolmen.content.icon("directory.png")
    dolmen.content.name("User directory")
    dolmen.content.require('dolmen.security.ManageUsers')
    grok.implements(IDirectory)
    

class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        # here, raise UserError on some tests.
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
