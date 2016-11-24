from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    #url(r'^$', hello.views.index, name='index'),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', hello.views.logout_page, name='logout_page'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', hello.views.register, name='register'),
    url(r'^register/success/$', hello.views.register_success, name='register_success'),
    url(r'^home/$', hello.views.home, name='home'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^status', hello.views.status_report, name='status_report'),
    url(r'^admin/', include(admin.site.urls)),
]
