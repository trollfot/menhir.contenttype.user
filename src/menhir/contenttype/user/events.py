# -*- coding: utf-8 -*-

import grokcore.component as grok

from dolmen.authentication import IPrincipalFolder
from menhir.contenttype.user import IUser, Directory
from zope.component import getSiteManager
from zope.component.hooks import getSite
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.securitypolicy import interfaces as security


@grok.subscribe(IUser, IObjectAddedEvent)
def grant_permissions(ob, event):
    prinrole = security.IPrincipalRoleManager(ob)
    prinrole.assignRoleToPrincipal('dolmen.Owner', ob.id)
    site = getSite()
    prinrole = security.IPrincipalRoleManager(site)
    prinrole.assignRoleToPrincipal('dolmen.Member', ob.id)


@grok.subscribe(IPrincipalFolder, IObjectAddedEvent)
def UserFolderInitiation(ob, event):
    """We grant the right to register to an anonymous user.
    """
    rpm = security.IPrincipalPermissionManager(ob)
    rpm.grantPermissionToPrincipal('dolmen.security.AddUsers', 'zope.anybody')

    sitemanager = getSiteManager()
    sitemanager.registerUtility(ob, IPrincipalFolder, name=ob.__name__)
