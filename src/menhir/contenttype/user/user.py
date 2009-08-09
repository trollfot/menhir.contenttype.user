# -*- coding: utf-8 -*-

import grok
from z3c.form import field, button
import dolmen.content as content
from dolmen.app.layout import models as layout
from dolmen.app.authentication import IUser, IPrincipal, IChangePassword
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.app.authentication.interfaces import IPasswordManager

_ = MessageFactory("dolmen")


class User(content.Container):
    content.icon('user.png')
    content.name('User')
    content.schema(IUser)
    content.require('dolmen.security.AddUsers')

    relations = None

    def __init__(self):
        content.Container.__init__(self)
        self._password = u""
        
    def get_password(self):
        return self._password
        
    def set_password(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        self._password = passwordmanager.encodePassword(password)

    password = property(get_password, set_password)

    def checkPassword(self, password):
        passwordmanager = getUtility(IPasswordManager, 'SHA1')
        return passwordmanager.checkPassword(self.password, password)



class UserView(layout.DefaultView):
    grok.name('index')
    grok.context(IUser)
    fields = field.Fields(IPrincipal).omit('description')


class UserEdit(layout.Edit):
    grok.name('edit')
    grok.context(IUser)
    fields = field.Fields(IPrincipal).omit('id', 'description')


class UserPassword(layout.Form, layout.TabView):
    grok.name('change_passwd')
    grok.title("Change password")
    grok.context(IUser)
    fields = field.Fields(IChangePassword)

    form_name = _('Change password')

    @button.buttonAndHandler(_('Change password'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.context.password = data['password']
        self.redirect(self.url(self.context))
