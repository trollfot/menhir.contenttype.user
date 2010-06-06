# -*- coding: utf-8 -*-

import grokcore.component as grok

from zope.component import getSiteManager
from zope.component.hooks import getSite
from zope.securitypolicy import interfaces as security

from dolmen.app.site import IDolmen
from menhir.contenttype.user import IUser, IDirectory


@grok.subscribe(IUser, grok.IObjectAddedEvent)
def grant_permissions(ob, event):
    prinrole = security.IPrincipalRoleManager(ob)
    prinrole.assignRoleToPrincipal('dolmen.Owner', ob.id)
    site = getSite()
    prinrole = security.IPrincipalRoleManager(site)
    prinrole.assignRoleToPrincipal('dolmen.Member', ob.id)


@grok.subscribe(IDirectory, grok.IObjectAddedEvent)
def UserFolderInitiation(ob, event):
    """We grant the right to register to an anonymous user.
    """
    rpm = security.IPrincipalPermissionManager(ob)
    rpm.grantPermissionToPrincipal('dolmen.security.AddUsers', 'zope.anybody')
    
    sitemanager = getSiteManager()
    sitemanager.registerUtility(ob, IDirectory, name=ob.__name__, info=u'')
