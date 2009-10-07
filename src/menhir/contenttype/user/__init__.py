from zope.i18nmessageid import MessageFactory
mf = MessageFactory("dolmen")
del MessageFactory

from menhir.contenttype.user.user import IPortrait, User, UserView
from menhir.contenttype.user.directory import Directory, DuplicatedLogin
from menhir.contenttype.user.forms import UserAdd, UserEdit, UserPassword
