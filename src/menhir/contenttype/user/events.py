# -*- coding: utf-8 -*-

import grok

from zope.site.hooks import getSite
from zope.component import getSiteManager
from zope.securitypolicy import interfaces as security

from dolmen.app.site import IDolmen
from dolmen.authentication import IPrincipalFolder
from menhir.contenttype.user import IUser


@grok.subscribe(IUser, grok.IObjectAddedEvent)
def grant_permissions(ob, event):
    prinrole = security.IPrincipalRoleManager(ob)
    prinrole.assignRoleToPrincipal('dolmen.Owner', ob.id)
    site = getSite()
    prinrole = security.IPrincipalRoleManager(site)
    prinrole.assignRoleToPrincipal('dolmen.Member', ob.id)


@grok.subscribe(IPrincipalFolder, grok.IObjectAddedEvent)
def UserFolderInitiation(ob, event):
    """We grant the right to register to an anonymous user.
    """
    rpm = security.IPrincipalPermissionManager(ob)
    rpm.grantPermissionToPrincipal('dolmen.security.AddUsers', 'zope.anybody')
