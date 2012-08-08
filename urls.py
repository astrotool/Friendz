#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from friendz.views import viewupdates, search, adduser, register, getupdate, addupdate, getsess, login, homepage, welcome, logout#Import from view
from friendz.sitefeed import LatestEntriesFeed


from django.contrib import admin
admin.autodiscover()

#feeds = {'viewupdates': LatestEntriesFeed}

urlpatterns = patterns('',
	(r'^welcome/$', welcome),
	(r'^login/$', login), 
	(r'^home/$', homepage),
	(r'^addupdate/$', addupdate),
	(r'^logout/$', logout),
	(r'^register/$', register),
	(r'^getsess/$', getsess),
	(r'^search/$', search),
	(r'^viewupdates/$', viewupdates),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', welcome),
    #(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^latest/feed/$', LatestEntriesFeed()),
    (r'^update/(\d{1,2})/$', getupdate),
    (r'^adduser/(.*)/$', adduser),
    #(r'', include(django.contrib.flatpages.urls)),
)

