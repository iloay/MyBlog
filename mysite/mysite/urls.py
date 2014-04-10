from django.conf.urls import patterns, include, url
from mysite.blog.views import show,full,main,add_comment,month
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/$',show,{'template_name':'catalog.html','pg':10}),
    url(r'^abstract/$',show,{'template_name':'abstract.html','pg':3}),
    url(r'^list/(?P<pk>\d+)/$',full),
    url(r'^main/$',main),
    url(r'^add_comment/(?P<pk>\d+)/$',add_comment),
    url(r'^show_archive/(?P<year>\d+)/(?P<month>\d+)/$',month),
#    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
