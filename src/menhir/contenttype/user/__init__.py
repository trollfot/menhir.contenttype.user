from zope.i18nmessageid import MessageFactory
MF = MessageFactory("dolmen")
del MessageFactory

from menhir.contenttype.user.user import IUser, User
from menhir.contenttype.user.directory import Directory, IDirectory
from menhir.contenttype.user.browser.forms import (
    UserAdd, UserEdit, UserPassword)
