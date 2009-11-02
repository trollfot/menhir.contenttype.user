## -*- coding: utf-8 -*-

import grokcore.view as grok

from zope.event import notify
from zope.component import getUtility
from zope.lifecycleevent import ObjectCreatedEvent

import dolmen.app.layout as layout
from dolmen.app.authentication.interfaces import *
from dolmen.forms.crud import utils
from dolmen.forms.base import button, validator, Fields
from menhir.contenttype.user import DuplicatedLogin, IPortrait, mf as _


class UserAdd(layout.Add):
    grok.name("useradd")
    grok.require('dolmen.security.AddUsers')

    ignoreContext = True

    user_fields = Fields(IUser, IPortrait)
    fields = (user_fields.omit('password') + Fields(IChangePassword)).select(
        'id', 'title', 'email', 'portrait', 'password', 'verify_pass'
        )

    def create(self, data):
        obj = self.context.factory()
        utils.notify_object_creation(self.user_fields, obj, data)
        return obj


class LoginValidator(validator.SimpleFieldValidator, grok.MultiAdapter):
    grok.adapts(None, None, UserAdd, IUser['id'].__class__, None)

    def validate(self, value):
        super(LoginValidator, self).validate(value)
        users = getUtility(IUserDirectory)
        if users.getIdByLogin(value) is not None:
            raise DuplicatedLogin(value)


class UserEdit(layout.Edit):
    grok.name('edit')
    grok.context(IUser)
    fields = Fields(IPrincipal, IPortrait).select(
        'title', 'email', 'portrait'
        )


class UserPassword(layout.Form, layout.ContextualMenuEntry):
    grok.context(IUser)
    grok.name('change_passwd')
    grok.title("Change password")
    grok.require("dolmen.content.Edit")
    
    fields = Fields(IChangePassword)
    form_name = _('Change password')

    @button.buttonAndHandler(_('Change password'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.context.password = data['password']
        self.redirect(self.url(self.context))
