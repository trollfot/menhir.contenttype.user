## -*- coding: utf-8 -*-

import grokcore.view as grok
import dolmen.app.layout as layout

from dolmen import menu
from dolmen.app.authentication.interfaces import IChangePassword
from dolmen.forms.crud import utils
from dolmen.forms.base import Fields
from zeam.form.ztk import action
from menhir.contenttype.user import IUser, MF as _

from zope.formlib.interfaces import IWidgetInputError
from zope.interface import implements
from zope.schema import ValidationError


class DuplicatedLogin(ValidationError):
    implements(IWidgetInputError)
    __doc__ = _(u"This user identifier is already in use.")


class UserAdd(layout.Add):
    grok.name("useradd")
    grok.require('dolmen.security.AddUsers')

    ignoreContext = True

    user_fields = Fields(IUser)
    fields = (user_fields.omit('password') + Fields(IChangePassword)).select(
        'id', 'title', 'email', 'portrait', 'password', 'verify_pass')

    def create(self, data):
        obj = self.context.factory()
        utils.notify_object_creation(self.user_fields, obj, data)
        return obj


class UserEdit(layout.Edit):
    grok.name('edit')
    grok.context(IUser)
    fields = Fields(IUser).select(
        'title', 'email', 'portrait')


@menu.menuentry(layout.ContextualMenu)
class UserPassword(layout.Form):
    grok.context(IUser)
    grok.name('change_passwd')
    grok.title(_("Change password"))
    grok.require("dolmen.content.Edit")
    
    fields = Fields(IChangePassword)
    form_name = _('Change password')

    @action(_('Change password'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.context.password = data['password']
        self.redirect(self.url(self.context))
