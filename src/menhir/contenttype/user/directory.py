# -*- coding: utf-8 -*-

import grok
import dolmen.content as content
from dolmen.app.authentication import IUserDirectory
from zope.schema import ValidationError
from zope.app.container.interfaces import INameChooser


class DuplicatedLogin(ValidationError):
    __doc__ = u"This username is already in use."
    

class Directory(content.Container):
    grok.implements(IUserDirectory)
    content.icon("directory.png")
    content.name("User directory")
    content.schema(content.IBaseContent)
    content.require('dolmen.security.ManageUsers')

    def getIdByLogin(self, login):
        if login in self.keys():
            return login
        return None

    def getUserByLogin(self, login):
        return self.get(login)


class UserNameChooser(grok.Adapter):
    grok.context(Directory)
    grok.implements(INameChooser)

    def checkName(self, name, object):
        return not name in self.context

    def chooseName(self, name, object):
        return object.id
