from django.conf.urls.defaults import *
from django.contrib import admin
from app.resources import api

admin.autodiscover()

urlpatterns = patterns('',
    # The normal jazz here...
    url(r'admin/', include(admin.site.urls)),
    (r'^api/', include(api.urls)),
)
