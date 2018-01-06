from django.conf import settings
from django.conf.urls import url, static
from django.conf.urls.static import static

from django.contrib import admin

from authentication.views import signup, check_signup, signin, signout


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^check/$', check_signup, name='check_signup'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', signin, name='signin'),
    url(r'^logout/$', signout, name='signout'),
]

# if settings.DEBUG == True:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)