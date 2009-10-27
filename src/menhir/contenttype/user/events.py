# -*- coding: utf-8 -*-

import grok

from zope.component import getSiteManager
from zope.app.component.hooks import getSite
from zope.securitypolicy import interfaces as security

from dolmen.app.site import IDolmen
from dolmen.app.authentication import IUser, IUserDirectory


@grok.subscribe(IUser, grok.IObjectAddedEvent)
def grant_permissions(ob, event):
    prinrole = security.IPrincipalRoleManager(ob)
    prinrole.assignRoleToPrincipal('dolmen.Owner', ob.id)
    site = getSite()
    prinrole = security.IPrincipalRoleManager(site)
    prinrole.assignRoleToPrincipal('dolmen.Member', ob.id)


@grok.subscribe(IUserDirectory, grok.IObjectAddedEvent)
def UserFolderInitiation(ob, event):
    """We grant the right to register to an anonymous user.
    """
    rpm = security.IPrincipalPermissionManager(ob)
    rpm.grantPermissionToPrincipal('dolmen.security.AddUsers', 'zope.anybody')
    
    sitemanager = getSiteManager()
    sitemanager.registerUtility(ob, IUserDirectory, name=u'', info=u'')
