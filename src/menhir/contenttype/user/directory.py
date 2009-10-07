# -*- coding: utf-8 -*-

import grok
import dolmen.content
from zope.app.container.interfaces import INameChooser
from dolmen.app.authentication import IUserDirectory, UserRegistrationError


class DuplicatedLogin(UserRegistrationError):
    __doc__ = u"This user identifier is already in use."
    

class Directory(dolmen.content.Container):
    grok.implements(IUserDirectory)
    dolmen.content.icon("directory.png")
    dolmen.content.name("User directory")
    dolmen.content.schema(dolmen.content.IBaseContent)
    dolmen.content.require('dolmen.security.ManageUsers')

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
